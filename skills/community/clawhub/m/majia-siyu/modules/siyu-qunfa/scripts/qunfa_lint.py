#!/usr/bin/env python3
"""社群群发合规前置扫描。

复用专家团合规词库（单一真源 src/siyu_team/eval/compliance_lexicon.py），并重点扫描
群发特有的社交裂变门槛——转发得赠、集赞、拉人进群都是企微封号高发动作。

用法:
    echo "群发文案" | python3 qunfa_lint.py -
    python3 qunfa_lint.py 文案.txt
退出码: 0=通过, 1=命中封号红线(必改), 2=用法/环境错误。
"""
import pathlib
import sys

# 源码态从 repo/src 导入；SkillHub 独立安装态从包内 tools 导入。
SCRIPT = pathlib.Path(__file__).resolve()
for candidate in (SCRIPT.parents[5] / "src", SCRIPT.parents[3] / "tools"):
    if candidate.is_dir():
        sys.path.insert(0, str(candidate))

try:
    from siyu_team.eval.models import ScanMode
    from siyu_team.eval.static import scan
except ImportError as exc:
    print(
        "❌ 找不到统一合规扫描器；请从仓库根或完整 SkillHub 包运行："
        f"{exc}",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc

RELEVANT = {
    "COMPLIANCE_RED",
    "ABSOLUTE_CLAIM",
    "INDUCE_SHARE",
    "PRIVACY_COLLECT",
    "ATTRIBUTED_CLAIM",
    "QUOTED_RISK_MENTION",
    "RISK_TERM_MENTION",
}

def main() -> None:
    if len(sys.argv) < 2:
        print("用法: qunfa_lint.py <文件|->   （- 表示从 stdin 读）")
        sys.exit(2)
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()

    hits = [
        detail
        for detail in scan(
            text, mode=ScanMode.CUSTOMER_COPY
        )["details"]
        if detail["flag"] in RELEVANT
    ]

    if not hits:
        print("✅ 群发合规前置扫描通过（无封号红线 / 裂变门槛）")
        sys.exit(0)

    hard = any(d["hard"] for d in hits)
    flags = [d["flag"] for d in hits]
    print("⚠️ 命中：", ", ".join(flags))
    for d in hits:
        tag = "  ← 封号红线，必须改写" if d["hard"] else "  ← 广告法风险，建议改写"
        print(f"  - {d['flag']}: {d['desc']}{tag}")
    print("改写方向见 references/合规前置扫描.md，改完再发。")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
