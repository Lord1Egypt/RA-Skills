"""
Text Analyzer - 文本分析器
支持中文和英文的自然语言处理功能
"""

import re
import math
import jieba
import jieba.analyse
from typing import List, Dict, Tuple, Optional, Any, Union
from collections import Counter
from dataclasses import dataclass


@dataclass
class SentimentResult:
    """情感分析结果"""
    polarity: float  # 情感极性 (-1~1 或 0~1，取决于分析器)
    subjectivity: float  # 主观性 (0~1)
    confidence: float  # 置信度
    language: str  # 检测到的语言
    raw_score: float = 0.0  # 原始分数


@dataclass
class AnalysisResult:
    """综合分析结果"""
    text: str
    language: str
    tokens: List[str]
    sentiment: SentimentResult
    keywords: List[Tuple[str, float]]
    summary: str
    word_freq: Dict[str, int]
    text_length: int
    sentence_count: int


class TextAnalyzer:
    """
    文本分析器主类
    提供分词、情感分析、关键词提取等功能
    """
    
    def __init__(self):
        """初始化文本分析器"""
        self._init_jieba()
        self.stopwords = self._load_default_stopwords()
    
    def _init_jieba(self):
        """初始化Jieba分词器"""
        # 添加常用词典路径（如果存在）
        try:
            jieba.initialize()
        except:
            pass
    
    def _load_default_stopwords(self) -> set:
        """加载默认停用词表"""
        # 中英文常用停用词
        default_stopwords = {
            # 中文停用词
            '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', 
            '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '之',
            '为', '与', '及', '等', '或', '但', '而', '因', '于', '由',
            '被', '把', '从', '将', '向', '让', '给', '使', '对', '比',
            # 英文停用词
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'what', 'which', 'who', 'whom', 'this',
            'that', 'these', 'those', 'am', 'it', 'its', 'i', 'me',
            'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
            'his', 'himself', 'she', 'her', 'hers', 'herself', 'they',
            'them', 'their', 'theirs', 'themselves', 'itself'
        }
        return default_stopwords
    
    def detect_language(self, text: str) -> str:
        """
        检测文本语言（简单版本）
        
        Returns:
            'zh': 中文, 'en': 英文, 'mixed': 混合, 'unknown': 未知
        """
        if not text:
            return 'unknown'
        
        # 统计中文字符和英文单词
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        total_chars = len(text.replace(' ', ''))
        
        if total_chars == 0:
            return 'unknown'
        
        chinese_ratio = chinese_chars / total_chars
        english_ratio = english_words * 3 / total_chars  # 假设平均每个词3个字母
        
        if chinese_ratio > 0.5:
            return 'zh'
        elif english_ratio > 0.5:
            return 'en'
        elif chinese_ratio > 0.1 or english_ratio > 0.1:
            return 'mixed'
        else:
            return 'unknown'
    
    def segment(self, text: str, mode: str = 'accurate') -> List[str]:
        """
        分词
        
        Args:
            text: 待分词文本
            mode: 分词模式 ('accurate':精确, 'full':全模式, 'search':搜索引擎模式)
        
        Returns:
            分词结果列表
        """
        if not text:
            return []
        
        language = self.detect_language(text)
        
        if language == 'zh' or language == 'mixed':
            # 中文使用jieba分词
            cut_mode = {
                'accurate': jieba.cut,
                'full': jieba.cut,
                'search': jieba.cut_for_search
            }.get(mode, jieba.cut)
            
            if mode == 'full':
                words = list(jieba.cut(text, cut_all=True))
            else:
                words = list(cut_mode(text))
            
            # 过滤停用词和空格
            words = [w.strip() for w in words 
                     if w.strip() and w.strip() not in self.stopwords]
            
        else:
            # 英文按空格和标点分词
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            words = [w for w in words if w not in self.stopwords]
        
        return words
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """
        情感分析
        
        Args:
            text: 待分析文本
        
        Returns:
            SentimentResult对象
        """
        if not text:
            return SentimentResult(
                polarity=0.0, subjectivity=0.0, 
                confidence=0.0, language='unknown'
            )
        
        language = self.detect_language(text)
        
        if language == 'zh' or language == 'mixed':
            return self._analyze_chinese_sentiment(text)
        else:
            return self._analyze_english_sentiment(text)
    
    def _analyze_chinese_sentiment(self, text: str) -> SentimentResult:
        """使用SnowNLP进行中文情感分析"""
        try:
            from snownlp import SnowNLP
            
            s = SnowNLP(text)
            sentiment_score = s.sentiments  # 0~1，越接近1越正面
            
            # 转换为 -1~1 范围
            polarity = (sentiment_score - 0.5) * 2
            
            return SentimentResult(
                polarity=round(polarity, 4),
                subjectivity=round(abs(polarity), 4),
                confidence=round(sentiment_score if sentiment_score > 0.5 else 1 - sentiment_score, 4),
                language='zh',
                raw_score=round(sentiment_score, 4)
            )
        except ImportError:
            return SentimentResult(
                polarity=0.0, subjectivity=0.0,
                confidence=0.0, language='zh'
            )
    
    def _analyze_english_sentiment(self, text: str) -> SentimentResult:
        """使用TextBlob进行英文情感分析"""
        try:
            from textblob import TextBlob
            
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1~1
            subjectivity = blob.sentiment.subjectivity  # 0~1
            
            # 计算置信度
            confidence = abs(polarity) * (1 - abs(subjectivity - 0.5) * 2)
            
            return SentimentResult(
                polarity=round(polarity, 4),
                subjectivity=round(subjectivity, 4),
                confidence=round(confidence, 4),
                language='en',
                raw_score=round((polarity + 1) / 2, 4)
            )
        except ImportError:
            return SentimentResult(
                polarity=0.0, subjectivity=0.0,
                confidence=0.0, language='en'
            )
    
    def extract_keywords(self, text: str, top_k: int = 10, 
                        allow_pos: Tuple[str, ...] = ('n', 'v', 'a', 'ns', 'vn')) -> List[Tuple[str, float]]:
        """
        关键词提取
        
        Args:
            text: 待分析文本
            top_k: 返回前k个关键词
            allow_pos: 允许的词性（中文）
        
        Returns:
            [(关键词, 权重), ...]
        """
        if not text or top_k <= 0:
            return []
        
        language = self.detect_language(text)
        
        if language == 'zh' or language == 'mixed':
            # 使用jieba的TF-IDF提取关键词
            keywords = jieba.analyse.extract_tags(
                text, 
                topK=top_k,
                withWeight=True,
                allowPOS=allow_pos
            )
            return [(word, round(weight, 4)) for word, weight in keywords]
        else:
            # 英文简单处理：按词频排序，排除停用词
            words = self.segment(text)
            word_freq = Counter(words)
            
            # 计算TF-IDF风格的权重
            total_words = len(words)
            unique_words = len(word_freq)
            
            keywords = []
            for word, freq in word_freq.most_common(top_k * 2):
                if len(word) > 2:  # 过滤短词
                    # 简单TF-IDF计算
                    tf = freq / total_words
                    idf = math.log(total_words / freq)
                    weight = tf * idf
                    keywords.append((word, round(weight, 4)))
                
                if len(keywords) >= top_k:
                    break
            
            return keywords
    
    def generate_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        生成文本摘要（基于TextRank的简单实现）
        
        Args:
            text: 原始文本
            num_sentences: 摘要句数
        
        Returns:
            摘要文本
        """
        if not text:
            return ""
        
        # 分句
        if self.detect_language(text) == 'zh':
            sentences = re.split(r'[。！？\n]+', text)
        else:
            sentences = re.split(r'[.!?\n]+', text)
        
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= num_sentences:
            return text
        
        # 计算每句话的重要性（基于与其他句子的相似度）
        sentence_scores = []
        for i, sent in enumerate(sentences):
            score = 0
            for j, other_sent in enumerate(sentences):
                if i != j:
                    score += self._sentence_similarity(sent, other_sent)
            sentence_scores.append((i, score, sent))
        
        # 选择得分最高的句子
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = sorted(sentence_scores[:num_sentences], key=lambda x: x[0])
        
        # 保持原始顺序拼接
        summary = ' '.join([s[2] for s in top_sentences])
        return summary
    
    def _sentence_similarity(self, sent1: str, sent2: str) -> float:
        """计算两个句子的相似度（Jaccard系数）"""
        words1 = set(self.segment(sent1))
        words2 = set(self.segment(sent2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def word_frequency(self, text: str, top_k: Optional[int] = None) -> Dict[str, int]:
        """
        词频统计
        
        Args:
            text: 待分析文本
            top_k: 只返回前k个高频词
        
        Returns:
            {词: 频次}
        """
        words = self.segment(text)
        freq = Counter(words)
        
        if top_k:
            return dict(freq.most_common(top_k))
        return dict(freq)
    
    def calculate_similarity(self, text1: str, text2: str, method: str = 'cosine') -> float:
        """
        计算两段文本的相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            method: 计算方法 ('cosine':余弦相似度, 'jaccard':Jaccard)
        
        Returns:
            相似度分数 (0~1)
        """
        if not text1 or not text2:
            return 0.0
        
        if method == 'jaccard':
            return self._sentence_similarity(text1, text2)
        
        # 余弦相似度
        words1 = self.segment(text1)
        words2 = self.segment(text2)
        
        vocab = set(words1) | set(words2)
        vec1 = [words1.count(w) for w in vocab]
        vec2 = [words2.count(w) for w in vocab]
        
        # 计算余弦相似度
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return round(dot_product / (norm1 * norm2), 4)
    
    def analyze(self, text: str) -> AnalysisResult:
        """
        综合文本分析
        
        Args:
            text: 待分析文本
        
        Returns:
            AnalysisResult对象
        """
        language = self.detect_language(text)
        tokens = self.segment(text)
        sentiment = self.analyze_sentiment(text)
        keywords = self.extract_keywords(text, top_k=10)
        summary = self.generate_summary(text, num_sentences=2)
        word_freq = self.word_frequency(text, top_k=20)
        
        # 统计句子数
        if language == 'zh':
            sentences = re.split(r'[。！？\n]+', text)
        else:
            sentences = re.split(r'[.!?\n]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        return AnalysisResult(
            text=text,
            language=language,
            tokens=tokens,
            sentiment=sentiment,
            keywords=keywords,
            summary=summary,
            word_freq=word_freq,
            text_length=len(text),
            sentence_count=sentence_count
        )
    
    def add_stopwords(self, words: List[str]):
        """添加停用词"""
        self.stopwords.update(words)
    
    def remove_stopwords(self, words: List[str]):
        """移除停用词"""
        for word in words:
            self.stopwords.discard(word)
    
    def add_custom_dict(self, dict_path: str):
        """添加自定义词典（jieba）"""
        try:
            jieba.load_userdict(dict_path)
        except Exception as e:
            print(f"加载自定义词典失败: {e}")


class TextClassifier:
    """
    简单文本分类器（基于关键词匹配）
    适用于快速分类场景，不适用于高精度需求
    """
    
    def __init__(self):
        self.categories: Dict[str, List[str]] = {}
    
    def add_category(self, name: str, keywords: List[str]):
        """添加分类及其关键词"""
        self.categories[name] = keywords
    
    def classify(self, text: str, analyzer: TextAnalyzer) -> List[Tuple[str, float]]:
        """
        分类文本
        
        Returns:
            [(分类名, 置信度), ...] 按置信度排序
        """
        text_keywords = set([kw[0] for kw in analyzer.extract_keywords(text, top_k=20)])
        
        scores = []
        for cat_name, cat_keywords in self.categories.items():
            cat_keyword_set = set(cat_keywords)
            
            if not cat_keyword_set:
                scores.append((cat_name, 0.0))
                continue
            
            # 计算匹配度
            matches = len(text_keywords & cat_keyword_set)
            total = len(cat_keyword_set)
            score = matches / total if total > 0 else 0.0
            
            scores.append((cat_name, round(score, 4)))
        
        # 按置信度排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
