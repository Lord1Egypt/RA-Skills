"""
输出护栏 (Output Guard)
- API 密钥过滤
- 密码/令牌过滤
- 身份证/邮箱过滤
"""

import re
from typing import List, Tuple, Optional


# 10 种敏感信息模式
SENSITIVE_PATTERNS: List[Tuple[str, str]] = [
    # (正则表达式, 类型描述)
    (r"API_KEY\s*[:=]\s*['\"]?\S+['\"]?", "API密钥"),
    (r"api_key\s*[:=]\s*['\"]?\S+['\"]?", "API密钥"),
    (r"password\s*(?:is\s*)?[:=]\s*['\"]?\S+['\"]?", "密码"),
    (r"passwd\s*[:=]\s*['\"]?\S+['\"]?", "密码"),
    (r"secret\s*[:=]\s*['\"]?\S+['\"]?", "密钥"),
    (r"token\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}['\"]?", "访问令牌"),
    (r"private_key\s*[:=]\s*['\"]?\S+['\"]?", "私钥"),
    (r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----", "私钥"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "邮箱地址"),
    (r"\b\d{17}[\dXx]\b", "身份证号"),
]

# 预编译正则表达式
COMPILED_SENSITIVE_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), desc)
    for pattern, desc in SENSITIVE_PATTERNS
]

# 替换模板
REDACTED_TEMPLATES = {
    "API密钥": "[API密钥已过滤]",
    "密码": "[密码已过滤]",
    "密钥": "[密钥已过滤]",
    "访问令牌": "[访问令牌已过滤]",
    "私钥": "[私钥已过滤]",
    "邮箱地址": "[邮箱已过滤]",
    "身份证号": "[身份证号已过滤]",
}


class OutputGuard:
    """输出护栏：检测并过滤敏感信息"""

    def __init__(self):
        self.patterns = COMPILED_SENSITIVE_PATTERNS
        self.redacted_templates = REDACTED_TEMPLATES

    def check(self, message: str) -> "GuardrailResult":
        """
        检查输出消息，过滤敏感信息

        Args:
            message: 输出消息

        Returns:
            GuardrailResult: 检查结果，包含过滤后的消息
        """
        from guardrail import GuardrailResult

        sanitized = message
        found_types = []

        for pattern, desc in self.patterns:
            if pattern.search(sanitized):
                found_types.append(desc)
                replacement = self.redacted_templates.get(desc, f"[{desc}已过滤]")
                sanitized = pattern.sub(replacement, sanitized)

        if found_types:
            return GuardrailResult(
                allowed=True,
                reason=f"检测到敏感信息：{', '.join(set(found_types))}",
                message=f"已过滤 {len(found_types)} 处敏感信息：{', '.join(set(found_types))}",
                sanitized_output=sanitized
            )

        # 没有敏感信息
        return GuardrailResult(allowed=True)

    def detect_only(self, message: str) -> List[str]:
        """仅检测敏感信息类型，不做过滤（用于调试）"""
        found = []
        for pattern, desc in self.patterns:
            if pattern.search(message):
                found.append(desc)
        return found


if __name__ == "__main__":
    # 测试
    guard = OutputGuard()

    test_cases = [
        "这是一条正常消息",
        "API_KEY=sk-1234567890abcdef",
        "password=mysecretpass123",
        "联系邮箱：test@example.com",
        "身份证号：110101199001011234",
        "REDACTED-SECRET",
    ]

    for msg in test_cases:
        result = guard.check(msg)
        if result.sanitized_output:
            print(f"原始: {msg[:50]}...")
            print(f"过滤: {result.sanitized_output[:50]}...")
            print(f"原因: {result.reason}")
            print()
        else:
            print(f"正常: {msg[:50]}...")
