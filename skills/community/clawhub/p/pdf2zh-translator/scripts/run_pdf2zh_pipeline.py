from __future__ import annotations

import argparse
import concurrent.futures
import os
import shutil
import subprocess
import tomllib
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def log(msg: str) -> None:
    print(msg, flush=True)


def detect_pdf2zh_cli(explicit_exe: str | None) -> list[str]:
    if explicit_exe:
        p = Path(explicit_exe).expanduser().resolve()
        if not p.exists():
            raise RuntimeError(f"--exe-path not found: {p}")
        return [str(p)]

    for name in ["pdf2zh_next", "pdf2zh-next", "pdf2zh"]:
        path = shutil.which(name)
        if path:
            return [path]

    extra_paths = [
        Path.home() / ".local" / "bin" / "pdf2zh_next",
        Path.home() / ".local" / "bin" / "pdf2zh_next.exe",
        Path.home() / "AppData" / "Roaming" / "Python" / "Scripts" / "pdf2zh_next.exe",
    ]
    for p in extra_paths:
        if p.exists():
            return [str(p)]

    raise RuntimeError("pdf2zh CLI not found. Install pdf2zh-next first, or provide --exe-path.")


def gather_pdfs(files: list[str], folders: list[str], include_globs: list[str], recursive: bool = True) -> list[Path]:
    out: list[Path] = []

    for fp in files:
        p = Path(fp).expanduser().resolve()
        if p.exists() and p.suffix.lower() == ".pdf":
            out.append(p)

    for folder in folders:
        d = Path(folder).expanduser().resolve()
        if not d.exists() or not d.is_dir():
            continue
        out.extend(d.glob("**/*.pdf" if recursive else "*.pdf"))

    uniq = {str(p): p for p in out}
    merged = sorted(uniq.values(), key=lambda x: str(x).lower())

    if include_globs:
        selected: list[Path] = []
        for p in merged:
            rel_name = p.name
            rel_full = str(p)
            if any(p.match(g) or Path(rel_name).match(g) or Path(rel_full).match(g) for g in include_globs):
                selected.append(p)
        return selected

    return merged


def ensure_output_dir(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_cli_help_text(base_cmd: list[str]) -> str:
    cp = subprocess.run([*base_cmd, "-h"], text=True, capture_output=True, check=False, env=_isolated_env())
    return (cp.stdout or "") + "\n" + (cp.stderr or "")


def validate_provider_in_config(config_path: Path, provider: str | None) -> str | None:
    if not provider:
        return None

    name = provider.strip().lower()
    with config_path.open("rb") as f:
        cfg = tomllib.load(f)

    if name not in cfg:
        available = sorted(k for k, v in cfg.items() if isinstance(v, bool))
        raise RuntimeError(
            f"provider '{name}' not found in config.toml top-level service switches. "
            f"available={available}"
        )

    if not isinstance(cfg[name], bool):
        raise RuntimeError(f"config.toml key '{name}' exists but is not a boolean service switch")

    return name


def build_provider_args(help_text: str, provider: str | None) -> list[str]:
    if not provider:
        return []

    provider = provider.strip().lower()
    explicit_flag = f"--{provider}"
    if explicit_flag in help_text:
        return [explicit_flag]

    raise RuntimeError(
        f"Provider '{provider}' is not supported by current pdf2zh CLI help. "
        "Use an official --<Services> name shown in `pdf2zh_next -h`."
    )


def build_config_arg(help_text: str, config_path: Path) -> list[str]:
    if "--config-file" in help_text:
        return ["--config-file", str(config_path)]
    # Older versions may not expose this flag.
    log("[warn] current pdf2zh help does not show --config-file; run may rely on default config behavior.")
    return []


def _isolated_env() -> dict[str, str]:
    # Minimal child env: keep only runtime essentials, drop provider/API secrets by default.
    keep_keys = {
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "TEMP",
        "TMP",
        "LANG",
        "LC_ALL",
    }
    env = {k: v for k, v in os.environ.items() if k in keep_keys}

    isolated_home = str(SKILL_DIR)
    env["HOME"] = isolated_home
    env["USERPROFILE"] = isolated_home
    env["XDG_CONFIG_HOME"] = isolated_home
    env["APPDATA"] = isolated_home
    env["LOCALAPPDATA"] = isolated_home
    return env


def translate_one_cli(base_cmd: list[str], pdf: Path, out_dir: Path, stream: bool, extra_args: list[str], visible_window: bool) -> tuple[bool, str]:
    cmd = [*base_cmd, *extra_args, str(pdf), "--output", str(out_dir)]
    env = _isolated_env()

    if visible_window:
        # Windows native console window for realtime monitoring.
        flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
        proc = subprocess.Popen(cmd, env=env, creationflags=flags)
        rc = proc.wait()
        return rc == 0, f"exit={rc}"

    if stream:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env)
        lines: list[str] = []
        assert proc.stdout is not None
        for line in proc.stdout:
            line = line.rstrip("\n")
            if line:
                log(f"[{pdf.name}] {line}")
                lines.append(line)
                if len(lines) > 120:
                    lines = lines[-120:]
        rc = proc.wait()
        return rc == 0, "\n".join(lines[-40:])

    cp = subprocess.run(cmd, text=True, capture_output=True, env=env)
    tail = (cp.stdout + "\n" + cp.stderr)[-2000:]
    return cp.returncode == 0, tail

def translated_pdf_exists(out_dir: Path, source_pdf: Path) -> bool:
    base = source_pdf.stem
    return any(out_dir.glob(f"{base}*.pdf"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Run pdf2zh-next pipeline via CLI + config.toml")
    ap.add_argument("--input-file", action="append", default=[], help="single pdf; can repeat")
    ap.add_argument("--input-dir", action="append", default=[], help="folder containing pdf files; can repeat")
    ap.add_argument("--include-glob", action="append", default=[], help="optional subset matcher; can repeat")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--exe-path", default=None, help="absolute path to pdf2zh executable")
    ap.add_argument("--provider", default=None, help="optional service name; when set, wrapper passes official --<Services> flag to pdf2zh")
    ap.add_argument("--config-path", default=str(SKILL_DIR / "config.toml"), help="must be skills/translator-pdf2zh/config.toml")
    ap.add_argument("--stream", action="store_true", help="stream progress output")
    ap.add_argument("--visible-monitor", action="store_true", help="show realtime logs for progress monitoring")
    ap.add_argument("--workers", type=int, default=1, help="number of PDFs to translate in parallel (default: 1)")
    ap.add_argument("--recursive", action="store_true", default=True)
    args = ap.parse_args()

    if args.workers < 1:
        raise RuntimeError("--workers must be >= 1")

    config_path = Path(args.config_path).expanduser().resolve()
    allowed_config = (SKILL_DIR / "config.toml").resolve()
    if config_path != allowed_config:
        raise RuntimeError(
            f"config-path not allowed: {config_path}. Only this file is allowed: {allowed_config}"
        )
    if not config_path.exists():
        raise RuntimeError(f"config file not found: {config_path}")

    out_dir = ensure_output_dir(args.output_dir)
    pdfs = gather_pdfs(args.input_file, args.input_dir, include_globs=args.include_glob, recursive=args.recursive)
    if not pdfs:
        raise RuntimeError("no input pdf found (use --input-file and/or --input-dir)")

    provider = validate_provider_in_config(config_path, args.provider)

    cli_cmd = detect_pdf2zh_cli(args.exe_path)
    help_text = read_cli_help_text(cli_cmd)

    cli_extra_args: list[str] = []
    cli_extra_args.extend(build_config_arg(help_text, config_path))
    cli_extra_args.extend(build_provider_args(help_text, provider))

    if "--no-auto-extract-glossary" in help_text:
        cli_extra_args.append("--no-auto-extract-glossary")

    stream = args.stream or args.visible_monitor

    log(f"[setup] using pdf2zh cli: {cli_cmd[0]}")
    log(f"[setup] config={config_path}")
    effective_provider = provider if provider else "(from config.toml)"
    log(f"[run] files={len(pdfs)} provider={effective_provider} workers={args.workers} monitor={'realtime' if stream else 'silent'}")

    def run_one(item: tuple[int, Path]) -> tuple[bool, str]:
        i, pdf = item
        log(f"[run] ({i}/{len(pdfs)}) {pdf}")
        ok, reason = translate_one_cli(cli_cmd, pdf, out_dir, stream, extra_args=cli_extra_args, visible_window=args.visible_monitor)
        if not ok:
            return False, f"{pdf.name}: {reason}"
        if not translated_pdf_exists(out_dir, pdf):
            return False, f"{pdf.name}: output pdf not found"
        return True, pdf.name

    tasks = list(enumerate(pdfs, start=1))

    if args.workers == 1:
        for t in tasks:
            ok, reason = run_one(t)
            if not ok:
                log(f"[error] translation stopped: {reason}")
                return 2
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = [ex.submit(run_one, t) for t in tasks]
            for fut in concurrent.futures.as_completed(futures):
                ok, reason = fut.result()
                if not ok:
                    log(f"[error] translation stopped: {reason}")
                    return 2

    log(f"[ok] all translations finished successfully. output={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
