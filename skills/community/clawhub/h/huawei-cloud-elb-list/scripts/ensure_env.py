#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensure the runtime dependencies of huawei-cloud-elb-list are installed.

list_elb.py itself only needs the Python standard library, but its SDK fallback
path (used when the KooCLI `hcloud` binary is absent) imports the official
Huawei Cloud SDK. This self-heal script checks every required import and
installs whatever is missing via pip (prefer a fast domestic mirror, fall back
to the official index, both with a timeout). Nothing is installed when it is
already importable.

Required packages:
    - huaweicloudsdkcore             (SDK bootstrap: credentials / region / http)
    - huaweicloudsdkelb              (ELB v3 SDK: ELBClient.list_load_balancers)

Usage:
    python3 scripts/ensure_env.py [--upgrade]
"""

import argparse
import importlib
import subprocess
import sys

REQUIRED_MODULES = [
    ("huaweicloudsdkcore", "huaweicloudsdkcore"),
    ("huaweicloudsdkelb", "huaweicloudsdkelb"),
]

PIP_TIMEOUT = "60"


def fail(msg):
    sys.stderr.write("\n[error] %s\n" % msg)
    return False


def ok(msg):
    print("  [ok] %s" % msg)


def info(msg):
    print(msg)


def check_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


def run_cmd(cmd, timeout=300):
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=timeout, universal_newlines=True,
        )
    except subprocess.TimeoutExpired:
        sys.stderr.write("[error] 命令执行超时：%s\n" % " ".join(cmd))
        return 1
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-400:])
    return proc.returncode


def pip_install(packages, upgrade=False):
    cmd = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check"]
    if upgrade:
        cmd.append("--upgrade")
    cmd.extend(packages)
    mirrors = [
        "https://pypi.tuna.tsinghua.edu.cn/simple",
        "https://mirrors.aliyun.com/pypi/simple/",
    ]
    for mirror in mirrors:
        host = mirror.split("//")[1].split("/")[0]
        info("  尝试镜像源 %s ..." % host)
        rc = run_cmd(cmd + ["-i", mirror, "--trusted-host", host,
                            "--timeout", PIP_TIMEOUT, "--retries", "2"])
        if rc == 0:
            return True
    info("  镜像源不可用，尝试官方源 ...")
    return run_cmd(cmd + ["--timeout", PIP_TIMEOUT, "--retries", "2"]) == 0


def ensure_env(upgrade=False):
    info("\nchecking python deps for huawei-cloud-elb-list ...")
    missing = []
    for module_name, _pkg in REQUIRED_MODULES:
        if check_import(module_name) and not upgrade:
            ok("already importable: %s" % module_name)
        else:
            missing.append(module_name)
    if missing:
        info("installing missing packages: %s" % ", ".join(missing))
        if not pip_install(missing, upgrade=upgrade):
            return fail("依赖安装失败，请检查网络后重试（或手动 pip install %s）"
                        % " ".join(missing))
        bad = [m for m in missing if not check_import(m)]
        if bad:
            return fail("安装后仍无法导入：%s" % ", ".join(bad))
        for name in missing:
            ok("installed: %s" % name)
    if not check_import("huaweicloudsdkcore"):
        return fail("huaweicloudsdkcore 不可用，SDK 回退路径不可用。")
    ok("SDK fallback dependencies ready")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="检查并自动安装 huawei-cloud-elb-list 运行依赖（SDK 回退路径）。")
    parser.add_argument("--upgrade", action="store_true",
                        help="强制升级依赖到最新版本")
    args = parser.parse_args(argv)
    if ensure_env(upgrade=args.upgrade):
        info("\n环境就绪，可运行 scripts/list_elb.py。")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())