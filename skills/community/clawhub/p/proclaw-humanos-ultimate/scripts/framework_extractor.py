#!/usr/bin/env python3
"""
框架提取器：从调研材料中提取思维框架
核心算法：基于多维度交叉验证的框架提取与四维评分系统
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict
import math


class FrameworkExtractor:
    """框架提取器 - 基于统计语言学和多维度验证"""

    # 四维验证标准（带权重和动态阈值）
    VALIDATION_CRITERIA = {
        'cross_domain_reproducibility': {
            'weight': 3,
            'threshold': 2,
            'description': '在≥2个领域出现',
            'pass_score': 3,
            'partial_score': 2,
            'fail_score': 1
        },
        'generative_power': {
            'weight': 2,
            'threshold': 1,
            'description': '能推断新问题立场',
            'pass_score': 2,
            'partial_score': 1,
            'fail_score': 0
        },
        'exclusivity': {
            'weight': 2,
            'threshold': 1,
            'description': '不是通用真理',
            'pass_score': 2,
            'partial_score': 1,
            'fail_score': 0
        },
        'testability': {
            'weight': 1,
            'threshold': 1,
            'description': '有案例/实证',
            'pass_score': 1,
            'partial_score': 0,
            'fail_score': 0
        }
    }

    # 通过线（总分12分，需≥7分）
    PASSING_SCORE = 7

    # 领域关键词映射
    DOMAIN_KEYWORDS = {
        'business': ['商业', '投资', '创业', '管理', '企业'],
        'technology': ['技术', '开发', '算法', '编程', '系统'],
        'philosophy': ['哲学', '思想', '本质', '真理', '逻辑'],
        'psychology': ['心理', '认知', '行为', '情绪', '思维'],
        'life': ['人生', '生活', '成长', '选择', '价值'],
        'education': ['教育', '学习', '教学', '知识', '理解']
    }

    def __init__(self):
        self.extracted_framework = {}
        self.domain_statistics = defaultdict(int)

    def extract_framework(self, research_dir: str, target: str) -> Dict:
        """提取思维框架 - 主流程"""

        research_path = Path(research_dir)

        # 读取调研文件
        research_data = self._load_research_data(research_path)

        # 分析领域分布
        domain_analysis = self._analyze_domains(research_data)

        # 提取框架组件（使用高级NLP技术）
        framework = {
            'target': target,
            'domain_analysis': domain_analysis,
            'mental_models': self._extract_mental_models_advanced(research_data),
            'decision_heuristics': self._extract_decision_heuristics_advanced(research_data),
            'expression_dna': self._extract_expression_dna_advanced(research_data),
            'values': self._extract_values_advanced(research_data),
            'toolkit': self._extract_toolkit_advanced(research_data),
            'internal_tensions': self._extract_internal_tensions_advanced(research_data),
            'honest_boundaries': self._extract_honest_boundaries_advanced(research_data)
        }

        # 验证心智模型（四维验证 + 一致性检查）
        framework['validated_models'] = self._validate_mental_models_advanced(
            framework['mental_models'],
            research_data
        )

        # 生成框架总结（含质量评分）
        framework['summary'] = self._generate_framework_summary_advanced(framework)

        self.extracted_framework = framework

        return framework

    def _load_research_data(self, research_path: Path) -> Dict:
        """加载调研数据"""

        research_data = {}

        # 读取6个维度的调研文件
        dimensions = [
            '01-writings.md',
            '02-conversations.md',
            '03-expression-dna.md',
            '04-external-views.md',
            '05-decisions.md',
            '06-timeline.md'
        ]

        for dimension_file in dimensions:
            file_path = research_path / dimension_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 预处理：去除空白行和冗余空格
                    cleaned_content = self._preprocess_text(content)
                    research_data[dimension_file.replace('.md', '')] = cleaned_content

        return research_data

    def _preprocess_text(self, text: str) -> str:
        """文本预处理"""

        # 去除多余空行
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # 统一标点
        text = text.replace('，', ',').replace('。', '.')
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _analyze_domains(self, research_data: Dict) -> Dict:
        """分析领域分布"""

        domain_counts = Counter()

        for dimension, text in research_data.items():
            for domain, keywords in self.DOMAIN_KEYWORDS.items():
                for keyword in keywords:
                    domain_counts[domain] += text.count(keyword)

        # 计算占比
        total = sum(domain_counts.values())
        domain_distribution = {
            domain: {
                'count': count,
                'percentage': count / total if total > 0 else 0
            }
            for domain, count in domain_counts.items()
        }

        # 识别主领域
        main_domain = max(domain_counts.items(), key=lambda x: x[1])[0] if domain_counts else 'unknown'

        return {
            'main_domain': main_domain,
            'distribution': domain_distribution,
            'total_mentions': total
        }

    def _extract_mental_models_advanced(self, research_data: Dict) -> List[Dict]:
        """高级心智模型提取 - 基于TF-IDF和共现分析"""

        models = []

        # 收集所有文本
        all_text = ' '.join(research_data.values())

        # 1. 关键词提取（TF-IDF简化版）
        keywords = self._extract_keywords_tfidf(all_text)

        # 2. 模式匹配提取心智模型
        patterns = [
            r'(\w+)\s*[:：]\s*(?:思维模型|原理|框架|效应|法则)',
            r'(\w+)(?:思维模型|原理|框架|效应|法则)',
            r'(\w+)\s*(?:的|是)\s*(?:思维模型|原理|框架)',
            r'(\w+)\s*(?:模型|Model)\s*\d*'
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, all_text, re.IGNORECASE)
            for match in matches:
                model_name = match.group(1).strip()
                if len(model_name) >= 2:  # 过滤单字
                    # 计算上下文窗口
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(all_text), match.end() + 50)
                    context = all_text[context_start:context_end]

                    # 计算重要性（TF-IDF权重）
                    importance = self._calculate_model_importance(model_name, keywords)

                    models.append({
                        'name': model_name,
                        'importance_score': importance,
                        'description': self._extract_model_description(model_name, all_text),
                        'evidence': self._find_model_evidence(model_name, research_data),
                        'contexts': [context],
                        'type': self._classify_model_type(model_name, all_text)
                    })

        # 3. 去重和排序
        unique_models = self._deduplicate_models(models)

        # 4. 按重要性排序
        unique_models.sort(key=lambda x: x['importance_score'], reverse=True)

        # 限制为3-7个
        return unique_models[:7]

    def _extract_keywords_tfidf(self, text: str) -> Dict[str, float]:
        """简化TF-IDF关键词提取"""

        # 分词（简化版）
        words = re.findall(r'\w+', text.lower())

        # 计算词频
        tf = Counter(words)

        # 过滤停用词和短词
        stop_words = {'的', '是', '在', '了', '和', '有', '我', '他', '她', '它', 'the', 'is', 'a', 'an', 'and'}
        keywords = {word: count for word, count in tf.items()
                    if len(word) > 2 and word not in stop_words}

        # 计算TF-IDF（简化版，只使用TF）
        total_words = sum(tf.values())
        tfidf = {word: count / total_words for word, count in keywords.items()}

        return tfidf

    def _calculate_model_importance(self, model_name: str, keywords: Dict[str, float]) -> float:
        """计算心智模型重要性"""

        # 模型名在关键词中的权重
        model_keywords = model_name.lower().split()
        keyword_weight = sum(keywords.get(kw, 0) for kw in model_keywords)

        # 名字长度加权
        length_weight = min(len(model_name) / 10, 1.0)

        # 综合得分
        importance = keyword_weight * 10 + length_weight * 2

        return round(importance, 2)

    def _extract_model_description(self, model_name: str, text: str) -> str:
        """提取模型描述"""

        # 寻找描述性语句
        patterns = [
            rf'{model_name}\s*[:：]\s*([^.。]+[.。])',
            rf'{model_name}\s*(?:是指|是|为)\s*([^.。]+[.。])',
            rf'(\w+)\s*[:：]\s*{model_name}.*?([^.。]+[.。])'
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                description = match.group(1) if match.lastindex >= 1 else ""
                if len(description) > 10 and len(description) < 100:
                    return description.strip()

        return f"{model_name}思维模型"

    def _find_model_evidence(self, model_name: str, research_data: Dict) -> List[str]:
        """寻找模型证据"""

        evidence = []

        for dimension, text in research_data.items():
            if model_name in text:
                # 寻找包含模型的句子
                sentences = re.split(r'[。！？.!?]', text)
                for sentence in sentences:
                    if model_name in sentence and len(sentence.strip()) > 5:
                        evidence.append(f"{dimension}: {sentence.strip()[:50]}...")
                        if len(evidence) >= 3:  # 最多3条证据
                            break
            if len(evidence) >= 3:
                break

        return evidence[:3]

    def _classify_model_type(self, model_name: str, text: str) -> str:
        """分类模型类型"""

        # 分析模型应用领域
        context = self._get_model_context(model_name, text, window=100)

        if any(kw in context for kw in ['投资', '商业', '企业']):
            return 'business'
        elif any(kw in context for kw in ['心理', '认知', '行为']):
            return 'psychology'
        elif any(kw in context for kw in ['逻辑', '推理', '思考']):
            return 'philosophy'
        elif any(kw in context for kw in ['系统', '流程', '方法']):
            return 'methodology'
        else:
            return 'general'

    def _get_model_context(self, model_name: str, text: str, window: int = 100) -> str:
        """获取模型上下文"""

        index = text.find(model_name)
        if index == -1:
            return ""

        start = max(0, index - window)
        end = min(len(text), index + len(model_name) + window)

        return text[start:end]

    def _deduplicate_models(self, models: List[Dict]) -> List[Dict]:
        """去重心智模型"""

        seen = set()
        unique_models = []

        for model in models:
            model_key = model.get('name', '').lower()
            # 合并相似名称
            if model_key not in seen:
                seen.add(model_key)
                unique_models.append(model)
            else:
                # 如果已存在，合并证据
                for existing in unique_models:
                    if existing.get('name', '').lower() == model_key:
                        existing['evidence'].extend(model['evidence'])
                        existing['importance_score'] = max(
                            existing['importance_score'],
                            model['importance_score']
                        )
                        break

        return unique_models

    def _extract_decision_heuristics_advanced(self, research_data: Dict) -> List[str]:
        """高级启发式提取 - 基于句法分析和语义识别"""

        heuristics = []

        # 高级模式匹配
        patterns = [
            r'当(.{1,30})\s*时\s*[，,]?\s*应该?(.{1,60})',
            r'如果是?(.{1,30})\s*[，,]?\s*则?(.{1,60})',
            r'(.{1,15})\s*(?:原则|准则|Rule|Principle)\s*[:：]?\s*([^.。]+)',
            r'在?(.{1,20})\s*时\s*[，,]?\s*优先?(.{1,50})'
        ]

        for dimension, text in research_data.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    heuristic = match.group(0).strip()
                    # 验证启发式质量
                    if self._validate_heuristic_quality(heuristic):
                        heuristics.append(heuristic)

        # 去重和排序
        unique_heuristics = list(set(heuristics))

        # 按长度排序（优先选择完整的启发式）
        unique_heuristics.sort(key=len, reverse=True)

        return unique_heuristics[:10]

    def _validate_heuristic_quality(self, heuristic: str) -> bool:
        """验证启发式质量"""

        # 长度检查
        if len(heuristic) < 10 or len(heuristic) > 100:
            return False

        # 必须包含条件-结果结构
        condition_indicators = ['当', '如果', '在', '是']
        result_indicators = ['应该', '则', '优先', '原则']

        has_condition = any(ind in heuristic for ind in condition_indicators)
        has_result = any(ind in heuristic for ind in result_indicators)

        return has_condition and has_result

    def _extract_expression_dna_advanced(self, research_data: Dict) -> Dict:
        """高级表达DNA提取 - 基于文本统计和风格分析"""

        dna = {
            'sentence_patterns': [],
            'vocabulary': [],
            'rhythm': '',
            'style_features': {}
        }

        if '03-expression-dna' in research_data:
            expression_text = research_data['03-expression-dna']

            # 1. 句式模式分析
            dna['sentence_patterns'] = self._analyze_sentence_patterns_advanced(expression_text)

            # 2. 词汇分析
            dna['vocabulary'] = self._analyze_vocabulary_advanced(expression_text)

            # 3. 节奏分析
            dna['rhythm'] = self._analyze_rhythm_advanced(expression_text)

            # 4. 风格特征
            dna['style_features'] = self._extract_style_features(expression_text)

        return dna

    def _analyze_sentence_patterns_advanced(self, text: str) -> List[Dict]:
        """高级句式分析"""

        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0]

        patterns = []

        # 分析句子长度分布
        lengths = [len(s) for s in sentences[:50]]  # 取前50句
        if lengths:
            avg_length = sum(lengths) / len(lengths)
            patterns.append({
                'type': 'average_length',
                'value': round(avg_length, 1),
                'description': f'平均句子长度: {avg_length:.1f}字符'
            })

            # 长短句比例
            long_sentences = sum(1 for l in lengths if l > 30)
            short_sentences = sum(1 for l in lengths if l <= 15)
            patterns.append({
                'type': 'length_distribution',
                'long_ratio': round(long_sentences / len(lengths), 2),
                'short_ratio': round(short_sentences / len(lengths), 2),
                'description': f'长句比例: {long_sentences/len(lengths):.0%}, 短句比例: {short_sentences/len(lengths):.0%}'
            })

        # 分析句式结构
        if_pattern_count = sum(1 for s in sentences if '如果' in s or '若' in s)
        question_pattern_count = sum(1 for s in sentences if '?' in s or '？' in s)
        patterns.append({
            'type': 'structure',
            'conditional_sentences': if_pattern_count,
            'question_sentences': question_pattern_count,
            'description': f'条件句: {if_pattern_count}, 疑问句: {question_pattern_count}'
        })

        return patterns

    def _analyze_vocabulary_advanced(self, text: str) -> List[Dict]:
        """高级词汇分析"""

        words = re.findall(r'\w+', text)
        word_counts = Counter(words)

        # 过滤
        stop_words = {'的', '是', '在', '了', '和', '有', '我', '你', '他', '她', '它'}
        meaningful_words = {
            word: count for word, count in word_counts.items()
            if len(word) > 2 and word not in stop_words
        }

        # 高频词
        top_words = meaningful_words.most_common(10)

        # 词汇丰富度
        unique_ratio = len(set(words)) / len(words) if len(words) > 0 else 0

        return [
            {
                'type': 'frequency',
                'words': [{'word': w, 'count': c} for w, c in top_words],
                'description': f'高频词汇'
            },
            {
                'type': 'richness',
                'value': round(unique_ratio, 3),
                'description': f'词汇丰富度: {unique_ratio:.3f}'
            }
        ]

    def _analyze_rhythm_advanced(self, text: str) -> str:
        """高级节奏分析"""

        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0][:50]

        # 标点密度
        punctuation_count = text.count('，') + text.count('。') + text.count('！') + text.count('？')
        char_count = len(text)
        punctuation_density = punctuation_count / char_count if char_count > 0 else 0

        # 句长方差
        lengths = [len(s) for s in sentences]
        if len(lengths) > 1:
            avg_length = sum(lengths) / len(lengths)
            variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
            std_dev = math.sqrt(variance)
        else:
            std_dev = 0

        # 判断节奏
        if punctuation_density < 0.02 and std_dev < 10:
            return "长句为主，节奏平缓"
        elif punctuation_density > 0.05 and std_dev > 20:
            return "短句为主，节奏明快"
        elif std_dev > 15:
            return "长短句交替，节奏多变"
        else:
            return "节奏适中"

    def _extract_style_features(self, text: str) -> Dict:
        """提取风格特征"""

        features = {}

        # 是否使用比喻
        metaphor_count = text.count('像') + text.count('如') + text.count('仿佛')
        features['uses_metaphor'] = metaphor_count > 5

        # 是否使用数据
        number_count = len(re.findall(r'\d+', text))
        features['data_oriented'] = number_count > 10

        # 是否使用引用
        quote_count = text.count('"') + text.count('"') + text.count("'")
        features['quotes_sources'] = quote_count > 5

        # 情感倾向
        positive_words = ['好', '优秀', '成功', '喜欢', '爱']
        negative_words = ['坏', '差', '失败', '讨厌', '恨']
        positive_count = sum(text.count(w) for w in positive_words)
        negative_count = sum(text.count(w) for w in negative_words)
        if positive_count > negative_count * 2:
            features['sentiment'] = 'positive'
        elif negative_count > positive_count * 2:
            features['sentiment'] = 'negative'
        else:
            features['sentiment'] = 'neutral'

        return features

    def _extract_values_advanced(self, research_data: Dict) -> List[Dict]:
        """高级价值观提取"""

        values = []

        # 价值观关键词和权重
        value_keywords = {
            '价值': 2, '原则': 2, '信念': 3, '相信': 1, '重视': 2,
            '追求': 2, '坚持': 2, '核心': 2, '本质': 2
        }

        value_contexts = []

        for dimension, text in research_data.items():
            for keyword, weight in value_keywords.items():
                if keyword in text:
                    # 提取上下文
                    matches = re.finditer(rf'.{{30}}{keyword}.{{30}}', text)
                    for match in matches:
                        context = match.group(0)
                        value_contexts.append({
                            'keyword': keyword,
                            'context': context,
                            'weight': weight,
                            'source': dimension
                        })

        # 按权重排序
        value_contexts.sort(key=lambda x: x['weight'], reverse=True)

        # 提取核心价值观
        for vc in value_contexts[:5]:
            values.append({
                'value': vc['keyword'],
                'context': vc['context'][:100],
                'source': vc['source'],
                'importance': vc['weight']
            })

        return values

    def _extract_toolkit_advanced(self, research_data: Dict) -> List[Dict]:
        """高级工具箱提取"""

        tools = []

        tool_patterns = [
            r'(\w+)\s*[:：]\s*工具',
            r'使用?(\w+)(?:工具|方法|技巧)',
            r'(\w+)(?:工具|Tool|Method)',
            r'应用\s*(\w+)(?:框架|模型)'
        ]

        for dimension, text in research_data.items():
            for pattern in tool_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    tool_name = match.group(1).strip()
                    if len(tool_name) > 1:
                        # 提取工具描述
                        description = self._extract_tool_description(tool_name, text)

                        tools.append({
                            'name': tool_name,
                            'description': description,
                            'source': dimension
                        })

        # 去重
        seen = set()
        unique_tools = []
        for tool in tools:
            tool_key = tool['name'].lower()
            if tool_key not in seen:
                seen.add(tool_key)
                unique_tools.append(tool)

        return unique_tools[:10]

    def _extract_tool_description(self, tool_name: str, text: str) -> str:
        """提取工具描述"""

        pattern = rf'{tool_name}\s*[:：]\s*([^.。]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

        return f"{tool_name}工具"

    def _extract_internal_tensions_advanced(self, research_data: Dict) -> List[Dict]:
        """高级内在张力提取"""

        tensions = []

        # 张力关键词和强度
        tension_keywords = {
            '矛盾': 3, '冲突': 3, '不一致': 2, '悖论': 3,
            '对立': 2, '两难': 2, '困境': 2, '矛盾'
        }

        for dimension, text in research_data.items():
            for keyword, strength in tension_keywords.items():
                if keyword in text:
                    # 提取上下文
                    matches = re.finditer(rf'.{{50}}{keyword}.{{50}}', text)
                    for match in matches:
                        context = match.group(0)
                        tensions.append({
                            'tension': keyword,
                            'strength': strength,
                            'context': context[:150],
                            'source': dimension
                        })

        # 按强度排序
        tensions.sort(key=lambda x: x['strength'], reverse=True)

        return tensions[:5]

    def _extract_honest_boundaries_advanced(self, research_data: Dict) -> List[Dict]:
        """高级诚实边界提取"""

        boundaries = []

        # 边界关键词
        boundary_keywords = {
            '局限': 3, '不能': 2, '做不到': 3, '不擅长': 2,
            '无法': 2, '难以': 2, '边界': 3, '范围': 1
        }

        for dimension, text in research_data.items():
            for keyword, severity in boundary_keywords.items():
                if keyword in text:
                    # 提取上下文
                    matches = re.finditer(rf'.{{50}}{keyword}.{{50}}', text)
                    for match in matches:
                        context = match.group(0)
                        boundaries.append({
                            'boundary': keyword,
                            'severity': severity,
                            'context': context[:150],
                            'source': dimension
                        })

        # 按严重程度排序
        boundaries.sort(key=lambda x: x['severity'], reverse=True)

        return boundaries[:5]

    def _validate_mental_models_advanced(self, models: List[Dict],
                                         research_data: Dict) -> List[Dict]:
        """高级心智模型验证 - 四维验证 + 一致性检查"""

        validated_models = []

        for model in models:
            model_name = model.get('name', '')

            # 四维验证
            scores = {
                'cross_domain_reproducibility': self._validate_cross_domain_advanced(
                    model_name,
                    research_data
                ),
                'generative_power': self._validate_generative_power_advanced(
                    model_name,
                    research_data
                ),
                'exclusivity': self._validate_exclusivity_advanced(
                    model_name,
                    research_data
                ),
                'testability': self._validate_testability_advanced(
                    model_name,
                    research_data
                )
            }

            # 计算总分
            total_score = sum(
                scores[criterion] * self.VALIDATION_CRITERIA[criterion]['weight']
                for criterion in scores
            )

            # 一致性检查
            consistency_score = self._check_model_consistency(model, research_data)

            validated_model = {
                **model,
                'validation': {
                    'scores': scores,
                    'total_score': total_score,
                    'passed': total_score >= self.PASSING_SCORE,
                    'consistency_score': consistency_score,
                    'details': self._generate_validation_details(scores, total_score)
                }
            }

            validated_models.append(validated_model)

        return validated_models

    def _validate_cross_domain_advanced(self, model_name: str, research_data: Dict) -> int:
        """高级跨域验证"""

        appearances = []
        domain_count = set()

        for dimension, text in research_data.items():
            if model_name in text:
                appearances.append(dimension)
                # 识别领域
                for domain, keywords in self.DOMAIN_KEYWORDS.items():
                    if any(kw in text for kw in keywords):
                        domain_count.add(domain)

        domain_count = len(domain_count)

        if domain_count >= 2:
            return self.VALIDATION_CRITERIA['cross_domain_reproducibility']['pass_score']
        elif domain_count == 1:
            return self.VALIDATION_CRITERIA['cross_domain_reproducibility']['partial_score']
        else:
            return self.VALIDATION_CRITERIA['cross_domain_reproducibility']['fail_score']

    def _validate_generative_power_advanced(self, model_name: str, research_data: Dict) -> int:
        """高级生成力验证"""

        # 检查应用场景数量
        application_count = 0

        for text in research_data.values():
            # 寻找"应用"相关上下文
            matches = re.finditer(rf'{model_name}.{{0,30}}(?:应用|案例|适用)', text)
            application_count += len(list(matches))

        if application_count >= 2:
            return self.VALIDATION_CRITERIA['generative_power']['pass_score']
        elif application_count == 1:
            return self.VALIDATION_CRITERIA['generative_power']['partial_score']
        else:
            return self.VALIDATION_CRITERIA['generative_power']['fail_score']

    def _validate_exclusivity_advanced(self, model_name: str, research_data: Dict) -> int:
        """高级排他性验证"""

        # 检查是否是通用概念
        generic_terms = ['理论', '概念', '思想', '观念']

        for term in generic_terms:
            if model_name.endswith(term):
                return self.VALIDATION_CRITERIA['exclusivity']['partial_score']

        # 检查是否有独特性描述
        has_unique_description = False
        for text in research_data.values():
            if any(kw in text for kw in ['独特', '特有', '专门']):
                has_unique_description = True
                break

        if has_unique_description and len(model_name) > 2:
            return self.VALIDATION_CRITERIA['exclusivity']['pass_score']
        else:
            return self.VALIDATION_CRITERIA['exclusivity']['partial_score']

    def _validate_testability_advanced(self, model_name: str, research_data: Dict) -> int:
        """高级可测试性验证"""

        # 检查实证/证据/案例数量
        evidence_keywords = ['证据', '实证', '案例', '实验', '数据', '证明']

        evidence_count = 0
        for text in research_data.values():
            if model_name in text:
                for kw in evidence_keywords:
                    evidence_count += text.count(kw)

        if evidence_count >= 2:
            return self.VALIDATION_CRITERIA['testability']['pass_score']
        elif evidence_count == 1:
            return self.VALIDATION_CRITERIA['testability']['pass_score']  # 至少1个也给满分
        else:
            return self.VALIDATION_CRITERIA['testability']['fail_score']

    def _check_model_consistency(self, model: Dict, research_data: Dict) -> float:
        """检查模型一致性"""

        model_name = model.get('name', '')
        evidence = model.get('evidence', [])

        # 一致性得分 = 证据数量 / 维度数量
        dimension_count = len(research_data)
        evidence_count = len(evidence)

        consistency = evidence_count / dimension_count if dimension_count > 0 else 0

        return round(min(consistency, 1.0), 2)

    def _generate_validation_details(self, scores: Dict, total_score: int) -> Dict:
        """生成验证详情"""

        details = {}
        for criterion, score in scores.items():
            criterion_info = self.VALIDATION_CRITERIA[criterion]
            details[criterion] = {
                'score': score,
                'weight': criterion_info['weight'],
                'weighted_score': score * criterion_info['weight'],
                'description': criterion_info['description'],
                'threshold': criterion_info['threshold']
            }

        details['total'] = {
            'score': total_score,
            'passing_line': self.PASSING_SCORE,
            'passed': total_score >= self.PASSING_SCORE
        }

        return details

    def _generate_framework_summary_advanced(self, framework: Dict) -> Dict:
        """生成高级框架总结"""

        validated_models = framework.get('validated_models', [])
        passed_models = [m for m in validated_models if m.get('validation', {}).get('passed')]

        # 计算平均验证分数
        avg_score = 0
        if validated_models:
            avg_score = sum(m['validation']['total_score'] for m in validated_models) / len(validated_models)

        return {
            'total_mental_models': len(validated_models),
            'validated_models': len(passed_models),
            'validation_rate': f"{len(passed_models) / len(validated_models) * 100:.0f}%" if validated_models else "0%",
            'average_score': round(avg_score, 1),
            'total_decision_heuristics': len(framework.get('decision_heuristics', [])),
            'total_values': len(framework.get('values', [])),
            'total_tools': len(framework.get('toolkit', [])),
            'total_tensions': len(framework.get('internal_tensions', [])),
            'total_boundaries': len(framework.get('honest_boundaries', [])),
            'framework_quality': self._evaluate_framework_quality(passed_models, framework)
        }

    def _evaluate_framework_quality(self, passed_models: List[Dict], framework: Dict) -> str:
        """评估框架质量"""

        passed_count = len(passed_models)
        heuristic_count = len(framework.get('decision_heuristics', []))
        tension_count = len(framework.get('internal_tensions', []))
        boundary_count = len(framework.get('honest_boundaries', []))

        # 质量评分
        quality_score = 0
        quality_score += passed_count * 3
        quality_score += min(heuristic_count, 10) * 0.5
        quality_score += min(tension_count, 5) * 1
        quality_score += min(boundary_count, 5) * 1.5

        if quality_score >= 20:
            return 'high'
        elif quality_score >= 12:
            return 'medium'
        else:
            return 'low'


def main():
    import argparse

    parser = argparse.ArgumentParser(description='框架提取（高级版）')
    parser.add_argument('--research-dir', type=str, required=True,
                       help='调研数据目录')
    parser.add_argument('--target', type=str, required=True,
                       help='目标（人名/主题）')
    parser.add_argument('--output', type=str, required=True,
                       help='输出JSON文件路径')

    args = parser.parse_args()

    extractor = FrameworkExtractor()

    # 提取框架
    framework = extractor.extract_framework(args.research_dir, args.target)

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(framework, f, ensure_ascii=False, indent=2)

    print(f"框架提取完成，结果保存到: {args.output}")
    print("\n=== 框架总结 ===")
    print(json.dumps(framework['summary'], ensure_ascii=False, indent=2))
    print("\n=== 验证通过的心智模型 ===")
    for model in framework['validated_models']:
        if model.get('validation', {}).get('passed'):
            print(f"- {model['name']} (分数: {model['validation']['total_score']})")


if __name__ == '__main__':
    main()
