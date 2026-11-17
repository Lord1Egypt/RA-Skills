#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensure the runtime dependencies of huawei-cloud-obs-list-pdf are installed.

Checks every required import and installs whatever is missing via pip (the
install mirrors the storage-query ``install_dependencies`` pattern: prefer a
fast domestic mirror, fall back to the official index, both with a timeout).
Nothing is installed when it is already importable.

Required packages:
    - reportlab (preferred PDF backend) OR fpdf2 (fallback PDF backend)
    - huaweicloudsdkcore             (SDK fallback bootstrap)
    - huaweicloudsdkobs              (SDK fallback)

Usage:
    python3 scripts/ensure_env.py [--upgrade]
"""

import argparse
import importlib
import sys

# Plain required package -> importable module.
REQUIRED_MODULES = [
    ("huaweicloudsdkcore", "huaweicloudsdkcore"),
    ("huaweicloudsdkobs", "huaweicloudsdkobs"),
]

# PDF backends: at least one must be importable. Ordered by preference.
PDF_BACKENDS = [
    ("reportlab", "reportlab"),
    ("fpdf2", "fpdf"),
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


def run_cmd(cmd, timeout=300):
    import subprocess

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


def ensure_env(upgrade=False):
    info("\nchecking python deps for huawei-cloud-obs-list-pdf ...")

    # 1) PDF backend: at least one of reportlab / fpdf2.
    have_backend = [pkg for pkg, mod in PDF_BACKENDS if check_import(mod)]
    if have_backend and not upgrade:
        for pkg in have_backend:
            ok("already importable: %s" % pkg)
    else:
        missing_pdf = [pkg for pkg, mod in PDF_BACKENDS if not check_import(mod)]
        info("installing PDF backend(s): %s" % ", ".join(missing_pdf))
        # Prefer reportlab alone; fpdf2 is only a fallback.
        install_target = ["reportlab"] if "reportlab" in missing_pdf else missing_pdf
        if not pip_install(install_target, upgrade=upgrade):
            return fail("PDF 依赖安装失败，请检查网络后重试（或手动 pip install "
                        "reportlab）")
        if not any(check_import(mod) for _pkg, mod in PDF_BACKENDS):
            return fail("安装后仍无可用 PDF 后端（reportlab / fpdf2）。")
        for pkg, mod in PDF_BACKENDS:
            if check_import(mod):
                ok("pdf backend ready: %s" % pkg)

    # 2) SDK fallback modules.
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

    if not any(check_import(mod) for _pkg, mod in PDF_BACKENDS):
        return fail("没有可用的 PDF 后端（reportlab / fpdf2），无法生成 PDF。")
    ok("PDF backend ready")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="检查并自动安装 huawei-cloud-obs-list-pdf 运行依赖。")
    parser.add_argument("--upgrade", action="store_true",
                        help="强制升级依赖到最新版本")
    args = parser.parse_args(argv)
    if ensure_env(upgrade=args.upgrade):
        info("\n环境就绪，可运行 scripts/list_obs_buckets_pdf.py。")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())