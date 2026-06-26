from __future__ import annotations

import re
import subprocess


def read_keychain_secret(service: str) -> tuple[str, str]:
    raw = subprocess.check_output(
        ["security", "find-generic-password", "-s", service],
        stderr=subprocess.STDOUT,
        text=True,
    )
    match = re.search(r'"acct"<blob>="([^"]+)"', raw)
    account = match.group(1) if match else ""
    password = subprocess.check_output(
        ["security", "find-generic-password", "-s", service, "-w"],
        text=True,
    ).strip()
    if not account:
        raise RuntimeError(f"Keychain item {service!r} does not expose an account name")
    return account, password
