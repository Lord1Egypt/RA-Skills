#!/usr/bin/env python3
"""
分析代码基本指标：函数数、类数、平均行长度、复杂度分数。
用法: python3 analyze-metrics.py <file>
"""

import re
import sys


def analyze_code_metrics(code):
    """Analyze code for common metrics."""
    functions = len(re.findall(r"^def\s+\w+", code, re.MULTILINE))
    classes = len(re.findall(r"^class\s+\w+", code, re.MULTILINE))
    lines = code.split("\n")
    avg_length = sum(len(l) for l in lines) / len(lines) if lines else 0
    complexity = len(re.findall(r"\b(if|elif|else|for|while|and|or)\b", code))

    return {
        "functions (函数数)": functions,
        "classes (类数)": classes,
        "avg_line_length (平均行长度)": avg_length,
        "complexity_score (复杂度分数)": complexity,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 analyze-metrics.py <file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        code = f.read()

    metrics = analyze_code_metrics(code)
    print("=" * 50)
    print("📊 代码指标分析")
    print("=" * 50)
    for key, value in metrics.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
    print("=" * 50)
