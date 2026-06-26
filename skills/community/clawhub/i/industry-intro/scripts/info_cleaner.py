#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息清洗与去重脚本
功能：剔除商业软文，数值硬校验，合并去重
"""

import re
import json
from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class CleanedInfo:
    """清洗后的信息数据结构"""
    category: str  # 信息类别
    content: str  # 清洗后的内容
    sources: List[str]  # 来源列表
    raw_numbers: List[str]  # 原始数值
    confidence: float  # 信度评分（0-1）


class InfoCleaner:
    """信息清洗器"""

    # 商业软文敏感词列表
    COMMERCIAL_WORDS = [
        "遥遥领先", "颠覆性", "世界领先", "全球第一", "史无前例",
        "强大", "卓越", "顶级", "完美", "极致", "无敌",
        "独一无二", "空前绝后", "里程碑", "革命性", "划时代"
    ]

    def __init__(self):
        """初始化信息清洗器"""
        self.seen_contents: Set[str] = set()

    def remove_commercial_words(self, text: str) -> str:
        """
        剔除商业软文中的溢美之词

        Args:
            text: 原始文本

        Returns:
            清洗后的文本
        """
        cleaned = text
        for word in self.COMMERCIAL_WORDS:
            # 使用正则表达式匹配，保留上下文结构
            pattern = re.compile(f"(['，。、；：？！\\s]|^){word}(['，。、；：？！\\s]|$)", re.IGNORECASE)
            cleaned = pattern.sub(r"\1\2", cleaned)

        # 清理多余的标点和空格
        cleaned = re.sub(r'([，。、；：？！]){2,}', r'\1', cleaned)
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)

        return cleaned.strip()

    def extract_raw_numbers(self, text: str) -> List[str]:
        """
        提取原始数值

        Args:
            text: 原始文本

        Returns:
            原始数值列表
        """
        # 匹配数字（整数、小数、百分比）
        number_pattern = re.compile(
            r'\b\d+\.?\d*%\s*|\b\d{4}年\s*|\b\d+\.?\d*\s*(?:万|亿|千元|万元|亿元|美元|欧元|人民币|元|美元|吨|千克|克|升|毫升|米|千米|毫米|微米|摄氏度|℃|伏特|V|瓦特|W|千瓦|kW|兆瓦|MW|吉瓦|GW|赫兹|Hz|千赫|kHz|兆赫|MHz)',
            re.IGNORECASE
        )
        matches = number_pattern.findall(text)
        return [match.strip() for match in matches]

    def validate_numbers(self, original_text: str, cleaned_text: str) -> bool:
        """
        数值硬校验：确保关键参数与原文一致

        Args:
            original_text: 原始文本
            cleaned_text: 清洗后的文本

        Returns:
            是否通过校验
        """
        original_numbers = self.extract_raw_numbers(original_text)
        cleaned_numbers = self.extract_raw_numbers(cleaned_text)

        # 检查数量是否一致
        if len(original_numbers) != len(cleaned_numbers):
            return False

        # 检查每个数值是否一致
        for orig_num, clean_num in zip(original_numbers, cleaned_numbers):
            if orig_num != clean_num:
                print(f"数值不一致：原文 {orig_num} vs 清洗后 {clean_num}")
                return False

        return True

    def deduplicate(self, info_list: List[Dict]) -> List[Dict]:
        """
        合并去重

        Args:
            info_list: 信息列表

        Returns:
            去重后的信息列表
        """
        deduplicated = []
        seen_signatures = set()

        for info in info_list:
            # 生成内容签名（用于去重）
            content = info.get("content", "")
            signature = content.strip().lower()[:100]  # 使用前100个字符作为签名

            if signature not in seen_signatures:
                seen_signatures.add(signature)
                deduplicated.append(info)

        return deduplicated

    def calculate_confidence(self, info: Dict) -> float:
        """
        计算信度评分

        Args:
            info: 信息字典

        Returns:
            信度评分（0-1）
        """
        confidence = 0.0

        # 来源信度评分
        source_type = info.get("source_type", "")
        if source_type == "knowledge":
            confidence += 0.4  # 知识库信度高
        elif source_type == "api":
            confidence += 0.3  # API信度中等
        elif source_type == "web":
            confidence += 0.2  # 网页信度较低

        # 优先级评分
        priority = info.get("priority", 1)
        confidence += min(priority * 0.1, 0.3)

        # 内容长度评分（避免过短内容）
        content = info.get("content", "")
        if len(content) > 100:
            confidence += 0.2
        elif len(content) > 50:
            confidence += 0.1

        # 包含数值加分
        if self.extract_raw_numbers(content):
            confidence += 0.1

        return min(confidence, 1.0)

    def clean(self, raw_results: List[Dict]) -> List[CleanedInfo]:
        """
        执行清洗流程

        Args:
            raw_results: 原始检索结果列表

        Returns:
            清洗后的信息列表
        """
        cleaned_infos = []

        # 1. 去重
        deduplicated = self.deduplicate(raw_results)

        # 2. 清洗每个信息项
        for info in deduplicated:
            original_content = info.get("content", "")
            source_name = info.get("source_name", "")
            source_type = info.get("source_type", "")

            # 剔除商业软文词汇
            cleaned_content = self.remove_commercial_words(original_content)

            # 数值硬校验
            if not self.validate_numbers(original_content, cleaned_content):
                print(f"警告：{source_name} 的数值校验失败，跳过")
                continue

            # 提取原始数值
            raw_numbers = self.extract_raw_numbers(cleaned_content)

            # 计算信度
            confidence = self.calculate_confidence(info)

            # 过滤低信度内容
            if confidence < 0.3:
                continue

            # 分类信息（根据内容特征）
            category = self._classify_content(cleaned_content)

            cleaned_info = CleanedInfo(
                category=category,
                content=cleaned_content,
                sources=[source_name],
                raw_numbers=raw_numbers,
                confidence=confidence
            )

            cleaned_infos.append(cleaned_info)

        # 3. 按信度排序
        cleaned_infos.sort(key=lambda x: x.confidence, reverse=True)

        return cleaned_infos

    def _classify_content(self, content: str) -> str:
        """
        根据内容特征分类

        Args:
            content: 清洗后的内容

        Returns:
            信息类别
        """
        if any(word in content for word in ["定义", "是指", "属于", "概念"]):
            return "core_definition"
        elif any(word in content for word in ["参数", "规格", "技术", "原理", "成分"]):
            return "technical_params"
        elif any(word in content for word in ["应用", "场景", "用途", "市场", "行业"]):
            return "applications"
        elif any(word in content for word in ["口径", "统计", "范围", "包含", "不包含"]):
            return "statistical_scope"
        else:
            return "general"


def main():
    """
    主函数示例
    """
    import argparse

    parser = argparse.ArgumentParser(description="信息清洗与去重")
    parser.add_argument("--input", required=True, help="输入文件路径（JSON格式）")
    parser.add_argument("--output", default="cleaned_info.json", help="输出文件路径")

    args = parser.parse_args()

    # 读取原始检索结果
    with open(args.input, 'r', encoding='utf-8') as f:
        raw_results = json.load(f)

    # 创建清洗器并执行清洗
    cleaner = InfoCleaner()
    cleaned_infos = cleaner.clean(raw_results.get("results", []))

    # 输出清洗后的信息
    output_data = {
        "cleaned_infos": [
            {
                "category": info.category,
                "content": info.content,
                "sources": info.sources,
                "raw_numbers": info.raw_numbers,
                "confidence": info.confidence
            }
            for info in cleaned_infos
        ]
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"清洗完成，共处理 {len(cleaned_infos)} 条高信度信息，结果已保存到 {args.output}")


if __name__ == "__main__":
    main()
