#!/usr/bin/env python3
"""
章节-检查项映射器 v1.0

负责：
- 定义章节与检查项的对应关系
- 根据章节内容分发检查任务
- 区分文档级、章节级、功能点级检查
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass

from .check_items import CHECK_ITEMS, CheckItem, Priority
from .section_parser import Section, SectionParser


@dataclass
class CheckTask:
    """检查任务"""
    check_item: CheckItem      # 检查项
    section: Section           # 目标章节
    content: str               # 待检查内容


class SectionMatcher:
    """章节-检查项映射器"""

    # 章节-检查项映射关系
    SECTION_CHECK_MAP = {
        # 业务流程章节 → 流程描述
        "业务流程": ["C001"],  # 流程描述

        # 功能需求章节 → 异常处理、元素完整性、交互逻辑、算法公式
        "功能需求": ["C002", "C004", "C005", "C006"],

        # 数据需求章节 → 查询关联
        "数据需求": ["C007"],  # 查询关联

        # 验收标准章节 → GWT验收标准
        "验收标准": ["C008"],  # GWT验收标准

        # 系统对接章节 → 系统对接描述
        "系统对接": ["C009"],  # 系统对接描述

        # 界面设计章节 → 界面细节、原型附件
        "界面设计": ["C011", "C013"],  # 界面细节、原型附件
    }

    # 文档级检查项（对全文检查）
    DOCUMENT_LEVEL_CHECKS = ["C003", "C010", "C012"]  # 改造内容标注、分项描述、改造类型

    # 功能点级检查项（对每个功能点检查）
    FUNCTION_LEVEL_CHECKS = ["C002", "C004", "C005", "C006", "C007"]

    def __init__(self):
        self.parser = SectionParser()

    def match(self, content: str) -> Tuple[List[CheckTask], List[CheckTask], List[CheckTask]]:
        """
        匹配章节与检查项

        返回:
            (文档级任务, 章节级任务, 功能点级任务)
        """
        # 解析章节结构
        sections = self.parser.parse(content)

        document_tasks = []
        section_tasks = []
        function_tasks = []

        # 1. 文档级检查
        for check_id in self.DOCUMENT_LEVEL_CHECKS:
            check_item = CHECK_ITEMS.get(check_id)
            if check_item:
                document_tasks.append(CheckTask(
                    check_item=check_item,
                    section=None,  # 文档级，无特定章节
                    content=content
                ))

        # 2. 章节级检查
        for section in self.parser.get_all_sections_flat():
            # 查找匹配的检查项
            matched_checks = self._find_checks_for_section(section.title)

            for check_id in matched_checks:
                check_item = CHECK_ITEMS.get(check_id)
                if check_item:
                    section_tasks.append(CheckTask(
                        check_item=check_item,
                        section=section,
                        content=section.content
                    ))

        # 3. 功能点级检查
        function_sections = self.parser.get_function_sections()

        for func_section in function_sections:
            for check_id in self.FUNCTION_LEVEL_CHECKS:
                check_item = CHECK_ITEMS.get(check_id)
                if check_item:
                    function_tasks.append(CheckTask(
                        check_item=check_item,
                        section=func_section,
                        content=func_section.content
                    ))

        return document_tasks, section_tasks, function_tasks

    def _find_checks_for_section(self, section_title: str) -> List[str]:
        """查找章节对应的检查项"""
        matched = []

        for section_pattern, check_ids in self.SECTION_CHECK_MAP.items():
            if section_pattern in section_title or section_title in section_pattern:
                matched.extend(check_ids)

        return list(set(matched))  # 去重

    def get_tasks_by_priority(self, tasks: List[CheckTask]) -> Dict[Priority, List[CheckTask]]:
        """按优先级分组任务"""
        result = {
            Priority.CORE: [],
            Priority.IMPROVE: [],
            Priority.OPTIMIZE: []
        }

        for task in tasks:
            result[task.check_item.priority].append(task)

        return result

    def get_all_tasks(self, content: str) -> List[CheckTask]:
        """获取所有检查任务（合并三类）"""
        doc_tasks, sec_tasks, func_tasks = self.match(content)
        return doc_tasks + sec_tasks + func_tasks


if __name__ == "__main__":
    # 测试用例
    test_prd = """
# 测试 PRD

## 一、产品概述
这是产品概述内容。

## 二、业务流程
### 2.1 主业务流程
```mermaid
graph LR
    A[开始] --> B[处理]
    B --> C[结束]
```

## 三、功能需求

### 功能 1：下单功能
用户点击下单按钮，系统处理下单请求。
输入：金额、产品代码
输出：订单号

### 功能 2：支付功能
用户支付订单。

## 四、验收标准
Given 用户已登录
When 用户点击购买
Then 系统创建订单

## 五、系统对接
上游：核心系统
下游：支付系统
"""

    matcher = SectionMatcher()
    doc_tasks, sec_tasks, func_tasks = matcher.match(test_prd)

    print("=" * 60)
    print(f"文档级检查任务：{len(doc_tasks)}")
    print("=" * 60)
    for task in doc_tasks:
        print(f"  - [{task.check_item.priority.value}] {task.check_item.name}")

    print("\n" + "=" * 60)
    print(f"章节级检查任务：{len(sec_tasks)}")
    print("=" * 60)
    for task in sec_tasks:
        print(f"  - [{task.check_item.priority.value}] {task.check_item.name} → {task.section.title}")

    print("\n" + "=" * 60)
    print(f"功能点级检查任务：{len(func_tasks)}")
    print("=" * 60)
    for task in func_tasks:
        print(f"  - [{task.check_item.priority.value}] {task.check_item.name} → {task.section.title}")