#!/usr/bin/env python3
"""
比较代码修改前后的圈复杂度变化。
用法: python3 compare-complexity.py <before_file> <after_file>
"""

import re
import sys


class ComplexityAnalyzer:
    """Analyze code complexity metrics."""

    def __init__(self, code: str):
        self.code = code
        self.lines = code.split("\n")

    def calculate_cyclomatic_complexity(self) -> int:
        """McCabe 圈复杂度：统计决策点"""
        complexity = 1
        decision_patterns = [
            r"\bif\b", r"\belif\b", r"\bfor\b", r"\bwhile\b",
            r"\bexcept\b", r"\band\b(?!$)", r"\bor\b(?!$)",
        ]
        for pattern in decision_patterns:
            complexity += len(re.findall(pattern, self.code))
        return complexity

    def calculate_cognitive_complexity(self) -> int:
        """认知复杂度：考虑嵌套深度"""
        cognitive = 0
        nesting_depth = 0
        for line in self.lines:
            if re.search(r"^\s*(if|for|while|def|class|try)\b", line):
                nesting_depth += 1
                cognitive += nesting_depth
            elif re.search(r"^\s*(elif|else|except|finally)\b", line):
                cognitive += nesting_depth
            if line and not line[0].isspace():
                nesting_depth = 0
        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        可维护性指数 (0-100)：
        > 85: 优秀 / > 65: 良好 / > 50: 一般 / < 50: 较差
        """
        lines = len(self.lines)
        cyclomatic = self.calculate_cyclomatic_complexity()
        cognitive = self.calculate_cognitive_complexity()
        mi = 171 - 5.2 * (cyclomatic / max(lines, 1)) - 0.23 * cognitive - 16.2 * (lines / 1000)
        return max(0, min(100, mi))

    def get_complexity_report(self) -> dict:
        return {
            "cyclomatic_complexity (圈复杂度)": self.calculate_cyclomatic_complexity(),
            "cognitive_complexity (认知复杂度)": self.calculate_cognitive_complexity(),
            "maintainability_index (可维护性指数)": round(self.calculate_maintainability_index(), 2),
            "lines_of_code (代码行数)": len(self.lines),
            "avg_line_length (平均行长度)": round(sum(len(l) for l in self.lines) / max(len(self.lines), 1), 2),
        }


def compare_files(before_file: str, after_file: str) -> None:
    with open(before_file) as f:
        before_code = f.read()
    with open(after_file) as f:
        after_code = f.read()

    before_metrics = ComplexityAnalyzer(before_code).get_complexity_report()
    after_metrics = ComplexityAnalyzer(after_code).get_complexity_report()

    print("=" * 60)
    print("📊 代码复杂度对比分析")
    print("=" * 60)

    for label, metrics in [("修改前 (BEFORE)", before_metrics), ("修改后 (AFTER)", after_metrics)]:
        print(f"\n{label}:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

    print("\n变化 (CHANGES):")
    for key in before_metrics:
        change = after_metrics[key] - before_metrics[key]
        print(f"  {key}: {change:+}")

    print("\n评估 (ASSESSMENT):")
    mi_change = after_metrics["maintainability_index (可维护性指数)"] - before_metrics["maintainability_index (可维护性指数)"]
    cc_change = after_metrics["cyclomatic_complexity (圈复杂度)"] - before_metrics["cyclomatic_complexity (圈复杂度)"]

    print(f"  {'✅ 代码更易维护' if mi_change > 0 else '⚠️  代码更难维护' if mi_change < 0 else '➡️ 可维护性未变'}")
    print(f"  {'✅ 复杂度降低' if cc_change < 0 else '⚠️  复杂度增加' if cc_change > 0 else '➡️ 复杂度未变'}")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python3 compare-complexity.py <before_file> <after_file>")
        sys.exit(1)
    compare_files(sys.argv[1], sys.argv[2])
