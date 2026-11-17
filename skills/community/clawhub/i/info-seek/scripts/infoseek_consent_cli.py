#!/usr/bin/env python3
"""
scripts/infoseek_consent_cli.py — 能力授权 / 撤销 / 状态端到端 CLI（v2.1.0）

闭合 ROADMAP P1#3「能力注册表授权 UX」的代码侧：Maigret/Sherlock/manual_review
等 default_off 能力此前仅有函数级 grant_consent，缺少用户可见的授权入口。

授权模型（与现有机制一致，不破坏零依赖/合规哲学）：
  - enabled（声明启用）：经 env 覆盖 INFOSEEK_ENABLE_<NAME>（registry.yaml 保持只读，
    不在运行时改写发布清单）。
  - consent（涉个人数据的显式授权）：grant_consent 为进程级；本 CLI 通过生成
    `export` 引导行，让调用 shell 在同一会话内持有 env 与 consent 标记。
  - 所有 grant/revoke 均写 ~/.infoseek/consent.log 审计（复用 registry 落盘）。

子命令：
  list [--kind K]                 列出能力 + enabled/consent/effective/边界
  grant NAME... [--kind-check]    授权（校验能力存在 + 打印 export 引导）
  revoke NAME...                  撤销授权
  shell-init                      打印可 eval 的 export 行（批量启用已授权能力）
  doctor                          授权 UX 自检（默认 OFF 能力、CLI 安装情况）

设计：本 CLI 只做「引导 + 审计 + 状态」，不真正长期存储凭证；真实长驻授权由
用户把 export 行写入自己的 shell profile（doctor 会给出指引）。
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# 路径引导（scripts/ 与仓库根）
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
for p in (str(_HERE), str(_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from core import capability_registry as cr  # noqa: E402


def _env_name(name: str) -> str:
    cap = cr.get_capability(name) or {}
    return cap.get("env_var") or f"INFOSEEK_ENABLE_{name.upper()}"


def _cli_installed(name: str) -> str:
    """探测能力所需 CLI 是否在 PATH（仅 identity 类有 CLI）。"""
    cli_map = {"Maigret": "maigret", "Sherlock": "sherlock"}
    cli = cli_map.get(name)
    if not cli:
        return "-"
    return "yes" if shutil.which(cli) else "no"


def cmd_list(args) -> int:
    caps = cr.list_capabilities(kind=args.kind)
    if not caps:
        print(f"(无 kind={args.kind} 的能力)")
        return 0
    header = f"{'能力':<22}{'kind':<22}{'enabled':>8}{'consent':>9}{'effective':>10}{'CLI':>5}"
    print(header)
    print("-" * len(header))
    for c in caps:
        name = c.get("name", "")
        en = cr.is_enabled(name)
        cg = cr.consent_granted(name) if c.get("requires_consent") else True
        eff = cr.is_effective_enabled(name)
        print(f"{name:<22}{c.get('kind',''):<22}"
              f"{('yes' if en else 'no'):>8}{('yes' if cg else '-'):>9}"
              f"{('YES' if eff else 'no'):>10}{_cli_installed(name):>5}")
    print("\nenabled=env/声明启用 · consent=已授权 · effective=最终可用(交集)")
    return 0


def _validate(names) -> list:
    missing = [n for n in names if not cr.get_capability(n)]
    if missing:
        print(f"错误：未知能力 {missing}；用 `list` 查看可用能力。", file=sys.stderr)
    return missing


def cmd_grant(args) -> int:
    if _validate(args.names):
        return 2
    lines = []
    for name in args.names:
        cr.grant_consent(name)                 # 写审计 + 进程态
        env = _env_name(name)
        lines.append(f'export {env}=1')
        print(f"[grant] {name} 已授权（审计已写 {cr.consent_log_path()}）")
        if cr.requires_consent(name):
            print(f"        {name} 涉个人数据，须在同会话持有授权；下方 export 行已就绪。")
    print("\n# 在当前 shell 启用（eval 本输出）：")
    for ln in lines:
        print(ln)
    print("# 长期生效请把上述 export 行追加到 ~/.bashrc / ~/.zshrc")
    return 0


def cmd_revoke(args) -> int:
    if _validate(args.names):
        return 2
    for name in args.names:
        cr.revoke_consent(name)
        env = _env_name(name)
        print(f"[revoke] {name} 已撤销授权（审计已记录）；如曾 export 请执行：unset {env}")
    print("\n# 在当前 shell 立即禁用（eval 本输出）：")
    for name in args.names:
        print(f"unset {_env_name(name)}")
    return 0


def cmd_shell_init(args) -> int:
    """打印所有「需授权且已在持久授权清单」能力的 export 行。

    进程级 consent 无法跨进程，故 shell-init 依据 env INFOSEEK_CONSENT_CAPS
    （逗号分隔的能力名，由用户 profile 持久持有）决定启用哪些，并在输出里
    同时导出它，供子进程 grant 使用。
    """
    granted = [c for c in cr.list_capabilities()
               if c.get("requires_consent") and os.environ.get("INFOSEEK_ENABLE_" + c["name"].upper())]
    names = [c["name"] for c in granted]
    print("# eval $(python3 infoseek_consent_cli.py shell-init)")
    for name in names:
        print(f"export {_env_name(name)}=1")
    if names:
        cur = os.environ.get("INFOSEEK_CONSENT_CAPS", "")
        merged = sorted(set(cur.split(",")) | set(names))
        print(f"export INFOSEEK_CONSENT_CAPS={','.join(x for x in merged if x)}")
    return 0


def cmd_doctor(args) -> int:
    print("== infoseek 能力授权 UX 自检 ==\n")
    off = [c for c in cr.list_capabilities() if not c.get("enabled", False)]
    print(f"默认 OFF 能力（{len(off)}）：")
    for c in off:
        print(f"  - {c['name']:<22} ({c.get('kind')})  CLI={_cli_installed(c['name'])}")
    print("\n授权步骤（以 Maigret 为例）：")
    print("  1) export INFOSEEK_ENABLE_MAIGRET=1")
    print("  2) 运行期 grant_consent('Maigret') 或经 MCP 工具传 consent=true")
    print("  3) 身份归因总闸：export INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION=1")
    print("  4) CLI 安装：pip install maigret（建议隔离 venv，设 INFOSEEK_MAIGRET_VENV）")
    print(f"\n审计日志：{cr.consent_log_path()}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="infoseek_consent_cli",
        description="infoseek 能力授权 / 撤销 / 状态端到端 CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="列出能力及启用/授权/生效状态")
    p_list.add_argument("--kind", default=None)
    p_list.set_defaults(func=cmd_list)

    p_grant = sub.add_parser("grant", help="授权一个或多个能力")
    p_grant.add_argument("names", nargs="+")
    p_grant.set_defaults(func=cmd_grant)

    p_revoke = sub.add_parser("revoke", help="撤销授权")
    p_revoke.add_argument("names", nargs="+")
    p_revoke.set_defaults(func=cmd_revoke)

    p_init = sub.add_parser("shell-init", help="打印 export 引导行（供 eval）")
    p_init.set_defaults(func=cmd_shell_init)

    p_doc = sub.add_parser("doctor", help="授权 UX 自检与步骤指引")
    p_doc.set_defaults(func=cmd_doctor)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
