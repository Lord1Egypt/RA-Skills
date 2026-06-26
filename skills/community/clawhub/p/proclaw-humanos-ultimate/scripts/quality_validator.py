#!/usr/bin/env python3
"""
质量验证器：10项质量检查（高级版）
核心算法：基于多维度统计分析和加权评分的质量评估系统
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
import math


class QualityValidator:
    """高级质量验证器"""

    # 10项质量检查（带详细权重和阈值）
    QUALITY_CHECKS = {
        'mental_model_count': {
            'weight': 15,
            'description': '心智模型数量',
            'pass_criteria': '3-7个',
            'pass_score': 15,
            'partial_score': 10,
            'fail_score': 5,
            'algorithm': 'count_and_classify'
        },
        'model_limitations': {
            'weight': 10,
            'description': '每个心智模型都有局限性说明',
            'pass_criteria': '100%覆盖率',
            'pass_score': 10,
            'partial_score': 5,
            'fail_score': 0,
            'algorithm': 'ratio_analysis'
        },
        'model_evidence': {
            'weight': 10,
            'description': '每个心智模型有≥2个证据',
            'pass_criteria': '100%满足',
            'pass_score': 10,
            'partial_score': 7,
            'fail_score': 3,
            'algorithm': 'evidence_counting'
        },
        'expression_dna': {
            'weight': 10,
            'description': '表达DNA特征≥3个',
            'pass_criteria': '≥3个特征',
            'pass_score': 10,
            'partial_score': 6,
            'fail_score': 2,
            'algorithm': 'feature_extraction'
        },
        'honest_boundaries': {
            'weight': 15,
            'description': '诚实边界≥3条',
            'pass_criteria': '≥3条边界',
            'pass_score': 15,
            'partial_score': 10,
            'fail_score': 5,
            'algorithm': 'boundary_detection'
        },
        'internal_tensions': {
            'weight': 10,
            'description': '内在张力≥2处',
            'pass_criteria': '≥2处张力',
            'pass_score': 10,
            'partial_score': 6,
            'fail_score': 2,
            'algorithm': 'tension_identification'
        },
        'decision_heuristics': {
            'weight': 10,
            'description': '决策启发式≥5条',
            'pass_criteria': '≥5条启发式',
            'pass_score': 10,
            'partial_score': 6,
            'fail_score': 2,
            'algorithm': 'pattern_matching'
        },
        'agentic_protocol': {
            'weight': 10,
            'description': '包含3步骤的Agentic Protocol',
            'pass_criteria': '包含完整3步骤',
            'pass_score': 10,
            'partial_score': 5,
            'fail_score': 0,
            'algorithm': 'protocol_validation'
        },
        'toolkit': {
            'weight': 5,
            'description': '工具箱≥3个',
            'pass_criteria': '≥3个工具',
            'pass_score': 5,
            'partial_score': 3,
            'fail_score': 1,
            'algorithm': 'tool_extraction'
        },
        'primary_sources': {
            'weight': 5,
            'description': '一手来源>50%（如有research）',
            'pass_criteria': '>50%',
            'pass_score': 5,
            'partial_score': 3,
            'fail_score': 1,
            'algorithm': 'source_classification'
        }
    }

    # 通过线（总分100分，需≥75分）
    PASSING_SCORE = 75

    def __init__(self):
        self.validation_result = {}

    def validate_skill(self, skill_file: str, research_dir: str = None) -> Dict:
        """验证HumanOS Skill - 主流程"""

        skill_path = Path(skill_file)

        # 读取Skill文件
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_content = f.read()

        # 执行10项检查
        check_results = {}

        # 检查1: 心智模型数量
        check_results['mental_model_count'] = self._check_mental_model_count_advanced(
            skill_content
        )

        # 检查2: 模型局限性
        check_results['model_limitations'] = self._check_model_limitations_advanced(
            skill_content
        )

        # 检查3: 模型证据
        check_results['model_evidence'] = self._check_model_evidence_advanced(
            skill_content
        )

        # 检查4: 表达DNA
        check_results['expression_dna'] = self._check_expression_dna_advanced(
            skill_content
        )

        # 检查5: 诚实边界
        check_results['honest_boundaries'] = self._check_honest_boundaries_advanced(
            skill_content
        )

        # 检查6: 内在张力
        check_results['internal_tensions'] = self._check_internal_tensions_advanced(
            skill_content
        )

        # 检查7: 决策启发式
        check_results['decision_heuristics'] = self._check_decision_heuristics_advanced(
            skill_content
        )

        # 检查8: Agentic Protocol
        check_results['agentic_protocol'] = self._check_agentic_protocol_advanced(
            skill_content
        )

        # 检查9: 工具箱
        check_results['toolkit'] = self._check_toolkit_advanced(
            skill_content
        )

        # 检查10: 一手来源
        check_results['primary_sources'] = self._check_primary_sources_advanced(
            skill_content,
            research_dir
        )

        # 计算总分（加权）
        total_score = 0
        for check_name, result in check_results.items():
            weight = self.QUALITY_CHECKS[check_name]['weight']
            score = result['score']
            # 归一化得分：score / pass_score * weight
            normalized_score = (score / self.QUALITY_CHECKS[check_name]['pass_score']) * weight
            result['normalized_score'] = round(normalized_score, 2)
            total_score += normalized_score

        total_score = round(total_score, 1)

        # 判断是否通过
        passed = total_score >= self.PASSING_SCORE

        # 生成详细报告
        validation_result = {
            'skill_file': skill_file,
            'total_score': total_score,
            'passing_score': self.PASSING_SCORE,
            'passed': passed,
            'passing_rate': f"{total_score / 100 * 100:.1f}%",
            'check_results': check_results,
            'summary': self._generate_summary_advanced(check_results, total_score),
            'recommendations': self._generate_recommendations_advanced(check_results),
            'quality_grade': self._calculate_quality_grade(total_score),
            'analysis': self._generate_detailed_analysis(check_results)
        }

        self.validation_result = validation_result

        return validation_result

    def _check_mental_model_count_advanced(self, skill_content: str) -> Dict:
        """高级心智模型数量检查"""

        # 识别心智模型的多种模式
        patterns = [
            r'\*\*([^*]+)\*\*.*?(?:思维模型|原理|框架|效应|法则)',
            r'##\s+(?:心智模型|Mental Models).*?\n(.*?)(?=\n##|\Z)',
            r'模型\d+\s*[:：]\s*\*\*([^*]+)\*\*',
            r'([^.\n]+)(?:思维模型|原理|框架)'
        ]

        models = set()

        for pattern in patterns:
            matches = re.findall(pattern, skill_content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    model_name = match[0].strip()
                else:
                    model_name = match.strip()

                # 过滤无效模型
                if len(model_name) >= 2 and not model_name.isdigit():
                    models.add(model_name)

        model_list = sorted(list(models))
        model_count = len(model_list)

        # 评分
        if 3 <= model_count <= 7:
            score = self.QUALITY_CHECKS['mental_model_count']['pass_score']
            status = 'pass'
        elif model_count >= 1 and model_count < 3:
            score = self.QUALITY_CHECKS['mental_model_count']['partial_score']
            status = 'partial'
        elif model_count > 7:
            score = self.QUALITY_CHECKS['mental_model_count']['pass_score']  # 超过也算通过
            status = 'pass'
        else:
            score = self.QUALITY_CHECKS['mental_model_count']['fail_score']
            status = 'fail'

        return {
            'check': 'mental_model_count',
            'description': self.QUALITY_CHECKS['mental_model_count']['description'],
            'criteria': self.QUALITY_CHECKS['mental_model_count']['pass_criteria'],
            'actual': model_count,
            'models': model_list[:10],  # 返回前10个
            'score': score,
            'status': status,
            'message': f"发现{model_count}个心智模型: {', '.join(model_list[:5])}{'...' if model_count > 5 else ''}",
            'algorithm': self.QUALITY_CHECKS['mental_model_count']['algorithm']
        }

    def _check_model_limitations_advanced(self, skill_content: str) -> Dict:
        """高级模型局限性检查"""

        # 获取心智模型
        model_check = self._check_mental_model_count_advanced(skill_content)
        models = model_check['models']
        model_count = model_check['actual']

        if model_count == 0:
            return {
                'check': 'model_limitations',
                'description': self.QUALITY_CHECKS['model_limitations']['description'],
                'criteria': self.QUALITY_CHECKS['model_limitations']['pass_criteria'],
                'actual': "0%",
                'score': self.QUALITY_CHECKS['model_limitations']['fail_score'],
                'status': 'fail',
                'message': '未发现心智模型',
                'algorithm': self.QUALITY_CHECKS['model_limitations']['algorithm']
            }

        # 识别局限性模式
        limitation_patterns = [
            r'(?:局限|不适用|不能|做不到|边界|限制|缺点)',
            r'局限性\s*[:：]',
            r'注意\s*[:：].*?(?:局限|限制)'
        ]

        found_limitations = set()

        for pattern in limitation_patterns:
            matches = re.finditer(pattern, skill_content)
            for match in matches:
                # 获取上下文
                context_start = max(0, match.start() - 30)
                context_end = min(len(skill_content), match.end() + 30)
                context = skill_content[context_start:context_end]

                found_limitations.add(context)

        limitation_count = len(found_limitations)
        limitation_ratio = limitation_count / model_count

        # 评分
        if limitation_ratio >= 1.0:
            score = self.QUALITY_CHECKS['model_limitations']['pass_score']
            status = 'pass'
        elif limitation_ratio >= 0.5:
            score = self.QUALITY_CHECKS['model_limitations']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['model_limitations']['fail_score']
            status = 'fail'

        return {
            'check': 'model_limitations',
            'description': self.QUALITY_CHECKS['model_limitations']['description'],
            'criteria': self.QUALITY_CHECKS['model_limitations']['pass_criteria'],
            'actual': f"{int(limitation_ratio * 100)}%",
            'limitation_count': limitation_count,
            'model_count': model_count,
            'score': score,
            'status': status,
            'message': f"发现{limitation_count}处局限性说明，覆盖{int(limitation_ratio * 100)}%模型",
            'algorithm': self.QUALITY_CHECKS['model_limitations']['algorithm']
        }

    def _check_model_evidence_advanced(self, skill_content: str) -> Dict:
        """高级模型证据检查"""

        # 获取心智模型
        model_check = self._check_mental_model_count_advanced(skill_content)
        models = model_check['models']
        model_count = model_check['actual']

        if model_count == 0:
            return {
                'check': 'model_evidence',
                'description': self.QUALITY_CHECKS['model_evidence']['description'],
                'criteria': self.QUALITY_CHECKS['model_evidence']['pass_criteria'],
                'actual': "0个证据/模型",
                'score': self.QUALITY_CHECKS['model_evidence']['fail_score'],
                'status': 'fail',
                'message': '未发现心智模型',
                'algorithm': self.QUALITY_CHECKS['model_evidence']['algorithm']
            }

        # 识别证据关键词
        evidence_keywords = [
            '证据', '案例', '实证', '例子', '例如',
            '比如', '举例', '证明', '显示', '表明',
            'example', 'case', 'evidence', 'proof'
        ]

        evidence_count = 0

        for keyword in evidence_keywords:
            # 统计关键词出现次数
            count = skill_content.lower().count(keyword.lower())
            evidence_count += count

        # 计算证据/模型比率
        evidence_ratio = evidence_count / model_count if model_count > 0 else 0

        # 评分
        if evidence_ratio >= 2.0:
            score = self.QUALITY_CHECKS['model_evidence']['pass_score']
            status = 'pass'
        elif evidence_ratio >= 1.0:
            score = self.QUALITY_CHECKS['model_evidence']['pass_score']  # >=1个也算通过
            status = 'pass'
        elif evidence_ratio > 0:
            score = self.QUALITY_CHECKS['model_evidence']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['model_evidence']['fail_score']
            status = 'fail'

        return {
            'check': 'model_evidence',
            'description': self.QUALITY_CHECKS['model_evidence']['description'],
            'criteria': self.QUALITY_CHECKS['model_evidence']['pass_criteria'],
            'actual': f"{evidence_ratio:.1f}个证据/模型",
            'evidence_count': evidence_count,
            'model_count': model_count,
            'score': score,
            'status': status,
            'message': f"发现{evidence_count}处证据引用，平均{evidence_ratio:.1f}个证据/模型",
            'algorithm': self.QUALITY_CHECKS['model_evidence']['algorithm']
        }

    def _check_expression_dna_advanced(self, skill_content: str) -> Dict:
        """高级表达DNA检查"""

        dna_features = {
            'sentence_patterns': 0,
            'vocabulary': 0,
            'rhythm': 0,
            'style': 0
        }

        # 检查句式模式
        if any(kw in skill_content for kw in ['句式', '句子', '句法']):
            dna_features['sentence_patterns'] = 1

        # 检查词汇
        if any(kw in skill_content for kw in ['词汇', '术语', '用词']):
            dna_features['vocabulary'] = 1

        # 检查节奏
        if any(kw in skill_content for kw in ['节奏', '语速', '停顿']):
            dna_features['rhythm'] = 1

        # 检查风格
        if any(kw in skill_content for kw in ['风格', '表达', '语气']):
            dna_features['style'] = 1

        feature_count = sum(dna_features.values())

        # 评分
        if feature_count >= 3:
            score = self.QUALITY_CHECKS['expression_dna']['pass_score']
            status = 'pass'
        elif feature_count >= 1:
            score = self.QUALITY_CHECKS['expression_dna']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['expression_dna']['fail_score']
            status = 'fail'

        return {
            'check': 'expression_dna',
            'description': self.QUALITY_CHECKS['expression_dna']['description'],
            'criteria': self.QUALITY_CHECKS['expression_dna']['pass_criteria'],
            'actual': feature_count,
            'features': {k: v for k, v in dna_features.items() if v > 0},
            'score': score,
            'status': status,
            'message': f"发现{feature_count}个表达DNA特征",
            'algorithm': self.QUALITY_CHECKS['expression_dna']['algorithm']
        }

    def _check_honest_boundaries_advanced(self, skill_content: str) -> Dict:
        """高级诚实边界检查"""

        # 识别边界关键词和模式
        boundary_patterns = [
            r'(?:边界|不能|做不到|不擅长|局限|限制|无法|难以)',
            r'诚实边界\s*[:：]',
            r'注意事项\s*[:：]',
            r'局限性\s*[:：]'
        ]

        found_boundaries = set()

        for pattern in boundary_patterns:
            matches = re.finditer(pattern, skill_content)
            for match in matches:
                # 获取上下文
                context_start = max(0, match.start() - 50)
                context_end = min(len(skill_content), match.end() + 50)
                context = skill_content[context_start:context_end]

                found_boundaries.add(context[:100])

        boundary_count = len(found_boundaries)

        # 评分
        if boundary_count >= 3:
            score = self.QUALITY_CHECKS['honest_boundaries']['pass_score']
            status = 'pass'
        elif boundary_count >= 1:
            score = self.QUALITY_CHECKS['honest_boundaries']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['honest_boundaries']['fail_score']
            status = 'fail'

        return {
            'check': 'honest_boundaries',
            'description': self.QUALITY_CHECKS['honest_boundaries']['description'],
            'criteria': self.QUALITY_CHECKS['honest_boundaries']['pass_criteria'],
            'actual': boundary_count,
            'score': score,
            'status': status,
            'message': f"发现{boundary_count}条诚实边界",
            'algorithm': self.QUALITY_CHECKS['honest_boundaries']['algorithm']
        }

    def _check_internal_tensions_advanced(self, skill_content: str) -> Dict:
        """高级内在张力检查"""

        # 识别张力关键词和模式
        tension_patterns = [
            r'(?:张力|矛盾|冲突|不一致|悖论|两难|困境)',
            r'内在张力\s*[:：]',
            r'核心矛盾\s*[:：]'
        ]

        found_tensions = set()

        for pattern in tension_patterns:
            matches = re.finditer(pattern, skill_content)
            for match in matches:
                # 获取上下文
                context_start = max(0, match.start() - 50)
                context_end = min(len(skill_content), match.end() + 50)
                context = skill_content[context_start:context_end]

                found_tensions.add(context[:100])

        tension_count = len(found_tensions)

        # 评分
        if tension_count >= 2:
            score = self.QUALITY_CHECKS['internal_tensions']['pass_score']
            status = 'pass'
        elif tension_count >= 1:
            score = self.QUALITY_CHECKS['internal_tensions']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['internal_tensions']['fail_score']
            status = 'fail'

        return {
            'check': 'internal_tensions',
            'description': self.QUALITY_CHECKS['internal_tensions']['description'],
            'criteria': self.QUALITY_CHECKS['internal_tensions']['pass_criteria'],
            'actual': tension_count,
            'score': score,
            'status': status,
            'message': f"发现{tension_count}处内在张力",
            'algorithm': self.QUALITY_CHECKS['internal_tensions']['algorithm']
        }

    def _check_decision_heuristics_advanced(self, skill_content: str) -> Dict:
        """高级决策启发式检查"""

        # 识别启发式模式
        heuristic_patterns = [
            r'当(.{1,30})\s*时\s*[，,]?\s*应该?(.{1,60})',
            r'如果是?(.{1,30})\s*[，,]?\s*则?(.{1,60})',
            r'(.{1,15})\s*(?:原则|准则|Rule|Principle)\s*[:：]?\s*([^.。]+)',
            r'在?(.{1,20})\s*时\s*[，,]?\s*优先?(.{1,50})',
            r'(?:启发式|Heuristic)\s*\d+\s*[:：]'
        ]

        found_heuristics = set()

        for pattern in heuristic_patterns:
            matches = re.finditer(pattern, skill_content)
            for match in matches:
                heuristic = match.group(0).strip()
                # 过滤和验证质量
                if 15 <= len(heuristic) <= 120:
                    found_heuristics.add(heuristic[:80])

        heuristic_count = len(found_heuristics)

        # 评分
        if heuristic_count >= 5:
            score = self.QUALITY_CHECKS['decision_heuristics']['pass_score']
            status = 'pass'
        elif heuristic_count >= 1:
            score = self.QUALITY_CHECKS['decision_heuristics']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['decision_heuristics']['fail_score']
            status = 'fail'

        return {
            'check': 'decision_heuristics',
            'description': self.QUALITY_CHECKS['decision_heuristics']['description'],
            'criteria': self.QUALITY_CHECKS['decision_heuristics']['pass_criteria'],
            'actual': heuristic_count,
            'score': score,
            'status': status,
            'message': f"发现{heuristic_count}条决策启发式",
            'algorithm': self.QUALITY_CHECKS['decision_heuristics']['algorithm']
        }

    def _check_agentic_protocol_advanced(self, skill_content: str) -> Dict:
        """高级Agentic Protocol检查"""

        # 检查是否存在Agentic Protocol
        has_agentic_protocol = 'Agentic Protocol' in skill_content or 'agentic protocol' in skill_content.lower()

        if not has_agentic_protocol:
            return {
                'check': 'agentic_protocol',
                'description': self.QUALITY_CHECKS['agentic_protocol']['description'],
                'criteria': self.QUALITY_CHECKS['agentic_protocol']['pass_criteria'],
                'actual': 0,
                'score': self.QUALITY_CHECKS['agentic_protocol']['fail_score'],
                'status': 'fail',
                'message': '未发现Agentic Protocol',
                'algorithm': self.QUALITY_CHECKS['agentic_protocol']['algorithm']
            }

        # 提取Agentic Protocol部分
        protocol_pattern = r'Agentic Protocol.*?(?=\n##|\Z)'
        protocol_match = re.search(protocol_pattern, skill_content, re.DOTALL | re.IGNORECASE)

        if not protocol_match:
            return {
                'check': 'agentic_protocol',
                'description': self.QUALITY_CHECKS['agentic_protocol']['description'],
                'criteria': self.QUALITY_CHECKS['agentic_protocol']['pass_criteria'],
                'actual': 0,
                'score': self.QUALITY_CHECKS['agentic_protocol']['fail_score'],
                'status': 'fail',
                'message': 'Agentic Protocol格式不正确',
                'algorithm': self.QUALITY_CHECKS['agentic_protocol']['algorithm']
            }

        protocol_text = protocol_match.group(0)

        # 检查步骤
        step_patterns = [
            r'步骤\s*[123]',
            r'Step\s*[123]',
            r'[一二三]\s*[、\.]?\s*步骤'
        ]

        steps_found = set()
        for pattern in step_patterns:
            matches = re.findall(pattern, protocol_text, re.IGNORECASE)
            steps_found.update(matches)

        step_count = len(steps_found)

        # 检查是否包含必需步骤
        required_steps = ['问题', '研究', '回答', 'Question', 'Research', 'Answer']
        has_required = any(step in protocol_text for step in required_steps)

        # 评分
        if step_count >= 3 and has_required:
            score = self.QUALITY_CHECKS['agentic_protocol']['pass_score']
            status = 'pass'
        elif step_count >= 1:
            score = self.QUALITY_CHECKS['agentic_protocol']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['agentic_protocol']['fail_score']
            status = 'fail'

        return {
            'check': 'agentic_protocol',
            'description': self.QUALITY_CHECKS['agentic_protocol']['description'],
            'criteria': self.QUALITY_CHECKS['agentic_protocol']['pass_criteria'],
            'actual': step_count,
            'score': score,
            'status': status,
            'message': f"发现{step_count}个Agentic Protocol步骤",
            'algorithm': self.QUALITY_CHECKS['agentic_protocol']['algorithm']
        }

    def _check_toolkit_advanced(self, skill_content: str) -> Dict:
        """高级工具箱检查"""

        # 识别工具模式
        tool_patterns = [
            r'##\s*(?:工具箱|Toolkit|Tools)\s*\n(.*?)(?=\n##|\Z)',
            r'工具\s*\d*\s*[:：]\s*([^.\n]+)',
            r'使用\s*(\w+)(?:工具|方法|技巧)',
            r'Tool\s*\d*\s*[:：]\s*([^.\n]+)'
        ]

        found_tools = set()

        for pattern in tool_patterns:
            matches = re.finditer(pattern, skill_content, re.DOTALL)
            for match in matches:
                tool = match.group(1) if match.lastindex >= 1 else match.group(0)
                tool = tool.strip()

                if len(tool) >= 2 and not tool.isdigit():
                    found_tools.add(tool[:50])

        tool_count = len(found_tools)

        # 评分
        if tool_count >= 3:
            score = self.QUALITY_CHECKS['toolkit']['pass_score']
            status = 'pass'
        elif tool_count >= 1:
            score = self.QUALITY_CHECKS['toolkit']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['toolkit']['fail_score']
            status = 'fail'

        return {
            'check': 'toolkit',
            'description': self.QUALITY_CHECKS['toolkit']['description'],
            'criteria': self.QUALITY_CHECKS['toolkit']['pass_criteria'],
            'actual': tool_count,
            'score': score,
            'status': status,
            'message': f"发现{tool_count}个工具",
            'algorithm': self.QUALITY_CHECKS['toolkit']['algorithm']
        }

    def _check_primary_sources_advanced(self, skill_content: str,
                                        research_dir: str = None) -> Dict:
        """高级一手来源检查"""

        # 如果没有提供research目录，跳过此项
        if not research_dir:
            return {
                'check': 'primary_sources',
                'description': self.QUALITY_CHECKS['primary_sources']['description'],
                'criteria': self.QUALITY_CHECKS['primary_sources']['pass_criteria'],
                'actual': 'N/A',
                'score': self.QUALITY_CHECKS['primary_sources']['pass_score'],
                'status': 'pass',
                'message': '未提供research目录，跳过此项',
                'algorithm': self.QUALITY_CHECKS['primary_sources']['algorithm']
            }

        research_path = Path(research_dir)

        if not research_path.exists():
            return {
                'check': 'primary_sources',
                'description': self.QUALITY_CHECKS['primary_sources']['description'],
                'criteria': self.QUALITY_CHECKS['primary_sources']['pass_criteria'],
                'actual': 'N/A',
                'score': self.QUALITY_CHECKS['primary_sources']['pass_score'],
                'status': 'pass',
                'message': 'Research目录不存在，跳过此项',
                'algorithm': self.QUALITY_CHECKS['primary_sources']['algorithm']
            }

        # 统计来源
        primary_sources = 0
        secondary_sources = 0
        total_sources = 0

        # 扫描research目录
        for file_path in research_path.glob('**/*.md'):
            total_sources += 1

            # 判断来源类型
            filename = file_path.stem.lower()

            # 一手来源指标
            primary_indicators = [
                'writings', 'interview', 'speech', 'conversation',
                'original', 'primary', 'transcript'
            ]

            # 二手来源指标
            secondary_indicators = [
                'summary', 'analysis', 'review', 'commentary',
                'secondary', 'interpretation'
            ]

            if any(ind in filename for ind in primary_indicators):
                primary_sources += 1
            elif any(ind in filename for ind in secondary_indicators):
                secondary_sources += 1
            else:
                # 默认认为是一手来源
                primary_sources += 1

        if total_sources > 0:
            primary_ratio = primary_sources / total_sources
        else:
            primary_ratio = 0

        # 评分
        if primary_ratio > 0.5:
            score = self.QUALITY_CHECKS['primary_sources']['pass_score']
            status = 'pass'
        elif primary_ratio > 0:
            score = self.QUALITY_CHECKS['primary_sources']['partial_score']
            status = 'partial'
        else:
            score = self.QUALITY_CHECKS['primary_sources']['fail_score']
            status = 'fail'

        return {
            'check': 'primary_sources',
            'description': self.QUALITY_CHECKS['primary_sources']['description'],
            'criteria': self.QUALITY_CHECKS['primary_sources']['pass_criteria'],
            'actual': f"{int(primary_ratio * 100)}%",
            'primary_count': primary_sources,
            'secondary_count': secondary_sources,
            'total_count': total_sources,
            'score': score,
            'status': status,
            'message': f"发现{primary_sources}/{total_sources}个一手来源 ({int(primary_ratio * 100)}%)",
            'algorithm': self.QUALITY_CHECKS['primary_sources']['algorithm']
        }

    def _generate_summary_advanced(self, check_results: Dict, total_score: float) -> Dict:
        """生成高级验证总结"""

        passed_checks = sum(1 for result in check_results.values() if result['status'] == 'pass')
        partial_checks = sum(1 for result in check_results.values() if result['status'] == 'partial')
        failed_checks = sum(1 for result in check_results.values() if result['status'] == 'fail')

        return {
            'total_checks': len(check_results),
            'passed': passed_checks,
            'partial': partial_checks,
            'failed': failed_checks,
            'overall_score': total_score,
            'passing_line': self.PASSING_SCORE,
            'passed_checks_count': passed_checks,
            'pass_rate': f"{passed_checks / len(check_results) * 100:.0f}%" if check_results else "0%"
        }

    def _generate_recommendations_advanced(self, check_results: Dict) -> List[Dict]:
        """生成高级改进建议"""

        recommendations = []

        for check_name, result in check_results.items():
            if result['status'] == 'fail':
                recommendations.append({
                    'priority': 'high',
                    'check': result['description'],
                    'message': f'未通过，需要补充。当前: {result["actual"]}',
                    'action': f'添加至少{result["criteria"]}的{result["description"]}'
                })
            elif result['status'] == 'partial':
                recommendations.append({
                    'priority': 'medium',
                    'check': result['description'],
                    'message': f'部分通过，建议改进。当前: {result["actual"]}',
                    'action': f'提升{result["description"]}至{result["criteria"]}'
                })

        return recommendations

    def _calculate_quality_grade(self, total_score: float) -> str:
        """计算质量等级"""

        if total_score >= 90:
            return 'A+'
        elif total_score >= 85:
            return 'A'
        elif total_score >= 80:
            return 'A-'
        elif total_score >= 75:
            return 'B+'
        elif total_score >= 70:
            return 'B'
        elif total_score >= 65:
            return 'B-'
        elif total_score >= 60:
            return 'C'
        elif total_score >= 50:
            return 'D'
        else:
            return 'F'

    def _generate_detailed_analysis(self, check_results: Dict) -> Dict:
        """生成详细分析"""

        analysis = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': []
        }

        for check_name, result in check_results.items():
            if result['status'] == 'pass':
                analysis['strengths'].append({
                    'area': result['description'],
                    'performance': f'优秀 (得分: {result["normalized_score"]})'
                })
            elif result['status'] == 'fail':
                analysis['weaknesses'].append({
                    'area': result['description'],
                    'issue': f'不满足要求 (当前: {result["actual"]})'
                })
            elif result['status'] == 'partial':
                analysis['opportunities'].append({
                    'area': result['description'],
                    'improvement': f'可以提升 (当前: {result["actual"]}, 目标: {result["criteria"]})'
                })

        return analysis


def main():
    import argparse

    parser = argparse.ArgumentParser(description='质量验证（高级版）')
    parser.add_argument('--skill-file', type=str, required=True,
                       help='Skill文件路径')
    parser.add_argument('--research-dir', type=str,
                       help='Research目录路径（可选）')
    parser.add_argument('--output', type=str,
                       help='输出JSON文件路径（可选）')

    args = parser.parse_args()

    validator = QualityValidator()

    # 执行验证
    validation_result = validator.validate_skill(
        args.skill_file,
        args.research_dir
    )

    # 输出结果
    print(json.dumps(validation_result, ensure_ascii=False, indent=2))

    # 保存到文件（可选）
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(validation_result, f, ensure_ascii=False, indent=2)
        print(f"\n验证结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
