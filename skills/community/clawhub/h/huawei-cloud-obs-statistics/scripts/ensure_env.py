#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensure the runtime dependencies of huawei-cloud-obs-statistics are installed.

The CLI path (hcloud / obsutil) needs no Python packages. The SDK fallback path
needs ``huaweicloudsdkcore`` and ``huaweicloudsdkobs``; this helper installs
whatever is missing via pip (prefer a fast domestic mirror, fall back to the
official index). Nothing is installed when it is already importable.

Usage:
    python3 scripts/ensure_env.py [--upgrade]
"""

import argparse
import importlib
import subprocess
import sys

REQUIRED_MODULES = [
    ("huaweicloudsdkcore", "huaweicloudsdkcore"),
    ("huaweicloudsdkobs", "huaweicloudsdkobs"),
]

PIP_TIMEOUT = "60"
MIRROR = "https://mirrors.huaweicloud.com/repository/pypi/simple"


def ok(msg):
    print("  [ok] %s" % msg)


def info(msg):
    print("[ensure_env] %s" % msg)


def fail(msg):
    sys.stderr.write("\n[error] %s\n" % msg)
    return False


def has_module(module):
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False


def pip_install(package, upgrade=False, index=None):
    cmd = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
           "--timeout", PIP_TIMEOUT]
    if upgrade:
        cmd.append("--upgrade")
    if index:
        cmd.extend(["-i", index])
    cmd.append(package)
    return subprocess.call(cmd) == 0


def ensure(upgrade=False):
    missing = [(pkg, mod) for pkg, mod in REQUIRED_MODULES if not has_module(mod)]
    if not missing:
        ok("huaweicloudsdkcore / huaweicloudsdkobs 已安装")
        return True
    ok_any = True
    for pkg, mod in missing:
        info("安装 %s …" % pkg)
        installed = pip_install(pkg, upgrade=upgrade, index=MIRROR) or \
            pip_install(pkg, upgrade=upgrade)
        if installed and has_module(mod):
            ok("%s 安装成功" % pkg)
        else:
            fail("%s 安装失败；请手动 pip install %s" % (pkg, pkg))
            ok_any = False
    return ok_any


def main():
    parser = argparse.ArgumentParser(description="Install OBS statistics SDK dependencies.")
    parser.add_argument("--upgrade", action="store_true", help="强制升级到最新版本")
    args = parser.parse_args()
    return 0 if ensure(upgrade=args.upgrade) else 1


if __name__ == "__main__":
    sys.exit(main())