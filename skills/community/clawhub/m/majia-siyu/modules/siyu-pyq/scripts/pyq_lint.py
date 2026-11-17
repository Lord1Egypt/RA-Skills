#!/usr/bin/env python3
"""朋友圈文案合规前置扫描。

复用专家团合规词库（单一真源 src/siyu_team/eval/compliance_lexicon.py）——这就是把"合规官"
从事后评审节点，变成生成前的内嵌函数（边写边合规）。

只查朋友圈相关的合规项（COMPLIANCE_RED / ABSOLUTE_CLAIM），过滤掉给"方案质量门"
用的 NO_METRIC / NO_CALIBRATION 等不适用项。

用法:
    echo "文案" | python3 pyq_lint.py -
    python3 pyq_lint.py 文案.txt
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
        print("用法: pyq_lint.py <文件|->   （- 表示从 stdin 读）")
        sys.exit(2)
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()

    result = scan(text, mode=ScanMode.CUSTOMER_COPY)
    hits = [d for d in result["details"] if d["flag"] in RELEVANT]
    if not hits:
        print("✅ 合规前置扫描通过（无封号红线 / 绝对化用词）")
        sys.exit(0)

    hard = any(d["hard"] for d in hits)
    print("⚠️ 命中：", ", ".join(d["flag"] for d in hits))
    for d in hits:
        tag = "  ← 封号红线，必须就地改写" if d["hard"] else "  ← 广告法风险，建议改写"
        print(f"  - {d['flag']}: {d['desc']}{tag}")
    print("改写方向见 references/合规前置扫描.md，改完再发。")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
