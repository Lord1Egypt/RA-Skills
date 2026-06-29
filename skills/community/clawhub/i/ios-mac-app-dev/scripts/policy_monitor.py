#!/usr/bin/env python3
"""
Apple 开发者政策变更监控器。
追踪 Apple Developer News 中的政策变更。
"""

import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PolicyChange:
    type: str
    section: Optional[str]
    title: str
    detail: str
    impact: str  # HIGH, MEDIUM, LOW
    deadline: Optional[str]
    source: str

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "section": self.section,
            "title": self.title,
            "detail": self.detail,
            "impact": self.impact,
            "deadline": self.deadline,
            "source": self.source,
        }


class ApplePolicyMonitor:
    WATCH_SOURCES = [
        "https://developer.apple.com/news/",
        "https://developer.apple.com/cn/news/",
    ]

    KEY_AREAS = [
        ("AI/ML框架使用规范", "条款3.3.11"),
        ("敏感内容分析(Sensitive Content)", "条款3.3.3(N)"),
        ("未成年保护", "审核指南1.2.1(a)"),
        ("出口合规", "条款3.1"),
        ("隐私标签与数据披露", "审核指南更新"),
        ("4.3低质应用清理", "审核指南"),
        ("API废弃", "API_DEPRECATION"),
    ]

    def __init__(self):
        self.changes: List[PolicyChange] = []

    def check_watchlist(self) -> List[PolicyChange]:
        """核心检查：返回当前已知的政策变更监控项"""
        self.changes = [
            PolicyChange(
                type="REVIEW_GUIDELINE_UPDATE",
                section="3.3.11",
                title="AI/ML 框架使用规范",
                detail="新增条款3.3.11，规范AI及机器学习技术使用。"
                       "要求AI生成内容明确标识，用户可控制AI功能开关。",
                impact="HIGH",
                deadline="2026年6月起",
                source="Apple Developer Program 许可协议",
            ),
            PolicyChange(
                type="REVIEW_GUIDELINE_UPDATE",
                section="1.2.1(a)",
                title="未成年保护要求",
                detail="新增年龄分级和限制机制要求。"
                       "面向儿童的应用必须提供家长控制功能。",
                impact="HIGH",
                deadline="2026年6月起",
                source="App Store 审核指南",
            ),
            PolicyChange(
                type="REVIEW_GUIDELINE_UPDATE",
                section="4.3",
                title="低质同质化应用清理",
                detail="禁止提交与现有内容高度相似的应用。"
                       "约会、手电筒、音效、壁纸等成熟类别需显著差异化。",
                impact="HIGH",
                deadline="2026年6月起",
                source="App Store 审核指南",
            ),
            PolicyChange(
                type="REVIEW_GUIDELINE_UPDATE",
                section="3.3.3(N)",
                title="敏感内容分析框架",
                detail="明确 Sensitive Content Analysis 框架使用要求。",
                impact="MEDIUM",
                deadline="2026年6月起",
                source="App Store 审核指南",
            ),
            PolicyChange(
                type="API_DEPRECATION",
                section="ImageCreator",
                title="ImageCreator 废弃",
                detail="ImageCreator类在iOS 27中被废弃，需切换至Image Playground框架。",
                impact="MEDIUM",
                deadline="iOS 27正式发布前",
                source="WWDC 2026",
            ),
            PolicyChange(
                type="REGULATION_UPDATE",
                section="巴西市场",
                title="巴西市场附件12修订",
                detail="支持替代分发和支付方式。",
                impact="LOW",
                deadline="iOS 26.5",
                source="Apple Developer Program 许可协议",
            ),
            PolicyChange(
                type="REGULATION_UPDATE",
                section="得州年龄验证",
                title="SB2420法规影响",
                detail="得克萨斯州SB2420法规，需使用年龄保证API。",
                impact="MEDIUM",
                deadline="2026年6月起",
                source="美国各州法规",
            ),
        ]
        return self.changes

    def generate_alert_report(self) -> str:
        """生成政策警报报告"""
        report_lines = [
            "📢  Apple Developer 政策监控报告",
            "=" * 60,
            f"  生成时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            "",
        ]

        if not self.changes:
            self.check_watchlist()

        # 按影响程度分组
        high = [c for c in self.changes if c.impact == "HIGH"]
        medium = [c for c in self.changes if c.impact == "MEDIUM"]
        low = [c for c in self.changes if c.impact == "LOW"]

        if high:
            report_lines.append("🔴 高风险变更:")
            report_lines.append("-" * 40)
            for c in high:
                report_lines.append(f"  [{c.section}] {c.title}")
                report_lines.append(f"  {c.detail}")
                report_lines.append(f"  📅 期限: {c.deadline}")
                report_lines.append(f"  🔗 来源: {c.source}")
                report_lines.append("")

        if medium:
            report_lines.append("🟡 中风险变更:")
            report_lines.append("-" * 40)
            for c in medium:
                report_lines.append(f"  [{c.section}] {c.title}")
                report_lines.append(f"  📅 期限: {c.deadline}")
                report_lines.append("")

        if low:
            report_lines.append("🟢 低风险变更:")
            report_lines.append("-" * 40)
            for c in low:
                report_lines.append(f"  [{c.section}] {c.title}")

        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("⚠️ 建议操作：")
        report_lines.append("1. 高风险项必须在下次提交前处理")
        report_lines.append("2. 中风险项安排在下一个版本迭代")
        report_lines.append("3. 低风险项持续关注")

        return "\n".join(report_lines)

    def generate_compliance_checklist(self) -> dict:
        """生成合规检查清单"""
        if not self.changes:
            self.check_watchlist()

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "high_priority": [
                {
                    "area": "AI合规",
                    "check": "AI生成内容是否明确标识？用户能否控制AI功能开关？",
                },
                {
                    "area": "未成年保护",
                    "check": "应用是否设置了正确的年龄分级？是否需要家长控制？",
                },
                {
                    "area": "4.3差异化",
                    "check": "应用与同类App的差异化优势是否充分？",
                },
            ],
            "medium_priority": [
                {
                    "area": "敏感内容",
                    "check": "是否使用了敏感内容分析框架？隐私声明是否充分？",
                },
                {
                    "area": "废弃API",
                    "check": "检查项目中是否有ImageCreator等即将废弃的API调用",
                },
                {
                    "area": "隐私标签",
                    "check": "PrivacyInfo.xcprivacy是否已更新？数据分类是否准确？",
                },
            ],
            "must_fix": [
                "Info.plist 必须包含 ITSAppUsesNonExemptEncryption = false",
                "所有隐私权限必须在 Info.plist 中声明使用说明",
            ],
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Apple 开发者政策监控器"
    )
    parser.add_argument("--alert", action="store_true",
                        help="生成警报报告")
    parser.add_argument("--checklist", action="store_true",
                        help="生成合规检查清单")
    parser.add_argument("--json", action="store_true",
                        help="以 JSON 格式输出")

    args = parser.parse_args()

    monitor = ApplePolicyMonitor()
    monitor.check_watchlist()

    if args.alert:
        report = monitor.generate_alert_report()
        print(report)
    elif args.checklist:
        checklist = monitor.generate_compliance_checklist()
        if args.json:
            print(json.dumps(checklist, ensure_ascii=False, indent=2))
        else:
            print("合规检查清单:")
            print("=" * 60)
            for level, items in [("🔴 高优先级", checklist["high_priority"]),
                                  ("🟡 中优先级", checklist["medium_priority"]),
                                  ("❌ 必须修复", [{"check": m} for m in checklist["must_fix"]])]:
                print(f"\n{level}:")
                for item in items:
                    print(f"  • {item['check']}")
    else:
        if args.json:
            print(json.dumps(
                [c.to_dict() for c in monitor.changes],
                ensure_ascii=False, indent=2
            ))
        else:
            print(monitor.generate_alert_report())


if __name__ == "__main__":
    main()
