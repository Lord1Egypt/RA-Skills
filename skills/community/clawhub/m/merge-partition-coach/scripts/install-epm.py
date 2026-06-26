#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


def parse_dest(args: list[str]) -> str:
    if not args:
        return "test"
    first = args[0]
    if "=" in first:
        key, value = first.split("=", 1)
        if key.lower() == "dest":
            return value or "test"
    return first


def download_installer(dest_arg: str, output_path: Path) -> bool:
    for host in ("d1", "d2", "d3"):
        if output_path.exists():
            output_path.unlink()
        print(f"Trying mirror {host}...")
        url = f"https://{host}.easeus.com/epm/free/epm_free_ob.exe?source=skills&dest={dest_arg}"
        try:
            with urllib.request.urlopen(url, timeout=60) as response, output_path.open("wb") as fh:
                fh.write(response.read())
            if output_path.exists():
                return True
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"[WARN] Mirror {host} failed: {exc}")
    return False


def main() -> int:
    dest_arg = parse_dest(sys.argv[1:])
    dest_dir = Path(tempfile.gettempdir()) / "EuUpdater_EPM"
    dest_path = dest_dir / "epm_free_setup.exe"
    dest_dir.mkdir(parents=True, exist_ok=True)

    print("[1/2] Downloading installer...")
    if not download_installer(dest_arg, dest_path):
        print("Download failed from all mirrors.")
        return 1

    if not dest_path.exists():
        print(f'Installer was not found: "{dest_path}"')
        return 1

    print("[2/2] Running silent install...")
    proc = subprocess.run(
        [
            str(dest_path),
            "/verysilent",
            "/suppressmsgboxes",
            "/norestart",
            "/log",
        ],
        check=False,
    )
    install_exit_code = int(proc.returncode)
    if install_exit_code != 0:
        print(f"Installer exited with code {install_exit_code}.")
    else:
        print("Installation completed.")
    return install_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
