#!/usr/bin/env python3
"""破冰欢迎/答疑话术合规前置扫描。

复用专家团合规词库（单一真源 src/siyu_team/eval/compliance_lexicon.py），并在其上额外检测：
- 社交裂变门槛（欢迎语里也不能有）
- 首句索取敏感信息（手机号/身份证/定位 未经授权口径直接索取）

用法:
    echo "话术" | python3 huashu_lint.py -
    python3 huashu_lint.py 话术.txt
退出码: 0=通过(可能带软提示), 1=命中封号红线(必改), 2=用法/环境错误。
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
        print("用法: huashu_lint.py <文件|->   （- 表示从 stdin 读）")
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
        print("✅ 话术合规前置扫描通过（无红线 / 诱导 / 首句索取敏感信息）")
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
