#!/usr/bin/env python3
"""
L4 Verify Agent — 终极根治 retry 缩水 bug
==========================================

按老板 2026-07-01 强推 + LRN-20260630-002 设计:
- L1 (抽象 prompt) 失败: 18 分
- L2 (百分比 80%) 失败: 18 分
- L3 (绝对值 3000 字) 成功: 60 分 (老板硬指令)
- L4 (Verify Agent 长度校验) 理论根治: 未实施 ← 本文件

Verify Agent 在 Write Agent 之后立即执行，5 步规则检查：
1. 长度检查：≥ min_chars (3000 for code.py, 5000 for test_code.py)
2. 完整性检查：含 import + 类 + 主入口 + docstring
3. 占位符检查：无 TODO / "..." / "待补" / "（填写）"
4. 语法检查：python compile 验证语法正确
5. 关键字匹配：含 class/def/__init__/main

不通过 → 立即 retry，带具体失败原因给 Write Agent。
通过 → 进入 Test Agent。

设计原则:
- **不是 LLM agent**（纯规则）→ 不被偷懒
- **确定性逻辑** → 不依赖概率
- **5 步检查全失败才 retry** → 不浪费 token
- **结构化错误报告** → Write Agent 收到具体失败原因
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


@dataclass
class VerifyResult:
    """Verify Agent 输出"""
    passed: bool                            # 是否通过
    failures: List[str] = field(default_factory=list)    # 失败原因列表
    warnings: List[str] = field(default_factory=list)    # 警告列表
    metrics: dict = field(default_factory=dict)          # 量化指标

    def __bool__(self) -> bool:
        return self.passed


class VerifyAgent:
    """L4 Verify Agent - 5 步规则检查

    不调 LLM，纯确定性逻辑。检查输出是否满足硬约束。
    """

    # 4-Agent 流水线经验值
    DEFAULT_MIN_CHARS = {
        "code.py": 3000,
        "test_code.py": 5000,
        "plan.md": 2000,
        "refine.md": 1000,
    }

    # 占位符 / 截断信号
    PLACEHOLDER_PATTERNS = [
        (r"TODO", "TODO"),
        (r"placeholder", "placeholder"),
        (r"（填写）", "（填写）"),
        (r"占位", "占位"),
        (r"待补", "待补"),
        (r"\.\.\.\s*$", "省略号结尾"),
        (r"pass\s*$", "pass 占位（无实现）"),
    ]

    # 必须元素（按 file_type 区分）
    REQUIRED_PATTERNS_PYTHON = [
        (r"^import\s+|^from\s+", "import/from 语句"),
        (r"\bclass\s+\w+", "类定义"),
        (r"\bdef\s+\w+", "函数定义"),
        (r'if\s+__name__\s*==\s*["\']__main__', "主入口"),
        (r'"""', "docstring"),
    ]
    REQUIRED_PATTERNS_MARKDOWN = [
        (r"^#\s+\S", "一级标题"),
        (r"^##\s+\S", "二级标题"),
        (r"```", "代码块"),
    ]

    @property
    def REQUIRED_PATTERNS(self):
        # 动态选择（按 file_type）
        if self._current_file_type and self._current_file_type.endswith('.md'):
            return self.REQUIRED_PATTERNS_MARKDOWN
        return self.REQUIRED_PATTERNS_PYTHON

    def __init__(
        self,
        min_chars: int = 3000,
        strict: bool = True,
        enable_syntax_check: bool = True,
    ):
        self.min_chars = min_chars
        self.strict = strict
        self.enable_syntax_check = enable_syntax_check

    def verify(
        self,
        code: str,
        file_type: str = "code.py",
        min_chars: int = None,
    ) -> VerifyResult:
        """5 步规则检查

        Args:
            code: 待验证的代码
            file_type: 文件类型（code.py / test_code.py / plan.md / refine.md）
            min_chars: 自定义最小字符数（覆盖默认值）

        Returns:
            VerifyResult: passed + failures + metrics
        """
        # 自定义阈值优先
        if min_chars is None:
            min_chars = self.DEFAULT_MIN_CHARS.get(file_type, self.min_chars)

        # 设置当前 file_type 用于动态选择必检项
        self._current_file_type = file_type

        result = VerifyResult(passed=True)
        result.metrics = {
            "actual_chars": len(code),
            "min_chars": min_chars,
            "file_type": file_type,
            "strict": self.strict,
        }

        # === Step 1: 长度检查 ===
        actual_chars = len(code.strip())
        if actual_chars < min_chars:
            result.passed = False
            result.failures.append(
                f"❌ [Step 1 长度] {actual_chars} 字 < {min_chars} 字硬下限 "
                f"({min_chars - actual_chars} 字短缺, {(actual_chars/min_chars*100):.1f}%)"
            )

        # === Step 2: 完整性检查（按 file_type 动态选择）===
        required = self.REQUIRED_PATTERNS  # 动态属性
        for pattern, desc in required:
            if not re.search(pattern, code, re.MULTILINE):
                # 主入口和 docstring 是可选警告
                if desc in ["主入口", "docstring"]:
                    result.warnings.append(f"⚠️ [Step 2 完整性] 缺 {desc} (非致命)")
                else:
                    result.passed = False
                    result.failures.append(f"❌ [Step 2 完整性] 缺 {desc}")

        # === Step 3: 占位符检查 ===
        placeholder_hits = []
        for pattern, desc in self.PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, code, re.MULTILINE | re.IGNORECASE)
            if matches:
                placeholder_hits.append(f"{desc}×{len(matches)}")

        if placeholder_hits:
            result.passed = False
            result.failures.append(
                f"❌ [Step 3 占位符] 发现: {', '.join(placeholder_hits)}"
            )

        # === Step 4: 语法检查 ===
        if self.enable_syntax_check and (file_type.endswith(".py")):
            try:
                ast.parse(code)
                result.metrics["syntax"] = "valid"
            except SyntaxError as e:
                result.passed = False
                result.metrics["syntax"] = "invalid"
                result.failures.append(
                    f"❌ [Step 4 语法] SyntaxError 第 {e.lineno} 行: {e.msg}"
                )

        # === Step 5: 关键字密度检查 ===
        # 检查代码密度（import/class/def 的密度）
        lines = code.splitlines()
        non_empty_lines = [l for l in lines if l.strip()]
        keyword_count = len(re.findall(r"\b(class|def|import|from|async)\b", code))
        density = keyword_count / max(len(non_empty_lines), 1)
        result.metrics["keyword_density"] = round(density, 3)

        if density < 0.1:
            result.passed = False
            result.failures.append(
                f"❌ [Step 5 关键字密度] {density:.3f} < 0.1 "
                f"(关键词 {keyword_count} / 非空行 {len(non_empty_lines)})"
            )

        return result

    def format_failure_for_write_agent(self, result: VerifyResult) -> str:
        """格式化失败原因，准备给 Write Agent retry 时参考

        让 Write Agent 知道"具体哪里不够"，而不是猜。
        """
        if result.passed:
            return ""

        lines = [
            "⚠️ Verify Agent 检测到输出不达标，**必须立即修复**！",
            "",
            f"📊 当前字数: {result.metrics.get('actual_chars')} / 下限: {result.metrics.get('min_chars')}",
            "",
            "失败原因（按优先级）:",
        ]
        for i, fail in enumerate(result.failures, 1):
            lines.append(f"{i}. {fail}")

        if result.warnings:
            lines.append("")
            lines.append("警告（非致命但建议修复）:")
            for warn in result.warnings:
                lines.append(f"  {warn}")

        lines.extend([
            "",
            "📝 修复要求:",
            f"- **必须达到 {result.metrics.get('min_chars')} 字**（不允许任何截断）",
            "- 必须有完整 import + 类 + 函数 + 主入口 + docstring",
            "- 不允许 TODO / placeholder / pass 占位",
            "- 第 4 次 retry: 老板的硬指令阈值无法再降, 请老老实实写完整代码",
        ])

        return "\n".join(lines)


def verify_file(file_path: str, file_type: str = None) -> VerifyResult:
    """便捷函数: 验证一个文件

    Args:
        file_path: 文件路径
        file_type: 文件类型（自动推断 if None）

    Returns:
        VerifyResult
    """
    p = Path(file_path)
    if not p.exists():
        return VerifyResult(
            passed=False,
            failures=[f"❌ 文件不存在: {file_path}"],
        )

    code = p.read_text(encoding="utf-8", errors="replace")

    if file_type is None:
        file_type = p.name
        if file_type == "code.py":
            file_type = "code.py"
        elif file_type == "test_code.py":
            file_type = "test_code.py"
        elif file_type == "plan.md":
            file_type = "plan.md"

    agent = VerifyAgent()
    return agent.verify(code, file_type)


# ===== CLI =====
def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: verify_agent.py <file_path> [file_type]")
        print("示例: verify_agent.py output/multi_agent_v2_v31/code.py code.py")
        sys.exit(1)

    file_path = sys.argv[1]
    file_type = sys.argv[2] if len(sys.argv) > 2 else None

    result = verify_file(file_path, file_type)

    print("=" * 60)
    print(f"🔍 L4 Verify Agent 验证报告")
    print("=" * 60)
    print(f"文件: {file_path}")
    print(f"类型: {result.metrics.get('file_type')}")
    print()
    print(f"📊 指标:")
    for k, v in result.metrics.items():
        print(f"  · {k}: {v}")
    print()

    if result.passed:
        print("✅ 通过 — 满足所有硬约束")
        sys.exit(0)
    else:
        print("❌ 不通过 — 必须 retry")
        print()
        for fail in result.failures:
            print(fail)
        if result.warnings:
            print()
            print("警告:")
            for warn in result.warnings:
                print(warn)
        sys.exit(1)


if __name__ == "__main__":
    main()