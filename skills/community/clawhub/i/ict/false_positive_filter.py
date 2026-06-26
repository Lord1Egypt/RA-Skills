"""
误报过滤与白名单机制
减少误报，支持忽略注释
"""
import re
import os
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple


class FalsePositiveFilter:
    """误报过滤器"""
    
    # 预定义误报模式
    DEFAULT_WHITELIST = {
        # 示例/测试代码
        r'API_KEY\s*=\s*["\']YOUR_',
        r'API_KEY\s*=\s*["\']xxx',
        r'API_KEY\s*=\s*["\']test',
        r'SECRET\s*=\s*["\']xxx',
        r'PASSWORD\s*=\s*["\']example',
        # 本地开发
        r'https?://localhost',
        r'https?://127\.0\.0\.1',
        r'https?://0\.0\.0\.0',
        # 示例域名
        r'https?://example\.com',
        r'https?://test\.com',
        r'https?://dummy\.com',
        # Docstring 中的示例
        r'""".*api.*key.*"""',
        r"'''.*api.*key.*'''",
        # 注释中的示例
        r'#.*example',
        r'//.*example',
        r'/\*.*example.*\*/',
    }
    
    # 忽略标记
    IGNORE_MARKERS = [
        '# ict: ignore',
        '# ict: skip',
        '# eslint-disable',
        '# pylint: disable',
        '# noqa',
        '// ict: ignore',
        '// ict: skip',
        '/* ict: ignore */',
    ]
    
    def __init__(self, custom_whitelist: Optional[Set[str]] = None):
        self.whitelist_patterns = self.DEFAULT_WHITELIST.copy()
        if custom_whitelist:
            self.whitelist_patterns.update(custom_whitelist)
        self.compiled_whitelist = [re.compile(p, re.IGNORECASE) for p in self.whitelist_patterns]
    
    def add_whitelist(self, pattern: str):
        """添加白名单模式"""
        self.whitelist_patterns.add(pattern)
        self.compiled_whitelist.append(re.compile(pattern, re.IGNORECASE))
    
    def is_false_positive(self, match: str, context: str = "", line: str = "") -> bool:
        """判断是否为误报"""
        # 检查行级忽略标记
        for marker in self.IGNORE_MARKERS:
            if marker.lower() in line.lower():
                return True
        
        # 检查匹配内容是否在白名单中
        for pattern in self.compiled_whitelist:
            if pattern.search(match) or pattern.search(context):
                return True
        
        return False
    
    def filter_matches(self, matches: List[Dict]) -> List[Dict]:
        """过滤误报"""
        filtered = []
        for match in matches:
            content = match.get('context', '') or match.get('match', '')
            line = match.get('line_content', '')
            if not self.is_false_positive(content, line=line):
                filtered.append(match)
        return filtered


class IgnoreCommentParser:
    """解析忽略注释"""
    
    # 支持的忽略语法
    IGNORE_TYPES = {
        # 单行忽略
        'line': r'#\s*ict:\s*ignore\s*(.*)',
        'line_skip': r'#\s*ict:\s*skip\s*(.*)',
        # 行范围忽略
        'block_start': r'#\s*ict:\s*ignore-next:\s*(\d+)',
        'block_end': r'#\s*ict:\s*ignore-end',
        # 规则忽略
        'rule': r'#\s*ict:\s*ignore:\s*([a-z\-]+)',
    }
    
    def __init__(self):
        self.compiled = {k: re.compile(v) for k, v in self.IGNORE_TYPES.items()}
    
    def parse_line(self, line: str) -> Dict:
        """解析单行注释"""
        result = {'type': None, 'value': None, 'line': line}
        
        for ignore_type, pattern in self.compiled.items():
            match = pattern.search(line)
            if match:
                result['type'] = ignore_type
                result['value'] = match.group(1) if match.groups() else True
                break
        
        return result
    
    def get_ignored_rules(self, lines: List[str]) -> Set[str]:
        """从代码中提取被忽略的规则"""
        ignored = set()
        for line in lines:
            parsed = self.parse_line(line)
            if parsed['type'] == 'rule':
                ignored.add(parsed['value'])
        return ignored
    
    def should_ignore_line(self, line: str) -> bool:
        """判断该行是否应该被忽略"""
        return self.parse_line(line)['type'] is not None


# 测试
if __name__ == "__main__":
    filter = FalsePositiveFilter()
    
    # 测试用例
    test_cases = [
        ("API_KEY = 'YOUR_API_KEY'", True),   # 误报
        ("password = 'example'", True),        # 误报  
        ("https://localhost:8080", True),      # 误报
        ("api_key = 'sk-1234567890abcdef'", False),  # 真问题
    ]
    
    print("=== 误报过滤测试 ===")
    for match, expected in test_cases:
        result = filter.is_false_positive(match, line=match)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{match}' -> 误报: {result}")
    
    print("\n=== 忽略注释测试 ===")
    parser = IgnoreCommentParser()
    test_lines = [
        "API_KEY = 'test' # ict: ignore",
        "password = 'xxx' # ict: ignore: credential-harvest",
        "normal_code()",
    ]
    for line in test_lines:
        print(f"  '{line}' -> {parser.parse_line(line)['type']}")
