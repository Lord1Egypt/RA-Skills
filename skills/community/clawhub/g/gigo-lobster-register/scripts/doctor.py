from __future__ import annotations

import os
import platform
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .runtime_bootstrap import inspect_runtime
from .session_client import end_task_session, start_task_session
from .soul_parser import find_soul_md_path
from .task_fetcher import fetch_task_package
from .utils import check_environment, friendly_os_name, resolve_default_lang, resolve_upload_mode, t
from .version_checker import check_skill_version


@dataclass
class DoctorItem:
    status: str
    label: str
    detail: str


def _print_item(item: DoctorItem) -> None:
    prefix = {"ok": "✅", "warn": "⚠️", "fail": "❌"}.get(item.status, "•")
    print(f"{prefix} {item.label}: {item.detail}")


def _write_test(output_dir: Path) -> tuple[str, str]:
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix="gigo-doctor-", suffix=".tmp", dir=output_dir, delete=True) as handle:
            handle.write(b"ok")
            handle.flush()
        return "ok", str(output_dir)
    except Exception as error:
        return "fail", str(error)


def run_doctor(config: dict[str, Any], repo_root: Path, *, offline: bool = False) -> int:
    lang = config.get("lang", "zh")
    print(t(lang, "doctor_title"))

    items: list[DoctorItem] = []
    py_version = ".".join(str(part) for part in platform.python_version_tuple()[:3])
    items.append(DoctorItem("ok", t(lang, "doctor_python"), py_version))
    items.append(
        DoctorItem(
            "ok",
            t(lang, "doctor_defaults"),
            t(
                lang,
                "doctor_defaults_ready",
                default_lang=resolve_default_lang(True),
                upload_mode=resolve_upload_mode(True),
            ),
        )
    )

    runtime = inspect_runtime(repo_root)
    if runtime.current_missing:
        items.append(
            DoctorItem(
                "warn",
                t(lang, "doctor_runtime"),
                t(lang, "doctor_runtime_missing", packages=", ".join(runtime.current_missing)),
            )
        )
    else:
        items.append(
            DoctorItem(
                "ok",
                t(lang, "doctor_runtime"),
                t(lang, "doctor_runtime_ready", runtime_root=str(runtime.runtime_root)),
            )
        )

    cert_missing = [package for package in runtime.current_missing if package in {"Pillow", "qrcode"}]
    if cert_missing:
        items.append(
            DoctorItem(
                "warn",
                t(lang, "doctor_certificate"),
                t(lang, "doctor_certificate_svg", packages=", ".join(cert_missing)),
            )
        )
    elif lang == "zh":
        from .cert_generator import supports_cjk_png_text

        if not supports_cjk_png_text():
            items.append(
                DoctorItem(
                    "warn",
                    t(lang, "doctor_certificate"),
                    t(lang, "doctor_certificate_cjk_missing"),
                )
            )
        else:
            items.append(DoctorItem("ok", t(lang, "doctor_certificate"), t(lang, "doctor_certificate_png")))
    else:
        items.append(DoctorItem("ok", t(lang, "doctor_certificate"), t(lang, "doctor_certificate_png")))

    output_status, output_detail = _write_test(Path(config["output_dir"]))
    items.append(DoctorItem(output_status, t(lang, "doctor_output"), output_detail))

    soul_path = find_soul_md_path(repo_root)
    if soul_path:
        items.append(DoctorItem("ok", t(lang, "doctor_soul"), str(soul_path)))
    else:
        items.append(DoctorItem("warn", t(lang, "doctor_soul"), t(lang, "doctor_soul_missing")))

    env_info = check_environment(config, repo_root)
    if offline:
        items.append(DoctorItem("warn", t(lang, "doctor_gateway"), t(lang, "doctor_gateway_skipped")))
        items.append(DoctorItem("warn", t(lang, "doctor_cloud"), t(lang, "doctor_cloud_skipped")))
        items.append(DoctorItem("warn", t(lang, "doctor_bundle"), t(lang, "doctor_bundle_skipped")))
    else:
        if env_info.gateway_available:
            detail = env_info.gateway_model or friendly_os_name(env_info.os_name)
            items.append(DoctorItem("ok", t(lang, "doctor_gateway"), detail))
        else:
            items.append(DoctorItem("fail", t(lang, "doctor_gateway"), t(lang, "doctor_gateway_missing")))

        version = check_skill_version(config, repo_root, offline=False)
        if version.error:
            items.append(DoctorItem("warn", t(lang, "doctor_cloud"), version.error))
        else:
            latest = version.latest_stable or version.local_version
            items.append(DoctorItem("ok", t(lang, "doctor_cloud"), t(lang, "doctor_cloud_ready", version=latest)))

        session = None
        bundle_status = "warn"
        bundle_detail = t(lang, "doctor_bundle_skipped")
        try:
            session = start_task_session(config)
            config_for_fetch = dict(config)
            config_for_fetch["task_session"] = session
            tasks = fetch_task_package(config_for_fetch, repo_root)
            source = config_for_fetch.get("task_bundle_source", "unknown")
            version = config_for_fetch.get("task_bundle_version", "unknown")
            if source in {"remote", "remote_session"}:
                bundle_status = "ok"
            else:
                bundle_status = "warn"
            bundle_detail = t(
                lang,
                "doctor_bundle_ready",
                task_count=len(tasks),
                version=version,
                source=source,
            )
        except Exception as error:
            bundle_status = "fail"
            bundle_detail = str(error)
        finally:
            if session:
                config_for_end = dict(config)
                config_for_end["task_session"] = session
                end_task_session(config_for_end)
        items.append(DoctorItem(bundle_status, t(lang, "doctor_bundle"), bundle_detail))

    for item in items:
        _print_item(item)

    has_fail = any(item.status == "fail" for item in items)
    if has_fail:
        print(t(lang, "doctor_summary_fail"))
        return 1

    print(t(lang, "doctor_summary_ready"))
    return 0
