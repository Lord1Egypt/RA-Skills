#!/usr/bin/env python3
"""
ASR one-click diagnostics for meeting-notes-skill.

Purpose:
- Distinguish "model/dependency not installed" vs "second-run state pollution".
- Provide a single consolidated report with actionable next steps.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILL_SLUG = SKILL_ROOT.name
PRIVATE_ROOT = Path.home() / "clawdhome_shared" / "private"
PRIVATE_OUTPUT_DIR = PRIVATE_ROOT / f"{SKILL_SLUG}-data"
WHISPER_CACHE = Path.home() / ".cache" / "whisper"
STATE_DIR = Path.home() / ".meeting-notes-skill"
TMP_DIR = Path("/tmp")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=False, text=True, capture_output=True)


def module_exists(name: str) -> bool:
    p = run([sys.executable, "-c", f"import {name}"])
    return p.returncode == 0


def ensure_private_dir() -> tuple[bool, str]:
    try:
        PRIVATE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        probe = PRIVATE_OUTPUT_DIR / ".asr_self_check_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True, str(PRIVATE_OUTPUT_DIR)
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def resolve_report_path(user_path: str | None) -> Path:
    if user_path:
        return Path(user_path).expanduser().resolve()
    try:
        PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        return (PRIVATE_ROOT / "asr-self-check-report.json").resolve()
    except Exception:
        return (Path.cwd() / "asr-self-check-report.json").resolve()


def inspect_whisper_cache() -> dict:
    info = {
        "cache_dir": str(WHISPER_CACHE),
        "exists": WHISPER_CACHE.exists(),
        "model_files": [],
        "partial_or_suspicious": [],
    }
    if not WHISPER_CACHE.exists():
        return info
    for p in sorted(WHISPER_CACHE.glob("*.pt")):
        size_mb = round(p.stat().st_size / (1024 * 1024), 2)
        item = {"name": p.name, "size_mb": size_mb, "path": str(p)}
        info["model_files"].append(item)
        if size_mb < 1.0:
            info["partial_or_suspicious"].append(item)
    for p in sorted(WHISPER_CACHE.glob("*.tmp")):
        info["partial_or_suspicious"].append(
            {"name": p.name, "size_mb": round(p.stat().st_size / (1024 * 1024), 2), "path": str(p)}
        )
    return info


def find_state_pollution() -> dict:
    tmp_patterns = ["builtin_asr_*", "builtin_asr_swift_cache_*", "tmp*whisper*"]
    leftovers: list[str] = []
    for pat in tmp_patterns:
        for p in TMP_DIR.glob(pat):
            leftovers.append(str(p))
    return {
        "state_dir": str(STATE_DIR),
        "state_dir_exists": STATE_DIR.exists(),
        "tmp_leftover_count": len(leftovers),
        "tmp_leftovers": leftovers[:20],
    }


def clean_state_pollution() -> dict:
    removed: list[str] = []
    failed: list[str] = []
    for pat in ["builtin_asr_*", "builtin_asr_swift_cache_*", "tmp*whisper*"]:
        for p in TMP_DIR.glob(pat):
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink(missing_ok=True)
                removed.append(str(p))
            except Exception:  # noqa: BLE001
                failed.append(str(p))
    return {"removed_count": len(removed), "failed_count": len(failed), "removed": removed[:20], "failed": failed[:20]}


def parse_kv(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for ln in text.splitlines():
        if "=" not in ln:
            continue
        k, v = ln.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def smoke_asr(audio_file: Path, topic: str, provider: str) -> dict:
    bridge = SCRIPT_DIR / "audio_bridge.py"
    cmd = [
        sys.executable,
        str(bridge),
        "asr",
        "--input",
        str(audio_file),
        "--topic",
        topic,
        "--provider",
        provider,
        "--language",
        "zh",
    ]
    p = run(cmd)
    info = {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    if p.returncode == 0:
        kv = parse_kv(p.stdout)
        info["provider"] = kv.get("provider")
        info["output_dir"] = kv.get("output_dir")
        info["json"] = kv.get("json")
        info["text"] = kv.get("text")
    return info


def summarize(report: dict) -> str:
    lines: list[str] = []
    base = report["base"]
    lines.append("ASR 自检总结")
    lines.append(f"- python3: {'OK' if base['python3'] else '缺失'}")
    lines.append(f"- ffmpeg(必装): {'OK' if base['ffmpeg'] else '缺失'}")
    lines.append(f"- edge_tts(必装): {'OK' if base['edge_tts'] else '缺失'}")
    lines.append(f"- whisper(ASR必装): {'OK' if base['whisper'] else '未安装'}")
    lines.append(f"- OPENAI_API_KEY: {'已配置' if base['openai_api_key'] else '未配置'}")
    lines.append(f"- 私有输出目录可写: {'OK' if report['output_dir']['ok'] else '失败'}")

    cache = report["whisper_cache"]
    if cache["exists"]:
        lines.append(f"- Whisper 缓存模型数: {len(cache['model_files'])}")
        if cache["partial_or_suspicious"]:
            lines.append(f"- 发现可疑缓存文件: {len(cache['partial_or_suspicious'])}（可能导致校验/加载失败）")
    else:
        lines.append("- Whisper 缓存目录不存在（若走 local provider，首次会下载模型）")

    pollution = report["pollution"]
    if pollution["tmp_leftover_count"] > 0:
        lines.append(f"- 临时残留文件: {pollution['tmp_leftover_count']}（建议清理后再跑第二次）")
    else:
        lines.append("- 临时残留文件: 未发现")

    smoke = report.get("smoke")
    if smoke:
        if smoke["returncode"] == 0:
            lines.append(f"- 冒烟转写: OK（provider={smoke.get('provider', 'unknown')}）")
        else:
            lines.append("- 冒烟转写: 失败（请看 report.json 的 stderr）")

    lines.append("")
    lines.append("建议动作")
    if not base["ffmpeg"]:
        lines.append("1) 安装 ffmpeg: brew install ffmpeg")
    if not base["edge_tts"]:
        lines.append("2) 安装 edge-tts: python3 -m pip install edge-tts")
    if pollution["tmp_leftover_count"] > 0:
        lines.append("3) 清理临时残留: python3 scripts/asr_self_check.py --clean-temp")
    if not base["whisper"]:
        lines.append("4) 安装本地 whisper（ASR必装）: python3 -m pip install openai-whisper")
    elif not cache["model_files"]:
        lines.append("4) 预下载 tiny 模型: python3 -c \"import whisper; whisper.load_model('tiny')\"")
    if smoke and smoke["returncode"] != 0:
        lines.append("5) 冒烟失败后建议优先重跑 auto provider，避免单一路径卡死")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="ASR one-click self check")
    ap.add_argument("--input", help="Optional audio file for smoke ASR test")
    ap.add_argument("--topic", default="asr-self-check", help="Topic name used when running smoke ASR")
    ap.add_argument("--provider", choices=["auto", "builtin", "local", "openai"], default="auto")
    ap.add_argument("--clean-temp", action="store_true", help="Clean likely temp/cache leftovers in /tmp")
    ap.add_argument("--report-path", default=None, help="Optional report output path")
    args = ap.parse_args()

    out_ok, out_msg = ensure_private_dir()
    report = {
        "base": {
            "python3": shutil.which("python3") is not None,
            "ffmpeg": shutil.which("ffmpeg") is not None,
            "edge_tts": module_exists("edge_tts"),
            "whisper": module_exists("whisper"),
            "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
        },
        "output_dir": {"ok": out_ok, "detail": out_msg},
        "whisper_cache": inspect_whisper_cache(),
        "pollution": find_state_pollution(),
    }

    if args.clean_temp:
        report["clean_result"] = clean_state_pollution()
        report["pollution_after_clean"] = find_state_pollution()

    if args.input:
        audio = Path(args.input).expanduser().resolve()
        if not audio.exists():
            report["smoke"] = {"returncode": 2, "stderr": f"input not found: {audio}"}
        else:
            report["smoke"] = smoke_asr(audio, args.topic, args.provider)

    report_path = resolve_report_path(args.report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(summarize(report))
    print(f"\nreport_json={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
