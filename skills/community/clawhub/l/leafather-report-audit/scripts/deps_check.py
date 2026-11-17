#!/usr/bin/env python3
"""deps_check.py — 依赖自检：把"裸 traceback"换成"看得懂的一句话 + 该敲的命令"。

为什么单独一个文件：
    最难受的失败不是算错，是**装不上/跑不起来却说不清原因**。
    实测两类真实场景：
      1. 环境里根本没有 duckdb → `ModuleNotFoundError: No module named 'duckdb'`
      2. 企业终端的应用程序控制策略把 duckdb 的原生 DLL 拦了 →
         `ImportError: DLL load failed while importing duckdb: 应用程序控制策略已阻止此文件`
    这两种的解法完全不同（一个装包，一个加白名单或换接法），但裸报错长得像，用户没法判断。

本模块只依赖标准库，任何入口都可以安全 import。
"""
from __future__ import annotations

import importlib
import sys

# (import 名, pip 名, 缺了会怎样)
CORE = [
    ("duckdb", "duckdb", "本地复算与 SQL 录像"),
    ("yaml", "pyyaml", "policy.yaml / metrics.yaml 解析"),
]
OPTIONAL = [
    ("docx", "python-docx", "docx 报告"),
    ("pptx", "python-pptx", "pptx 报告"),
    ("openpyxl", "openpyxl", "xlsx 报告"),
    ("bs4", "beautifulsoup4", "html 报告"),
]

_DLL_HINTS = ("DLL load failed", "应用程序控制策略", "WinError 126", "WinError 193",
              "The specified module could not be found")


def _try(module_name: str):
    """尝试导入。返回 (ok, error_message)。"""
    try:
        importlib.import_module(module_name)
        return True, ""
    except ModuleNotFoundError as e:
        return False, f"ModuleNotFoundError: {e}"
    except ImportError as e:
        return False, f"ImportError: {e}"
    except Exception as e:  # noqa: BLE001  某些环境下会抛 OSError
        return False, f"{type(e).__name__}: {e}"


def is_dll_blocked(err: str) -> bool:
    """判断失败是不是"原生 DLL 被系统/安全软件拦住"，而不是"没装"。"""
    return any(h.lower() in (err or "").lower() for h in _DLL_HINTS)


def pip_cmd(pkgs: list[str]) -> str:
    """给出适用于当前环境的安装命令（Windows 上 python3 往往不存在）。"""
    exe = "python" if sys.platform.startswith("win") else "python3"
    return f"{exe} -m pip install {' '.join(pkgs)}"


def scan() -> dict:
    """返回 {'core_missing': [(import名,pip名,用途,错误)], 'optional_missing': [...], 'dll_blocked': bool}"""
    core_missing, opt_missing = [], []
    dll_blocked = False
    for mod, pip_name, purpose in CORE:
        ok, err = _try(mod)
        if not ok:
            if is_dll_blocked(err):
                dll_blocked = True
            core_missing.append((mod, pip_name, purpose, err))
    for mod, pip_name, purpose in OPTIONAL:
        ok, err = _try(mod)
        if not ok:
            opt_missing.append((mod, pip_name, purpose, err))
    return {"core_missing": core_missing, "optional_missing": opt_missing,
            "dll_blocked": dll_blocked}


def duckdb_or_hint():
    """要真用 duckdb 时调它：成功返回模块，失败打印可操作的指引后 SystemExit(2)。

    比裸 import 多做三件事：说清是"没装"还是"被拦截"、给出确切的安装命令、
    并告诉你在装不上时还能怎么用（--command 接法，SQL 进 CSV 出）。
    """
    try:
        import duckdb  # noqa: PLC0415
        return duckdb
    except ImportError as e:
        msg = str(e)
        print("❌ 未就绪：本地复算需要 duckdb，但导入失败。", file=sys.stderr)
        if is_dll_blocked(msg):
            print("   看起来不是没装，而是原生 DLL 被拦了（企业终端管理/应用程序控制策略）：", file=sys.stderr)
            print(f"   原始错误：{msg}", file=sys.stderr)
            print("   两条路，任选一条：", file=sys.stderr)
            print("   ① 把 Python 的 site-packages 下 duckdb 目录加入安全软件/应用控制白名单，然后重试；", file=sys.stderr)
            print("   ② 不用 duckdb 也能审：复算走 --command 接法"
                  "（你的脚本从 stdin 读 SQL、向 stdout 写 CSV），录像走 sqlite3 / pandas。", file=sys.stderr)
            print("      例：python3 scripts/rla_audit.py --ledger ledger.json --files report.md \\", file=sys.stderr)
            print("            --command \"python3 my_query.py\"", file=sys.stderr)
        else:
            print(f"   原始错误：{msg}", file=sys.stderr)
            print(f"   安装：{pip_cmd(['duckdb'])}", file=sys.stderr)
            print("   （Windows 上若 python3 不存在，用上面这条；macOS/Linux 也可写成 python3 -m pip install duckdb）",
                  file=sys.stderr)
            print("   不想装也行：复算走 --command 接法（SQL 从 stdin 进、CSV 从 stdout 出）。", file=sys.stderr)
        raise SystemExit(2)


def banner(allow_degrade: bool = False) -> str:
    """主入口开头调它，做一次体检并打印。

    返回运行模式：'full'（duckdb 可用）或 'degraded'（没有 duckdb，走降级/--command）。
    缺核心依赖且不允许降级 → 打印指引后 SystemExit(2)。
    """
    res = scan()
    missing_core = res["core_missing"]
    mode = "full"

    # pyyaml 没有替代品（策略文件就是 YAML），缺了直接停
    yaml_missing = [m for m in missing_core if m[1] == "pyyaml"]
    duck_missing = [m for m in missing_core if m[1] == "duckdb"]

    if duck_missing:
        err = duck_missing[0][3]
        if is_dll_blocked(err):
            print("[依赖] duckdb 已安装但原生 DLL 被安全策略拦截（不是没装）。"
                  "把 site-packages 下的 duckdb 目录加白即可恢复完整功能。", file=sys.stderr)
        else:
            print(f"[依赖] 没装 duckdb。安装：{pip_cmd(['duckdb'])}", file=sys.stderr)
        if allow_degrade:
            mode = "degraded"
            print("[依赖] 本次走降级模式（sqlite3 造数 + --command 复算），功能验证不受影响。",
                  file=sys.stderr)
        else:
            duckdb_or_hint()          # 内部会打印完整指引并退出(2)

    if yaml_missing:
        print("❌ 未就绪：缺 pyyaml（policy.yaml / metrics.yaml 靠它解析）。", file=sys.stderr)
        print(f"   安装：{pip_cmd(['pyyaml'])}", file=sys.stderr)
        raise SystemExit(2)

    if res["optional_missing"]:
        names = "、".join(f"{p}（{u}）" for _, p, u, _ in res["optional_missing"])
        print(f"[依赖] 可选包缺：{names} —— 只是少支持这几种格式，md/txt 不受影响。", file=sys.stderr)

    return mode


def main() -> int:
    res = scan()
    print("核心依赖：")
    for mod, pip_name, purpose, err in res["core_missing"]:
        tag = "（DLL 被拦截）" if is_dll_blocked(err) else ""
        print(f"  ❌ {pip_name} —— 缺它无法{purpose}{tag}")
    if not res["core_missing"]:
        print("  ✅ 齐全（duckdb、pyyaml）")
    print("可选依赖：")
    for mod, pip_name, purpose, _ in res["optional_missing"]:
        print(f"  ⚠️ {pip_name} —— 缺它无法读{purpose}")
    if not res["optional_missing"]:
        print("  ✅ 齐全（docx / pptx / xlsx / html 全支持）")
    if res["core_missing"]:
        print()
        print("安装命令：", pip_cmd([m[1] for m in res["core_missing"]]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
