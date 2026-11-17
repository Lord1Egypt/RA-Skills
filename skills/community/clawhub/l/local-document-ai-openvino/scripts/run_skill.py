#!/usr/bin/env python3
"""
run_skill.py

Lightweight orchestrator for the Local Document AI with OpenVINO skill.

Supports three input styles:
1. Direct CLI flags
2. --config-file path/to/config.json
3. --config-json '{"mode":"to-code", ...}'

Responsibilities:
1. Resolve input/output paths
2. Run parse_document.py
3. Optionally run a downstream transform script
4. Write a combined run_report.json
5. Print a concise JSON status payload to stdout
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from dataclasses import replace
from pathlib import Path
from typing import Any

from _local_vendor import bootstrap_local_vendor
from utils import (
    detect_input_type,
    ensure_artifact_layout,
    ensure_dir,
    get_default_artifact_dir,
    now_iso,
    parse_json_from_subprocess_output,
    summarize_generated_files,
    write_error,
    write_json,
)


bootstrap_local_vendor()


SUPPORTED_MODES = {"parse", "to-code", "to-data"}
BASE_DIR = Path(__file__).resolve().parent
ALLOWED_CONFIG_KEYS = {
    "mode",
    "file",
    "out",
    "target",
    "extract",
    "fields",
    "title",
    "audience",
    "debug",
    "use_server",
    "no_server",
    "server_timeout",
    "server_kind",
}


@dataclass
class Config:
    mode: str
    file: Path
    out: Path | None = None
    target: str = "react"
    extract: str = "tables,entities,kv_pairs"
    fields: str | None = None
    title: str | None = None
    audience: str = "developer"
    debug: bool = False
    use_server: bool = True
    server_timeout: float = 300.0
    server_kind: str = "auto"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Local Document AI with OpenVINO skill pipeline."
    )

    parser.add_argument("--config-file", help="Path to JSON config file")
    parser.add_argument("--config-json", help="Inline JSON config string")

    parser.add_argument("--mode", choices=sorted(SUPPORTED_MODES), help="Pipeline mode")
    parser.add_argument("--file", help="Input PDF or image path")
    parser.add_argument("--out", help="Artifact output directory")
    parser.add_argument("--target", default="react", help="Target for to-code mode")
    parser.add_argument("--extract", default="tables,entities,kv_pairs", help="Extract list for to-data mode")
    parser.add_argument("--fields", help="Comma-separated key fields to extract for to-data mode")
    parser.add_argument("--title", help="Optional title override for to-code")
    parser.add_argument("--audience", default="developer", help="Reserved for future slide generation mode")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--use-server",
        action="store_true",
        help="Route the parse step through a persistent local MinerU/OpenVINO server. This is now the default.",
    )
    parser.add_argument(
        "--no-server",
        action="store_true",
        help="Disable the auto local service and run the parse step directly in the current process.",
    )
    parser.add_argument(
        "--server-timeout",
        type=float,
        default=300.0,
        help="Seconds to wait for the persistent parse server to start.",
    )
    parser.add_argument(
        "--server-kind",
        choices=["auto", "http", "ipc"],
        default=os.environ.get("LOCAL_DOCUMENT_AI_SERVER_KIND", "auto"),
        help="Server transport. auto prefers HTTP/FastAPI and falls back to the stdlib IPC server.",
    )
    parser.add_argument(
        "--server-status",
        action="store_true",
        help="Print persistent parse server status and exit.",
    )
    parser.add_argument(
        "--warmup-server",
        action="store_true",
        help="Start the persistent parse server and preload the MinerU/OpenVINO runtime.",
    )
    parser.add_argument(
        "--shutdown-server",
        action="store_true",
        help="Ask the persistent parse server to shut down and exit.",
    )

    return parser.parse_args()


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def coerce_path(value: str | None) -> Path | None:
    if value is None or value == "":
        return None
    return Path(value).expanduser().resolve()


def normalize_config_payload(raw: dict[str, Any], cli_ns: argparse.Namespace) -> Config:
    unknown_keys = sorted(set(raw.keys()) - ALLOWED_CONFIG_KEYS)
    if unknown_keys:
        raise ValueError(f"Unsupported config keys: {', '.join(unknown_keys)}")

    def cli_or_raw(name: str, default: Any = None) -> Any:
        cli_value = getattr(cli_ns, name, None)
        if cli_value not in (None, ""):
            if name in {"mode", "file", "out", "fields", "title"}:
                return cli_value
        return raw.get(name, cli_value if cli_value not in (None, "") else default)

    mode = cli_or_raw("mode")
    file_value = cli_or_raw("file")
    out_value = cli_or_raw("out")
    target = raw.get("target", cli_ns.target)
    extract = raw.get("extract", cli_ns.extract)
    fields = cli_or_raw("fields")
    title = raw.get("title", cli_ns.title)
    audience = raw.get("audience", cli_ns.audience)
    debug = bool(raw.get("debug", cli_ns.debug))
    raw_has_use_server = "use_server" in raw
    no_server = bool(raw.get("no_server", False)) or bool(cli_ns.no_server)
    use_server = bool(raw.get("use_server", True)) if raw_has_use_server else True
    use_server = (use_server or bool(cli_ns.use_server)) and not no_server
    server_timeout = float(raw.get("server_timeout", cli_ns.server_timeout))
    server_kind = str(raw.get("server_kind", cli_ns.server_kind or "auto"))

    if cli_ns.target != "react":
        target = cli_ns.target
    if cli_ns.extract != "tables,entities,kv_pairs":
        extract = cli_ns.extract
    if cli_ns.fields not in (None, ""):
        fields = cli_ns.fields
    if cli_ns.audience != "developer":
        audience = cli_ns.audience
    if cli_ns.debug:
        debug = True
    if os.environ.get("LOCAL_DOCUMENT_AI_USE_SERVER", "").strip().lower() in {"1", "true", "yes", "on"}:
        use_server = True
    if os.environ.get("LOCAL_DOCUMENT_AI_DISABLE_SERVER", "").strip().lower() in {"1", "true", "yes", "on"}:
        use_server = False

    if not mode:
        raise ValueError("Missing required config field: mode")
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"Unsupported mode: {mode}")

    if not file_value:
        raise ValueError("Missing required config field: file")

    return Config(
        mode=mode,
        file=Path(file_value).expanduser().resolve(),
        out=coerce_path(out_value),
        target=str(target),
        extract=str(extract),
        fields=str(fields) if fields not in (None, "") else None,
        title=title,
        audience=str(audience),
        debug=debug,
        use_server=use_server,
        server_timeout=server_timeout,
        server_kind=server_kind,
    )


def build_config(ns: argparse.Namespace) -> Config:
    if ns.config_json:
        raw = json.loads(ns.config_json)
        return normalize_config_payload(raw, ns)

    if ns.config_file:
        raw = load_json_file(Path(ns.config_file).expanduser().resolve())
        return normalize_config_payload(raw, ns)

    if not ns.mode:
        raise ValueError("Missing required argument: --mode (or provide --config-file / --config-json)")
    if not ns.file:
        raise ValueError("Missing required argument: --file (or provide --config-file / --config-json)")

    return Config(
        mode=ns.mode,
        file=Path(ns.file).expanduser().resolve(),
        out=coerce_path(ns.out),
        target=ns.target,
        extract=ns.extract,
        fields=ns.fields,
        title=ns.title,
        audience=ns.audience,
        debug=ns.debug,
        use_server=(
            not ns.no_server
            and os.environ.get("LOCAL_DOCUMENT_AI_DISABLE_SERVER", "").strip().lower() not in {"1", "true", "yes", "on"}
        ),
        server_timeout=ns.server_timeout,
        server_kind=ns.server_kind,
    )


def run_subprocess(cmd: list[str]) -> dict[str, Any]:
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )

    status = None
    if proc.stdout.strip():
        try:
            status = parse_json_from_subprocess_output(proc.stdout)
        except Exception:
            status = None

    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "status": status,
        "cmd": cmd,
    }


def build_parse_cmd(config: Config, artifact_dir: Path) -> list[str]:
    script = BASE_DIR / ("parse_client.py" if config.use_server else "parse_document.py")
    cmd = [
        sys.executable,
        str(script),
        "--file",
        str(config.file),
        "--out",
        str(artifact_dir),
        "--mode",
        config.mode,
    ]
    if config.debug:
        cmd.append("--debug")
    if config.use_server:
        cmd.extend(["--connect-timeout", str(config.server_timeout), "--server-kind", config.server_kind])
    return cmd


def run_parse_with_fallback(config: Config, artifact_dir: Path) -> dict[str, Any]:
    parse_run = run_subprocess(build_parse_cmd(config, artifact_dir))
    if parse_run["returncode"] == 0 or not config.use_server:
        return parse_run

    direct_config = replace(config, use_server=False)
    direct_run = run_subprocess(build_parse_cmd(direct_config, artifact_dir))
    if direct_run["returncode"] == 0:
        direct_run["server_fallback"] = {
            "used": True,
            "server_kind": config.server_kind,
            "server_returncode": parse_run["returncode"],
            "server_stdout": parse_run["stdout"],
            "server_stderr": parse_run["stderr"],
        }
        if isinstance(direct_run.get("status"), dict):
            direct_run["status"]["server_fallback"] = True
            direct_run["status"]["server_kind_attempted"] = config.server_kind
        return direct_run
    return parse_run


def build_transform_cmd(config: Config, artifact_dir: Path) -> list[str] | None:
    parsed_json = artifact_dir / "parsed.json"
    task_output = artifact_dir / "task_output"

    if config.mode == "to-code":
        script = BASE_DIR / "transform_doc_to_code.py"
        cmd = [
            sys.executable,
            str(script),
            "--parsed-json",
            str(parsed_json),
            "--out",
            str(task_output),
            "--target",
            config.target,
        ]
        if config.title:
            cmd.extend(["--title", config.title])
        if config.debug:
            cmd.append("--debug")
        return cmd

    if config.mode == "to-data":
        script = BASE_DIR / "transform_doc_to_data.py"
        cmd = [
            sys.executable,
            str(script),
            "--parsed-json",
            str(parsed_json),
            "--out",
            str(task_output),
            "--extract",
            config.extract,
        ]
        if config.fields:
            cmd.extend(["--fields", config.fields])
        if config.debug:
            cmd.append("--debug")
        return cmd

    return None


def build_report_cmd(config: Config, artifact_dir: Path) -> list[str]:
    script = BASE_DIR / "render_result_report.py"
    return [
        sys.executable,
        str(script),
        "--artifact-dir",
        str(artifact_dir),
    ]


def resolve_artifact_dir(config: Config) -> Path:
    if config.out is not None:
        return config.out
    return get_default_artifact_dir(config.file, base_dir=BASE_DIR.parent)


def build_effective_config_payload(config: Config, artifact_dir: Path) -> dict[str, Any]:
    return {
        "mode": config.mode,
        "file": str(config.file),
        "input_type": detect_input_type(config.file),
        "out": str(artifact_dir),
        "target": config.target,
        "extract": config.extract,
        "fields": config.fields,
        "title": config.title,
        "audience": config.audience,
        "debug": config.debug,
        "use_server": config.use_server,
        "server_timeout": config.server_timeout,
        "server_kind": config.server_kind,
    }


def write_run_report(
    artifact_dir: Path,
    config: Config,
    parse_result: dict[str, Any],
    transform_result: dict[str, Any] | None,
    report_result: dict[str, Any] | None,
) -> Path:
    report = {
        "run_at": now_iso(),
        "config": build_effective_config_payload(config, artifact_dir),
        "parse": parse_result,
        "transform": transform_result,
        "report": report_result,
        "generated_files": summarize_generated_files(artifact_dir),
    }
    report_path = artifact_dir / "run_report.json"
    write_json(report_path, report)
    return report_path


def write_effective_manifest(artifact_dir: Path, config: Config) -> Path:
    manifest_path = artifact_dir / "effective_config.json"
    write_json(manifest_path, build_effective_config_payload(config, artifact_dir))
    return manifest_path


def main() -> int:
    ns = parse_args()

    early_error_dir = Path.cwd() / "artifacts" / "run_skill_error"

    try:
        if ns.server_status or ns.warmup_server or ns.shutdown_server:
            client_script = BASE_DIR / "parse_client.py"
            cmd = [
                sys.executable,
                str(client_script),
                "--connect-timeout",
                str(ns.server_timeout),
                "--server-kind",
                str(ns.server_kind),
            ]
            if ns.server_status:
                cmd.append("--status")
            if ns.warmup_server:
                cmd.append("--warmup")
            if ns.shutdown_server:
                cmd.append("--shutdown")
            server_run = run_subprocess(cmd)
            if server_run["stdout"].strip():
                print(server_run["stdout"].strip())
            if server_run["returncode"] != 0 and server_run["stderr"].strip():
                print(server_run["stderr"].strip(), file=sys.stderr)
            return int(server_run["returncode"])

        config = build_config(ns)
        artifact_dir = resolve_artifact_dir(config)

        ensure_artifact_layout(artifact_dir)
        ensure_dir(BASE_DIR)

        if not config.file.exists():
            raise FileNotFoundError(f"Input file not found: {config.file}")

        write_effective_manifest(artifact_dir, config)

        parse_run = run_parse_with_fallback(config, artifact_dir)

        if parse_run["returncode"] != 0:
            write_error(
                artifact_dir,
                stage="run_skill.parse",
                message="Parse step failed",
                config=build_effective_config_payload(config, artifact_dir),
                parse_stdout=parse_run["stdout"],
                parse_stderr=parse_run["stderr"],
            )
            print(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "parse",
                        "mode": config.mode,
                        "input_file": str(config.file),
                        "artifact_dir": str(artifact_dir),
                        "message": "Parse step failed",
                        "stderr": parse_run["stderr"],
                    },
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            return 1

        transform_run: dict[str, Any] | None = None

        if config.mode != "parse":
            transform_cmd = build_transform_cmd(config, artifact_dir)

            if transform_cmd is None:
                write_error(
                    artifact_dir,
                    stage="run_skill.transform",
                    message=f"Mode not implemented yet: {config.mode}",
                    config=build_effective_config_payload(config, artifact_dir),
                )
                print(
                    json.dumps(
                        {
                            "ok": False,
                            "stage": "transform",
                            "mode": config.mode,
                            "artifact_dir": str(artifact_dir),
                            "message": f"Mode not implemented yet: {config.mode}",
                        },
                        ensure_ascii=False,
                    ),
                    file=sys.stderr,
                )
                return 1

            transform_run = run_subprocess(transform_cmd)

            if transform_run["returncode"] != 0:
                write_error(
                    artifact_dir,
                    stage="run_skill.transform",
                    message="Transform step failed",
                    config=build_effective_config_payload(config, artifact_dir),
                    transform_stdout=transform_run["stdout"],
                    transform_stderr=transform_run["stderr"],
                )
                print(
                    json.dumps(
                        {
                            "ok": False,
                            "stage": "transform",
                            "mode": config.mode,
                            "input_file": str(config.file),
                            "artifact_dir": str(artifact_dir),
                            "message": "Transform step failed",
                            "stderr": transform_run["stderr"],
                        },
                        ensure_ascii=False,
                    ),
                    file=sys.stderr,
                )
                return 1

        report_run = run_subprocess(build_report_cmd(config, artifact_dir))

        report_path = write_run_report(
            artifact_dir=artifact_dir,
            config=config,
            parse_result=parse_run,
            transform_result=transform_run,
            report_result=report_run,
        )

        final_status = {
            "ok": True,
            "mode": config.mode,
            "input_file": str(config.file),
            "artifact_dir": str(artifact_dir),
            "effective_config": str(artifact_dir / "effective_config.json"),
            "run_report": str(report_path),
            "parse_status": parse_run.get("status"),
            "transform_status": transform_run.get("status") if transform_run else None,
            "report_status": report_run.get("status"),
            "generated_files": summarize_generated_files(artifact_dir),
        }

        print(json.dumps(final_status, ensure_ascii=False))
        return 0

    except Exception as exc:
        ensure_artifact_layout(early_error_dir)
        write_error(
            early_error_dir,
            stage="run_skill",
            message=str(exc),
        )
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "run_skill",
                    "message": str(exc),
                    "artifact_dir": str(early_error_dir),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
