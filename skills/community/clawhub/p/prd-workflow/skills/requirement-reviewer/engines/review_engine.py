#!/usr/bin/env python3
"""
PRD 评审引擎 v3.0

支持插件式加载、场景模式和自动场景识别的 PRD 自动评审
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Optional

# 确保在当前目录
sys.path.insert(0, os.path.dirname(__file__))

# 导入插件管理器
from plugin_manager import PluginManager, SCENARIOS


# 场景识别规则
SCENARIO_RULES = {
    "financial": {
        "keywords": [
            "基金",
            "私募",
            "信托",
            "理财",
            "资管",
            "资产管理",
            "认购",
            "申购",
            "赎回",
            "份额",
            "净值",
            "托管",
            "合格投资者",
            "风险测评",
            "适当性",
            "冷静期",
            "R1",
            "R2",
            "R3",
            "R4",
            "R5",
            "保守型",
            "稳健型",
            "平衡型",
            "成长型",
            "进取型",
        ],
        "regex": [
            r"产品风险等级",
            r"客户风险等级",
            r"风险承受能力",
            r"申购费率",
            r"认购费率",
            r"赎回费率",
            r"管理费率",
            r"托管费率",
            r"合格投资者",
            r"适当性管理",
            r"冷静期",
            r"《.*》法",
            r"《.*》办法",
            r"《.*》指引",
            r"监管",
        ],
        "threshold": 3,  # 匹配 3 个以上关键词认为是金融场景
    },
    "internet": {
        "keywords": [
            "APP",
            "小程序",
            "H5",
            "Web",
            "SaaS",
            "平台",
            "用户注册",
            "登录",
            "密码",
            "验证码",
            "短信",
            "支付",
            "订单",
            "购物车",
            "商品",
            "物流",
            "接口",
            "API",
            "数据库",
            "服务器",
            "缓存",
            "前端",
            "后端",
            "移动端",
            "iOS",
            "Android",
        ],
        "regex": [
            r"DAU",
            r"MAU",
            r"UV",
            r"PV",
            r"QPS",
            r"TPS",
            r"UI",
            r"UX",
            r"用户体验",
            r"界面设计",
            r"原型",
        ],
        "threshold": 3,  # 匹配 3 个以上关键词认为是互联网场景
    },
}


class PRDReviewer:
    """PRD 评审引擎 v3.0 - 插件式架构"""

    def __init__(
        self,
        scenario: str = None,
        product_type: str = None,
        risk_level: str = "R3",
        custom_checkers: List[str] = None,
        auto_detect: bool = None,
    ):
        """
        初始化评审引擎

        参数:
            scenario: 场景模式 (default/financial/internet)，为 None 时自动识别
            product_type: 产品类型 (financial 场景专用)
            risk_level: 风险等级 (financial 场景专用)
            custom_checkers: 自定义评审器列表（优先级高于 scenario）
            auto_detect: 是否自动识别场景（默认：scenario 为 None 时开启）
        """
        self.product_type = product_type
        self.risk_level = risk_level

        # 场景识别：用户指定 > 自动识别 > 默认 default
        if scenario:
            self.scenario = scenario
            # 用户明确指定场景时，默认关闭自动识别
            self.auto_detect = auto_detect if auto_detect is not None else False
        elif auto_detect is not None:
            self.auto_detect = auto_detect
            self.scenario = "default"  # 初始值，review 时会被覆盖
        else:
            # scenario 为 None 且 auto_detect 未指定时，开启自动识别
            self.auto_detect = True
            self.scenario = "default"  # 初始值，review 时会被覆盖

        # 使用插件管理器加载评审器
        self.plugin_manager = PluginManager(
            base_path=__name__.replace(".review_engine", "")
        )

        if custom_checkers:
            # 自定义加载
            self.checkers = self.plugin_manager.load_custom(custom_checkers)
        else:
            # 按场景加载（初始可能加载 default，review 时会重新识别）
            self.checkers = self.plugin_manager.load_scenario(self.scenario)

        # 为部分评审器传递参数
        self._configure_checkers()

        # v2.6.3 新增：AI 语义评审器（独立于场景，所有 PRD 都检查）
        self.ai_checker = self._load_ai_semantic_checker()

    def detect_scenario(self, prd_content: str) -> str:
        """
        自动识别场景

        参数:
            prd_content: PRD 文档内容

        返回:
            识别的场景 (default/financial/internet)
        """
        scores = {"financial": 0, "internet": 0, "default": 0}

        # 检查金融场景
        financial_rules = SCENARIO_RULES["financial"]
        for keyword in financial_rules["keywords"]:
            if keyword in prd_content:
                scores["financial"] += 1
        for pattern in financial_rules["regex"]:
            if re.search(pattern, prd_content, re.IGNORECASE):
                scores["financial"] += 1

        # 检查互联网场景
        internet_rules = SCENARIO_RULES["internet"]
        for keyword in internet_rules["keywords"]:
            if keyword in prd_content:
                scores["internet"] += 1
        for pattern in internet_rules["regex"]:
            if re.search(pattern, prd_content, re.IGNORECASE):
                scores["internet"] += 1

        # 判断场景
        max_score = max(scores.values())
        if (
            max_score < financial_rules["threshold"]
            and max_score < internet_rules["threshold"]
        ):
            return "default"

        # 返回得分最高的场景
        return max(scores.keys(), key=lambda k: scores[k])

    def _configure_checkers(self) -> None:
        """为部分评审器传递参数"""
        # 为 compliance checker 传递参数
        if "compliance" in self.checkers:
            self.checkers["compliance"].product_type = self.product_type
            self.checkers["compliance"].risk_level = self.risk_level

    def _load_ai_semantic_checker(self):
        """加载 AI 语义评审器"""
        try:
            from core.ai_semantic_checker import AISemanticChecker

            return AISemanticChecker()
        except Exception as e:
            print(f"⚠️  AI 语义评审器加载失败：{e}")
            return None

    def review(
        self,
        prd_content: str,
        product_type: str = None,
        risk_level: str = "R3",
        auto_detect: bool = None,
    ) -> Dict:
        """
        评审 PRD

        参数:
            prd_content: PRD 文档内容
            product_type: 产品类型 (fund/private/trust/wealth)
            risk_level: 风险等级 (R1-R5)
            auto_detect: 是否自动识别场景（覆盖初始化时的设置）

        返回:
            {
                "timestamp": "2026-03-10 14:30",
                "overall_score": 85,
                "status": "pass",
                "check_results": {...},
                "issues": [...],
                "suggestions": [...]
            }
        """
        # 自动识别场景
        detect = auto_detect if auto_detect is not None else self.auto_detect
        if detect:
            detected = self.detect_scenario(prd_content)
            if detected != self.scenario:
                print(f"🔍 自动识别场景：{detected} (原场景：{self.scenario})")
                self.scenario = detected
                # 重新加载评审器
                self.checkers = self.plugin_manager.load_scenario(self.scenario)
                self._configure_checkers()
            else:
                print(f"🔍 场景确认：{self.scenario}")

        # 更新参数
        if product_type:
            self.product_type = product_type
            self._configure_checkers()

        results = {}
        all_issues = []

        # 执行各项检查
        for check_type, checker in self.checkers.items():
            print(f"🔍 执行{check_type}检查...")
            try:
                # 部分检查器支持额外参数
                if check_type == "risk":
                    result = checker.check(prd_content, risk_level=risk_level)
                elif check_type == "compliance":
                    result = checker.check(prd_content)
                else:
                    result = checker.check(prd_content)
                results[check_type] = result
                all_issues.extend(result.get("issues", []))
            except Exception as e:
                print(f"   ❌ {check_type}检查失败：{e}")
                results[check_type] = {"score": 0, "error": str(e)}

        # v2.6.3 新增：AI 语义评审
        if self.ai_checker:
            print("🔍 执行 AI 语义评审...")
            try:
                ai_result = self.ai_checker.check(prd_content)
                results["ai_semantic"] = ai_result
                all_issues.extend(ai_result.get("issues", []))
            except Exception as e:
                print(f"   ❌ AI 语义评审失败：{e}")
                results["ai_semantic"] = {"score": 0, "error": str(e)}

        # 计算总体得分
        overall_score = self.calculate_overall_score(results)

        # 确定状态
        if overall_score >= 80:
            status = "pass"
        elif overall_score >= 60:
            status = "warning"
        else:
            status = "fail"

        # 生成改进建议
        suggestions = self.generate_suggestions(all_issues)

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "overall_score": overall_score,
            "status": status,
            "check_results": results,
            "issues": all_issues,
            "suggestions": suggestions,
            "total_issues": len(all_issues),
            "critical_issues": len(
                [i for i in all_issues if i.get("severity") == "high"]
            ),
            "scenario": self.scenario,
            "loaded_checkers": list(self.checkers.keys()),
        }

    def calculate_overall_score(self, results: Dict) -> int:
        """计算总体得分"""
        if not results:
            return 0

        scores = [r.get("score", 0) for r in results.values()]
        return sum(scores) // len(scores)

    def generate_suggestions(self, issues: List[Dict]) -> List[Dict]:
        """生成改进建议"""
        suggestions = []

        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_issues = sorted(
            issues, key=lambda x: priority_order.get(x.get("severity", "low"), 2)
        )

        # 提取建议
        for issue in sorted_issues[:10]:  # 最多 10 条建议
            suggestions.append(
                {
                    "priority": issue.get("severity", "low"),
                    "title": issue.get("title", ""),
                    "suggestion": issue.get("suggestion", ""),
                }
            )

        return suggestions


class IterativeReviewer:
    """迭代评审控制器 v2.1 - 支持场景模式和自动识别"""

    def __init__(
        self,
        scenario: str = None,
        max_loops: int = 3,
        threshold: float = 0.05,
        auto_detect: bool = True,
    ):
        """
        初始化迭代评审器

        参数:
            scenario: 场景模式 (default/financial/internet)，为 None 时自动识别
            max_loops: 最大循环次数
            threshold: 增量阈值
            auto_detect: 是否自动识别场景
        """
        self.max_loops = max_loops
        self.threshold = threshold
        self.scenario = scenario
        self.auto_detect = auto_detect
        self.reviewer = PRDReviewer(scenario=scenario, auto_detect=auto_detect)

    def review_with_iteration(self, prd_content: str, improve_func=None) -> Dict:
        """
        带迭代优化的评审

        参数:
            prd_content: PRD 文档内容
            improve_func: 改进函数，接收问题和当前 PRD，返回改进后的 PRD

        返回:
            {
                "final_report": {...},
                "loop_count": 3,
                "exit_reason": "增量<5%",
                "improvement_history": [...]
            }
        """
        current_prd = prd_content
        prev_report = None
        improvement_history = []
        loop_count = 0

        print("🚀 开始迭代评审...")
        print(f"最大循环次数：{self.max_loops}")
        print(f"增量阈值：{self.threshold * 100}%")
        print()

        while True:
            loop_count += 1
            print(f"📊 第{loop_count}轮评审...")

            # 执行评审
            current_report = self.reviewer.review(current_prd)

            # 生成增量报告（第 2 轮开始）
            if prev_report:
                incremental = self.calculate_incremental(prev_report, current_report)
                improvement_history.append(incremental)

                print(f"   新增问题：{incremental['new_issues_count']}")
                print(f"   已修复：{incremental['fixed_issues_count']}")
                print(f"   增量百分比：{incremental['percentage']:.1f}%")

                # 检查退出条件
                should_exit, exit_reason = self.check_exit_condition(
                    incremental, loop_count, self.max_loops, self.threshold
                )

                if should_exit:
                    print(f"\n✅ 退出循环：{exit_reason}")
                    break

                # 执行改进（如果有改进函数）
                if improve_func and incremental["new_issues"]:
                    print(f"   执行改进...")
                    current_prd = improve_func(current_prd, incremental["new_issues"])
            else:
                print(f"   发现问题：{current_report['total_issues']}")
                print(f"   严重问题：{current_report['critical_issues']}")

                # 第 1 轮也执行改进
                if improve_func and current_report["issues"]:
                    print(f"   执行改进...")
                    current_prd = improve_func(current_prd, current_report["issues"])

            # 更新报告
            prev_report = current_report
            print()

        return {
            "final_report": current_report,
            "loop_count": loop_count,
            "exit_reason": exit_reason
            if "exit_reason" in locals()
            else "达到最大循环次数",
            "improvement_history": improvement_history,
            "total_improvements": len(improvement_history),
        }

    def calculate_incremental(self, prev_report: Dict, current_report: Dict) -> Dict:
        """计算增量内容"""
        # 提取问题 ID
        prev_issue_ids = set(
            [self.get_issue_id(i) for i in prev_report.get("issues", [])]
        )
        current_issue_ids = set(
            [self.get_issue_id(i) for i in current_report.get("issues", [])]
        )

        # 新增问题
        new_issue_ids = current_issue_ids - prev_issue_ids
        new_issues = [
            i
            for i in current_report.get("issues", [])
            if self.get_issue_id(i) in new_issue_ids
        ]

        # 已修复问题
        fixed_issue_ids = prev_issue_ids - current_issue_ids
        fixed_issues = [
            i
            for i in prev_report.get("issues", [])
            if self.get_issue_id(i) in fixed_issue_ids
        ]

        # 计算增量百分比
        prev_content_len = len(str(prev_report))
        current_content_len = len(str(current_report))
        incremental_content_len = len(str(new_issues))

        percentage = (
            (incremental_content_len / current_content_len * 100)
            if current_content_len > 0
            else 0
        )

        return {
            "percentage": percentage,
            "new_issues": new_issues,
            "new_issues_count": len(new_issues),
            "fixed_issues": fixed_issues,
            "fixed_issues_count": len(fixed_issues),
            "prev_content_len": prev_content_len,
            "current_content_len": current_content_len,
            "incremental_content_len": incremental_content_len,
        }

    def get_issue_id(self, issue: Dict) -> str:
        """生成问题唯一 ID"""
        return f"{issue.get('type', '')}-{issue.get('title', '')}"

    def check_exit_condition(
        self, incremental: Dict, loop_count: int, max_loops: int, threshold: float
    ) -> tuple:
        """检查是否退出循环"""
        # 条件 1: 达到最大循环次数
        if loop_count >= max_loops:
            return True, f"达到最大循环次数 ({max_loops}次)"

        # 条件 2: 增量 <= 阈值
        if incremental["percentage"] <= threshold * 100:
            return (
                True,
                f"增量内容低于阈值 ({incremental['percentage']:.1f}% <= {threshold * 100}%)",
            )

        # 条件 3: 没有新的严重问题
        critical_new = [
            i for i in incremental["new_issues"] if i.get("severity") == "high"
        ]
        if len(critical_new) == 0 and incremental["new_issues_count"] <= 2:
            return True, "没有新的严重问题"

        return False, "继续优化"


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD

    ## 产品概述
    产品风险等级：R3

    ## 功能设计
    功能 1: 用户注册
    功能 2: 养老测算

    ## 验收标准
    用例 1: 用户注册
    """

    print("=" * 60)
    print("PRD 评审引擎 v3.0 - 场景模式测试")
    print("=" * 60)

    # 测试 default 场景
    print("\n【测试 1】Default 场景（通用）")
    reviewer_default = PRDReviewer(scenario="default")
    result_default = reviewer_default.review(test_prd)

    print(f"\n评审结果:")
    print(f"  场景：{result_default['scenario']}")
    print(f"  加载评审器：{result_default['loaded_checkers']}")
    print(f"  得分：{result_default['overall_score']}/100")
    print(f"  问题数：{result_default['total_issues']}")

    # 测试 financial 场景
    print("\n【测试 2】Financial 场景（金融）")
    reviewer_financial = PRDReviewer(scenario="financial")
    result_financial = reviewer_financial.review(test_prd, risk_level="R3")

    print(f"\n评审结果:")
    print(f"  场景：{result_financial['scenario']}")
    print(f"  加载评审器：{result_financial['loaded_checkers']}")
    print(f"  得分：{result_financial['overall_score']}/100")
    print(f"  问题数：{result_financial['total_issues']}")
    print(f"  严重问题：{result_financial['critical_issues']}")

    print("\n" + "=" * 60)
    print("对比分析:")
    print(f"  Default 场景得分：{result_default['overall_score']}")
    print(f"  Financial 场景得分：{result_financial['overall_score']}")
    print(
        f"  差异：{result_financial['overall_score'] - result_default['overall_score']}"
    )
    print("=" * 60)


class IterativeReviewer:
    """迭代评审器 v1.0（新增）"""

    def __init__(self, max_loops=3, target_score=80, auto_fix=True):
        self.max_loops = max_loops
        self.target_score = target_score
        self.auto_fix = auto_fix

    def review_with_iteration(
        self, prd_content: str, product_type: str = None, risk_level: str = "R3"
    ) -> Dict:
        """迭代评审 + 自动优化"""
        loop_count = 0
        current_prd = prd_content
        history = []

        print(f"\n{'=' * 60}")
        print(f"开始迭代评审（目标：{self.target_score}分，最多{self.max_loops}轮）")
        print(f"{'=' * 60}\n")

        while loop_count < self.max_loops:
            loop_count += 1
            print(f"\n{'=' * 60}")
            print(f"第 {loop_count} 轮评审")
            print(f"{'=' * 60}")

            reviewer = PRDReviewer(auto_detect=True)
            result = reviewer.review(current_prd, product_type, risk_level)

            print(f"\n📊 评审结果：{result['overall_score']}分")

            if result["overall_score"] >= self.target_score:
                print(
                    f"\n✅ 第{loop_count}轮评审通过（{result['overall_score']}≥{self.target_score}分）"
                )
                return {
                    "final_score": result["overall_score"],
                    "loop_count": loop_count,
                    "passed": True,
                    "history": history,
                    "final_result": result,
                    "final_prd": current_prd,
                }

            history.append(
                {
                    "loop": loop_count,
                    "score": result["overall_score"],
                    "issues": result["issues"],
                    "prd": current_prd,
                }
            )

            if self.auto_fix and loop_count < self.max_loops:
                print(
                    f"\n⚠️  第{loop_count}轮评分{result['overall_score']}< {self.target_score}，启动自动优化..."
                )
                current_prd = self.auto_fix_prd(current_prd, result["issues"])
            else:
                print(
                    f"\n⚠️  第{loop_count}轮评分{result['overall_score']}< {self.target_score}，停止优化"
                )
                break

        return {
            "final_score": result["overall_score"],
            "loop_count": loop_count,
            "passed": False,
            "history": history,
            "final_result": result,
            "final_prd": current_prd,
        }

    def auto_fix_prd(self, prd_content: str, issues: List[Dict]) -> str:
        """自动修复 PRD"""
        print("   🤖 AI 自动修复中...")

        missing_chapters = [i for i in issues if i.get("type") == "missing_section"]
        ai_issues = [i for i in issues if i.get("id", "").startswith("AI-")]

        optimized_prd = prd_content

        for issue in missing_chapters:
            chapter_name = issue.get("location", "章节")
            suggestion = issue.get("suggestion", "")
            print(f"   - 补充缺失章节：{chapter_name}")
            optimized_prd = self.add_missing_chapter(
                optimized_prd, chapter_name, suggestion
            )

        for issue in ai_issues:
            issue_type = issue.get("type", "")
            suggestion = issue.get("suggestion", "")
            if "boundary" in issue_type.lower():
                print(f"   - 添加边界条件：{issue.get('title')}")
                optimized_prd = self.add_boundary_conditions(optimized_prd, suggestion)
            if "exception" in issue_type.lower():
                print(f"   - 添加异常处理：{issue.get('title')}")
                optimized_prd = self.add_exception_handling(optimized_prd, suggestion)

        print("   ✅ 优化完成\n")
        return optimized_prd

    def add_missing_chapter(
        self, prd_content: str, chapter_name: str, suggestion: str
    ) -> str:
        """补充缺失章节"""
        appendix_match = re.search(r"\n## 附录", prd_content)
        if appendix_match:
            insert_pos = appendix_match.start()
            new_chapter = f"\n## {chapter_name}\n\n{suggestion}\n"
            return prd_content[:insert_pos] + new_chapter + prd_content[insert_pos:]
        return prd_content + f"\n\n## {chapter_name}\n\n{suggestion}\n"

    def add_boundary_conditions(self, prd_content: str, suggestion: str) -> str:
        """添加边界条件"""
        func_match = re.search(r"### \d+\.\d+ 功能", prd_content)
        if func_match:
            insert_pos = func_match.start()
            boundary_text = f"\n**边界条件**:\n- 最大值：待补充\n- 最小值：待补充\n- 异常值处理：待补充\n\n"
            return prd_content[:insert_pos] + boundary_text + prd_content[insert_pos:]
        return prd_content

    def add_exception_handling(self, prd_content: str, suggestion: str) -> str:
        """添加异常处理"""
        acceptance_match = re.search(r"### \d+\.\d+ 验收标准", prd_content)
        if acceptance_match:
            insert_pos = acceptance_match.start()
            exception_text = f"\n**异常处理**:\n- 参数校验失败：提示用户\n- 系统异常：记录日志并返回错误\n- 超时处理：30 秒超时\n\n"
            return prd_content[:insert_pos] + exception_text + prd_content[insert_pos:]
        return prd_content


def check_environment():
    """环境检测入口"""
    try:
        from check_environment import main as check_main

        return check_main()
    except ImportError:
        print("❌ 环境检测工具未找到")
        return 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PRD 评审引擎")
    parser.add_argument("--check-env", action="store_true", help="检测运行环境")
    parser.add_argument("--test", action="store_true", help="运行测试模式")

    args = parser.parse_args()

    if args.check_env:
        # 环境检测模式
        sys.exit(check_environment())
    elif args.test:
        # 测试模式
        print("=" * 60)
        print("PRD 评审引擎测试")
        print("=" * 60)
        print("\n测试自动场景识别...")

        test_prd = """
        # 金融产品 PRD
        
        ## 产品概述
        本产品为混合型基金，风险等级 R3。
        目标用户：稳健型投资者
        
        ## 功能设计
        1. 基金认购
        2. 基金申购
        3. 基金赎回
        """

        reviewer = PRDReviewer(auto_detect=True)
        result = reviewer.review(test_prd)

        print(f"\n识别场景：{result.get('scenario', 'unknown')}")
        print(f"总体评分：{result.get('overall_score', 0)}/100")
        print("\n✅ 测试完成")
    else:
        # 默认：显示帮助信息
        print("PRD 评审引擎 v3.1")
        print("\n使用方式：")
        print("  Python API: from review_engine import PRDReviewer")
        print("  环境检测: python3 review_engine.py --check-env")
        print("  测试模式: python3 review_engine.py --test")
        print("\n详细文档：查看 SKILL.md")
