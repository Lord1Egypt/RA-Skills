#!/usr/bin/env python3
"""
章节解析器 v1.0

解析 PRD 文档的章节结构：
- 提取章节树（标题、层级、位置）
- 提取章节内容
- 识别功能点章节
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class Section:
    """章节定义"""
    title: str           # 章节标题
    level: int           # 标题层级（1-6）
    start_pos: int       # 起始位置（行号）
    end_pos: int         # 结束位置（行号）
    content: str         # 章节内容
    children: List['Section']  # 子章节
    parent: Optional['Section'] = None  # 父章节

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "title": self.title,
            "level": self.level,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "content_length": len(self.content),
            "children_count": len(self.children)
        }


class SectionParser:
    """章节解析器"""

    # 功能点章节的特征
    FUNCTION_PATTERNS = [
        r"功能\s*\d+[:：]",          # "功能 1：下单" 或 "### 功能 1：下单"
        r"功能\d+[:：]",             # "功能1：下单"
        r"[一二三四五六七八九十]+[、.]\s*功能",  # "一、功能xxx"
    ]

    # 常见章节名
    SECTION_ALIASES = {
        "产品概述": ["产品简介", "需求概述", "项目概述"],
        "业务流程": ["业务流程图", "全局业务流程", "流程图"],
        "功能需求": ["功能设计", "功能清单", "功能详情"],
        "非功能需求": ["非功能性需求", "性能需求", "质量属性"],
        "验收标准": ["验收条件", "验收测试", "测试标准"],
        "系统对接": ["接口设计", "系统接口", "外部接口"],
        "数据需求": ["数据来源", "数据处理", "数据字典"],
        "界面设计": ["UI设计", "界面原型", "原型设计"],
        "合规要求": ["合规说明", "监管要求", "业务规则"],
        "风险揭示": ["风险提示", "风险说明", "风险管理"],
        "异常处理": ["异常场景", "错误处理", "异常流程"],
    }

    def __init__(self):
        self.sections: List[Section] = []
        self.raw_content: str = ""
        self.lines: List[str] = []

    def parse(self, content: str) -> List[Section]:
        """
        解析文档内容，提取章节结构

        参数:
            content: PRD文档内容

        返回:
            章节列表
        """
        self.raw_content = content
        self.lines = content.split('\n')
        self.sections = []

        # 提取所有标题
        headings = self._extract_headings()

        if not headings:
            return self.sections

        # 构建章节树
        self.sections = self._build_section_tree(headings)

        # 提取章节内容
        self._extract_section_content()

        return self.sections

    def _extract_headings(self) -> List[Tuple[int, str, int]]:
        """
        提取所有标题

        返回:
            [(level, title, line_number), ...]
        """
        headings = []

        for i, line in enumerate(self.lines):
            # Markdown 标题
            md_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if md_match:
                level = len(md_match.group(1))
                title = md_match.group(2).strip()
                headings.append((level, title, i))
                continue

            # 中文数字章节（如"一、产品概述"）
            cn_match = re.match(r'^([一二三四五六七八九十]+)[、.．]\s*(.+)$', line)
            if cn_match:
                # 中文数字转阿拉伯数字
                cn_num = cn_match.group(1)
                ar_num = self._cn_to_arabic(cn_num)
                level = 1 if ar_num <= 10 else 2
                title = cn_match.group(2).strip()
                headings.append((level, title, i))
                continue

            # 数字章节（如"1. 产品概述"）
            num_match = re.match(r'^(\d+)[.．、]\s*(.+)$', line)
            if num_match:
                level = 1 if int(num_match.group(1)) < 10 else 2
                title = num_match.group(2).strip()
                headings.append((level, title, i))

        return headings

    def _build_section_tree(self, headings: List[Tuple[int, str, int]]) -> List[Section]:
        """构建章节树"""
        if not headings:
            return []

        sections = []
        stack = []  # 用于追踪当前路径上的父章节

        for i, (level, title, line_num) in enumerate(headings):
            # 确定结束位置
            if i + 1 < len(headings):
                end_line = headings[i + 1][2] - 1
            else:
                end_line = len(self.lines) - 1

            section = Section(
                title=title,
                level=level,
                start_pos=line_num,
                end_pos=end_line,
                content="",  # 后续填充
                children=[]
            )

            # 找到合适的父章节
            while stack and stack[-1].level >= level:
                stack.pop()

            if stack:
                # 有父章节
                section.parent = stack[-1]
                stack[-1].children.append(section)
            else:
                # 顶级章节
                sections.append(section)

            stack.append(section)

        return sections

    def _extract_section_content(self):
        """提取章节内容"""
        def extract_content(section: Section):
            # 提取内容行
            content_lines = self.lines[section.start_pos + 1:section.end_pos + 1]
            section.content = '\n'.join(content_lines).strip()

            # 递归处理子章节
            for child in section.children:
                extract_content(child)

        for section in self.sections:
            extract_content(section)

    def _cn_to_arabic(self, cn_num: str) -> int:
        """中文数字转阿拉伯数字"""
        cn_map = {
            "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
            "六": 6, "七": 7, "八": 8, "九": 9, "十": 10
        }
        if cn_num in cn_map:
            return cn_map[cn_num]
        if cn_num.startswith("十"):
            if len(cn_num) == 1:
                return 10
            return 10 + cn_map.get(cn_num[1], 0)
        return 0

    def get_section_by_title(self, title: str) -> Optional[Section]:
        """按标题查找章节"""
        def find_in(sections: List[Section]) -> Optional[Section]:
            for section in sections:
                # 直接匹配
                if title in section.title or section.title in title:
                    return section
                # 别名匹配
                aliases = self.SECTION_ALIASES.get(title, [])
                for alias in aliases:
                    if alias in section.title:
                        return section
                # 递归查找子章节
                result = find_in(section.children)
                if result:
                    return result
            return None

        return find_in(self.sections)

    def get_function_sections(self) -> List[Section]:
        """获取所有功能点章节"""
        functions = []

        def find_functions(sections: List[Section]):
            for section in sections:
                # 检查是否匹配功能点模式（明确的"功能 N："格式）
                is_function = False
                for pattern in self.FUNCTION_PATTERNS:
                    if re.search(pattern, section.title, re.IGNORECASE):
                        # 排除"功能需求"这种父章节
                        if "功能需求" not in section.title and "功能设计" not in section.title:
                            functions.append(section)
                            is_function = True
                        break

                # 无论是否匹配，都递归检查子章节
                find_functions(section.children)

        find_functions(self.sections)
        return functions

    def get_all_sections_flat(self) -> List[Section]:
        """获取扁平化的章节列表"""
        result = []

        def flatten(sections: List[Section]):
            for section in sections:
                result.append(section)
                flatten(section.children)

        flatten(self.sections)
        return result

    def print_structure(self, sections: List[Section] = None, indent: int = 0):
        """打印章节结构"""
        if sections is None:
            sections = self.sections

        for section in sections:
            prefix = "  " * indent
            print(f"{prefix}├─ {section.title} (L{section.start_pos}-L{section.end_pos})")
            if section.children:
                self.print_structure(section.children, indent + 1)


if __name__ == "__main__":
    # 测试用例
    test_prd = """
# 测试 PRD

## 一、产品概述
这是产品概述内容。

## 二、业务流程
### 2.1 主业务流程
流程内容...

## 三、功能需求

### 功能 1：下单功能
下单功能描述...

### 功能 2：支付功能
支付功能描述...

## 四、验收标准
验收标准内容...
"""

    parser = SectionParser()
    sections = parser.parse(test_prd)

    print("=" * 60)
    print("章节结构")
    print("=" * 60)
    parser.print_structure()

    print("\n" + "=" * 60)
    print("功能点章节")
    print("=" * 60)
    functions = parser.get_function_sections()
    for func in functions:
        print(f"  - {func.title}")