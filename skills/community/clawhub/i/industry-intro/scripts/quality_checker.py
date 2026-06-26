#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量评分与校验脚本
功能：四维度自动化评分与修正建议生成
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class QualityScore:
    """质量评分数据结构"""
    evidence_score: float  # 有根据性（满分40）
    relevance_score: float  # 相关性（满分20）
    structure_score: float  # 结构合规性（满分20）
    interpretability_score: float  # 可解释性（满分20）
    total_score: float  # 总分（满分100）
    feedback: List[str]  # 修正建议列表


class QualityChecker:
    """质量检查器"""

    # 四维结构关键词
    FOUR_DIMENSION_KEYWORDS = {
        "core_definition": ["核心本体", "属概念", "种差", "定义"],
        "technical_principles": ["技术原理", "理化属性", "参数", "原理"],
        "applications": ["应用场景", "价值", "痛点", "受众"],
        "boundary": ["边界", "口径", "包含", "不包含"]
    }

    # 溯源标注正则表达式（匹配编号格式：[1][2][3]）
    SOURCE_PATTERN = re.compile(r'\[\d+\]')

    # 模糊词汇列表
    UNCERTAIN_WORDS = ["也许", "大概", "可能", "或许", "估计", "应该", "差不多", "约", "左右", "大约"]

    def __init__(self, threshold: float = 85.0):
        """
        初始化质量检查器

        Args:
            threshold: 质量阈值（默认85分）
        """
        self.threshold = threshold

    def check_evidence(self, report_text: str) -> Tuple[float, List[str]]:
        """
        检查有根据性（满分40分）

        Args:
            report_text: 报告文本

        Returns:
            评分和反馈列表
        """
        score = 0.0
        feedback = []

        # 1. 检查溯源标注（20分）- 检查关键论点是否标注
        source_matches = self.SOURCE_PATTERN.findall(report_text)
        if len(source_matches) >= 3:  # 融合格式通常3-5处标注即可
            score += 20
        elif len(source_matches) >= 2:
            score += 15
            feedback.append("溯源标注较少，建议增加关键论点的来源标注")
        else:
            score += 10
            feedback.append("溯源标注严重不足，必须为所有关键论点添加来源")

        # 2. 检查关键论点标注（10分）- 检查技术参数、法规标准、行业共识
        # 检查技术参数标注
        tech_param_pattern = re.compile(r'\b\d+\.?\d*\s*(?:度|米|尼特|Hz|nm|℃|V|W|Wh|kg|g|mg|mL|L|%|伏特|瓦特|赫兹|纳米|摄氏度|伏|瓦|瓦时|千克|克|毫克|毫升|升)\b')
        tech_params = tech_param_pattern.findall(report_text)
        
        # 检查法规标准引用
        std_pattern = re.compile(r'\b(?:GB/T|ISO|IEC|USP|CN|专利|药典|CAS号|专利号)\b')
        std_refs = std_pattern.findall(report_text)
        
        # 检查行业共识性结论
        consensus_pattern = re.compile(r'(?:主流|普遍|共识|核心|主要)\s*(?:技术路线|应用|方案|方法)')
        consensus_refs = consensus_pattern.findall(report_text)
        
        total_key_points = len(tech_params) + len(std_refs) + len(consensus_refs)
        
        if total_key_points > 0:
            # 检查这些关键论点是否有溯源标注
            annotated_points = 0
            for param in tech_params:
                param_pos = report_text.find(param)
                context = report_text[max(0, param_pos - 30):param_pos + len(param) + 30]
                if self.SOURCE_PATTERN.search(context):
                    annotated_points += 1
            
            if annotated_points / len(tech_params) >= 0.8 if tech_params else True:
                score += 10
            elif annotated_points / len(tech_params) >= 0.5 if tech_params else False:
                score += 7
                feedback.append("部分技术参数缺少溯源标注，请补充")
            else:
                score += 5
                feedback.append("大多数技术参数缺少溯源标注，必须补充")
        else:
            feedback.append("报告中未发现技术参数、法规标准或行业共识，建议补充")

        # 3. 检查模糊词汇（10分）
        uncertain_count = 0
        for word in self.UNCERTAIN_WORDS:
            uncertain_count += report_text.count(word)

        if uncertain_count == 0:
            score += 10
        elif uncertain_count <= 2:
            score += 7
            feedback.append(f"存在{uncertain_count}处模糊词汇，建议删除或替换为确定表述")
        else:
            score += 4
            feedback.append(f"存在{uncertain_count}处模糊词汇，必须删除所有模糊表述")

        return score, feedback

    def check_relevance(self, report_text: str, seed_word: str) -> Tuple[float, List[str]]:
        """
        检查相关性（满分20分）

        Args:
            report_text: 报告文本
            seed_word: 种子词

        Returns:
            评分和反馈列表
        """
        score = 0.0
        feedback = []

        # 1. 检查种子词出现频率（10分）
        seed_count = report_text.count(seed_word)
        if seed_count >= 5:
            score += 10
        elif seed_count >= 3:
            score += 7
            feedback.append("种子词出现频率较低，建议增加核心关键词")
        else:
            score += 4
            feedback.append("种子词出现频率过低，内容可能跑题")

        # 2. 检查是否偏离主题（10分）
        # 通过检查关键词相关性来判断
        text_lower = report_text.lower()

        # 检查是否存在与种子词无关的长段落
        paragraphs = report_text.split('\n')
        irrelevant_paras = 0

        for para in paragraphs:
            if len(para) > 100:  # 只检查较长的段落
                if seed_word not in para:
                    irrelevant_paras += 1

        if irrelevant_paras == 0:
            score += 10
        elif irrelevant_paras <= 1:
            score += 7
            feedback.append("存在1个段落可能偏离主题，建议检查")
        else:
            score += 4
            feedback.append(f"存在{irrelevant_paras}个段落可能偏离主题，需要检查相关性")

        return score, feedback

    def check_structure(self, report_text: str) -> Tuple[float, List[str]]:
        """
        检查结构合规性（满分20分）

        Args:
            report_text: 报告文本

        Returns:
            评分和反馈列表
        """
        score = 0.0
        feedback = []

        # 1. 检查融合格式完整性（12分）- 检查是否包含四维结构的关键要素
        required_elements = {
            "属概念": ["是一种", "属于", "是"],
            "技术参数": ["视场角", "CAS号", "分子量", "熔点", "电压", "能量密度"],
            "应用场景": ["应用于", "针对", "服务于", "主要应用于"],
            "边界划定": ["包含", "不包含"]
        }
        
        found_elements = 0
        for element_name, keywords in required_elements.items():
            if any(keyword in report_text for keyword in keywords):
                found_elements += 1
        
        if found_elements == 4:
            score += 12
        elif found_elements == 3:
            score += 8
            feedback.append(f"缺少{4-found_elements}个关键要素，请补充")
        elif found_elements == 2:
            score += 4
            feedback.append(f"缺少{4-found_elements}个关键要素，结构不完整")
        else:
            feedback.append("缺少大多数关键要素，结构严重不完整")

        # 2. 检查标题格式（4分）
        if "## " in report_text:
            score += 4
        else:
            feedback.append("缺少Markdown标题格式")

        # 3. 检查输出格式规范（4分）- 检查分类层级、统计口径和溯源来源
        required_fields = ["分类层级", "统计口径", "溯源来源"]
        found_fields = sum(1 for field in required_fields if field in report_text)

        if found_fields == 3:
            score += 4
        elif found_fields == 2:
            score += 2
            feedback.append("缺少分类层级、统计口径或溯源来源字段")
        else:
            feedback.append("缺少分类层级、统计口径或溯源来源字段")

        return score, feedback

    def check_interpretability(self, report_text: str) -> Tuple[float, List[str]]:
        """
        检查可解释性（满分20分）

        Args:
            report_text: 报告文本

        Returns:
            评分和反馈列表
        """
        score = 0.0
        feedback = []

        # 1. 检查语句清晰度（8分）
        # 检查过长的句子
        sentences = re.split(r'[。！？\n]', report_text)
        long_sentences = [s for s in sentences if len(s) > 200]

        if not long_sentences:
            score += 8
        elif len(long_sentences) <= 2:
            score += 6
            feedback.append(f"存在{len(long_sentences)}个过长句子，建议拆分")
        else:
            score += 4
            feedback.append(f"存在{len(long_sentences)}个过长句子，需要拆分以提高可读性")

        # 2. 检查术语解释（6分）
        # 检查是否使用了过多专业术语而未解释
        technical_terms = re.findall(r'[A-Z]{2,}|[a-z]+[A-Z][a-z]+', report_text)  # 匹配驼峰命名和全大写缩写
        if len(technical_terms) > 5:
            score += 3
            feedback.append("存在较多专业术语，建议增加解释说明")
        else:
            score += 6

        # 3. 检查逻辑连贯性（6分）
        # 检查段落间的过渡词
        transition_words = ["因此", "然而", "此外", "同时", "综上所述", "具体而言"]
        transition_count = sum(report_text.count(word) for word in transition_words)

        if transition_count >= 3:
            score += 6
        elif transition_count >= 1:
            score += 4
            feedback.append("逻辑连接词较少，建议增加过渡以提高连贯性")
        else:
            score += 2
            feedback.append("缺乏逻辑连接词，表述可能不够连贯")

        return score, feedback

    def evaluate(self, report_text: str, seed_word: str) -> QualityScore:
        """
        执行质量评估

        Args:
            report_text: 报告文本
            seed_word: 种子词

        Returns:
            质量评分对象
        """
        # 四维度评分
        evidence_score, evidence_feedback = self.check_evidence(report_text)
        relevance_score, relevance_feedback = self.check_relevance(report_text, seed_word)
        structure_score, structure_feedback = self.check_structure(report_text)
        interpretability_score, interpretability_feedback = self.check_interpretability(report_text)

        # 计算总分
        total_score = evidence_score + relevance_score + structure_score + interpretability_score

        # 合并反馈
        all_feedback = evidence_feedback + relevance_feedback + structure_feedback + interpretability_feedback

        return QualityScore(
            evidence_score=evidence_score,
            relevance_score=relevance_score,
            structure_score=structure_score,
            interpretability_score=interpretability_score,
            total_score=total_score,
            feedback=all_feedback
        )

    def should_revise(self, score: QualityScore) -> bool:
        """
        判断是否需要修正

        Args:
            score: 质量评分对象

        Returns:
            是否需要修正
        """
        return score.total_score < self.threshold


def main():
    """
    主函数示例
    """
    import argparse

    parser = argparse.ArgumentParser(description="质量评分与校验")
    parser.add_argument("--input", required=True, help="输入文件路径（Markdown格式）")
    parser.add_argument("--seed-word", required=True, help="种子词")
    parser.add_argument("--threshold", type=float, default=85.0, help="质量阈值")
    parser.add_argument("--output", default="quality_report.json", help="输出文件路径")

    args = parser.parse_args()

    # 读取报告文本
    with open(args.input, 'r', encoding='utf-8') as f:
        report_text = f.read()

    # 创建质量检查器并执行评估
    checker = QualityChecker(threshold=args.threshold)
    score = checker.evaluate(report_text, args.seed_word)

    # 输出质量报告
    output_data = {
        "scores": {
            "evidence": score.evidence_score,
            "relevance": score.relevance_score,
            "structure": score.structure_score,
            "interpretability": score.interpretability_score,
            "total": score.total_score
        },
        "threshold": args.threshold,
        "passed": score.total_score >= args.threshold,
        "feedback": score.feedback
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"质量评估完成")
    print(f"总分: {score.total_score:.1f}/100")
    print(f"是否通过: {'是' if score.total_score >= args.threshold else '否'}")
    if score.feedback:
        print(f"\n修正建议:")
        for i, feedback in enumerate(score.feedback, 1):
            print(f"{i}. {feedback}")


if __name__ == "__main__":
    main()
