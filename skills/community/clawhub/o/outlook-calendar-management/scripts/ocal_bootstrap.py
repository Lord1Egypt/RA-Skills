"""ocal_bootstrap — 首次运行依赖自检与自动安装（requests/msal/tzdata）。

必须在导入任何依赖第三方库的模块（ocal_graph → requests）之前调用；
自身只依赖 stdlib，保证缺依赖时它还能先跑起来。
tzdata 是 Windows 时区解析的关键：没有它 ZoneInfo 解析不了 "China Standard Time"
这类 Windows 时区名，会静默回退 UTC，日程时间就偏了——所以它也在自动安装之列。
"""
import importlib.util
import subprocess
import sys

from ocal_i18n import t

# 依赖清单：requests（Graph 调用）/ msal（认证续期）/ tzdata（Windows 时区数据）
REQUIRED = ("requests", "msal", "tzdata")


def harden_stdio():
    """输出重定向到 GBK 等窄编码管道时（Windows cmd/管道常见），emoji 会抛
    UnicodeEncodeError 直接崩；改成 replace 让它们退化成 ? 而不是崩溃。
    UTF-8 终端与 --json 输出不受影响。仅用 stdlib，不依赖第三方库。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass  # Python < 3.7 或非文本流：保持原样


def _missing():
    """看当前环境缺哪些依赖。

    :return: 缺失的包名列表；全齐就是空列表
    """
    return [pkg for pkg in REQUIRED if importlib.util.find_spec(pkg) is None]


def ensure_deps():
    """检查依赖，缺了就自动 pip 装；装不了给出手动命令并退出（exit 1）。"""
    missing = _missing()
    if not missing:
        return
    pkgs = " ".join(missing)
    print(t("deps_missing", pkgs=pkgs), file=sys.stderr)
    print(t("deps_installing"), file=sys.stderr)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", *missing],
            capture_output=True, text=True, timeout=300,
        )
    except Exception as e:
        print(t("deps_fail", e=e), file=sys.stderr)
        print(t("deps_manual", cmd=f"{sys.executable} -m pip install {pkgs}"), file=sys.stderr)
        sys.exit(1)
    if proc.returncode != 0:
        if proc.stderr:
            print(proc.stderr.strip()[-2000:], file=sys.stderr)
        print(t("deps_fail_code", code=proc.returncode), file=sys.stderr)
        print(t("deps_manual", cmd=f"{sys.executable} -m pip install {pkgs}"), file=sys.stderr)
        sys.exit(1)
    still = _missing()
    if still:
        print(t("deps_still_missing", pkgs=", ".join(still)), file=sys.stderr)
        sys.exit(1)
    print(t("deps_done", pkgs=pkgs), file=sys.stderr)
