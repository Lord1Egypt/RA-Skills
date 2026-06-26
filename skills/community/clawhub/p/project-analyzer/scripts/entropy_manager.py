"""
Entropy Manager - 熵管理器
清理文档中的冗余、错误和不一致
"""

import re
from typing import Dict


class EntropyManager:
    """熵管理器 - 车夫"""
    
    def __init__(self):
        self.cleaners = [
            WhitespaceCleaner(),
            FormatCleaner(),
            DuplicateCleaner(),
        ]
        self.config = {
            'remove_extra_newlines': True,
            'remove_trailing_spaces': True,
            'normalize_whitespace': True,
            'fix_broken_lists': True
        }
    
    def clean(self, content: str) -> str:
        """清理输出内容"""
        for cleaner in self.cleaners:
            content = cleaner.clean(content)
        
        return content
    
    def organize(self, output_dir: str) -> Dict:
        """整理输出目录"""
        return {
            'organized': True,
            'files_processed': 0
        }


class WhitespaceCleaner:
    """空白清理"""
    
    def clean(self, content: str) -> str:
        # 移除多余空行（超过2个连续空行）
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        
        # 移除行尾空白
        lines = content.split('\n')
        lines = [line.rstrip() for line in lines]
        
        # 移除文件末尾多余空行
        while lines and not lines[-1].strip():
            lines.pop()
        
        return '\n'.join(lines)


class FormatCleaner:
    """格式清理"""
    
    def clean(self, content: str) -> str:
        # 标准化标题格式（确保 # 后有空格）
        content = re.sub(r'^#+\w+', lambda m: m.group(0)[:1] + ' ' + m.group(0)[1:].lstrip(), content, flags=re.MULTILINE)
        
        # 标准化代码块（确保换行）
        content = re.sub(r'```\s*(\w+)', r'```\n\1', content)
        content = re.sub(r'```\s*$', '```', content, flags=re.MULTILINE)
        
        # 标准化表格（确保 | 周围有空格）
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.strip().startswith('|'):
                # 标准化表格行
                parts = [p.strip() for p in line.split('|')]
                line = ' | '.join(p for p in parts if p or p == '')
                if not line.endswith('|'):
                    line = line + ' |'
                if not line.startswith('|'):
                    line = '| ' + line
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        return content


class DuplicateCleaner:
    """重复清理"""
    
    def clean(self, content: str) -> str:
        lines = content.split('\n')
        seen = set()
        result = []
        
        # 跳过完全重复的行（保留第一个）
        for line in lines:
            stripped = line.strip()
            if stripped and stripped not in seen:
                seen.add(stripped)
                result.append(line)
            elif not stripped:
                result.append(line)
        
        return '\n'.join(result)


# 导出
__all__ = ['EntropyManager']
