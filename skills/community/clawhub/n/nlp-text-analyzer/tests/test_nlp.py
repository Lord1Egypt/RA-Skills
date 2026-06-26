"""
NLP Text Analyzer - 单元测试
"""

import pytest
from scripts.text_analyzer import TextAnalyzer, TextClassifier, SentimentResult, AnalysisResult


class TestTextAnalyzer:
    """测试TextAnalyzer类"""
    
    @pytest.fixture
    def analyzer(self):
        """创建分析器fixture"""
        return TextAnalyzer()
    
    def test_init(self, analyzer):
        """测试初始化"""
        assert analyzer is not None
        assert len(analyzer.stopwords) > 0
    
    def test_detect_language_chinese(self, analyzer):
        """测试中文检测"""
        assert analyzer.detect_language("这是一个中文句子") == 'zh'
    
    def test_detect_language_english(self, analyzer):
        """测试英文检测"""
        assert analyzer.detect_language("This is an English sentence.") == 'en'
    
    def test_detect_language_mixed(self, analyzer):
        """测试混合语言检测"""
        assert analyzer.detect_language("This is 中文 mixed English") == 'mixed'
    
    def test_detect_language_empty(self, analyzer):
        """测试空文本检测"""
        assert analyzer.detect_language("") == 'unknown'
    
    def test_segment_chinese(self, analyzer):
        """测试中文分词"""
        text = "自然语言处理是人工智能的重要分支"
        tokens = analyzer.segment(text)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        # 验证停用词被过滤
        assert '的' not in tokens
        assert '是' not in tokens
    
    def test_segment_english(self, analyzer):
        """测试英文分词"""
        text = "Natural language processing is important"
        tokens = analyzer.segment(text)
        
        assert isinstance(tokens, list)
        assert 'natural' in tokens
        assert 'language' in tokens
        # 停用词应该被过滤
        assert 'is' not in tokens
    
    def test_segment_empty(self, analyzer):
        """测试空文本分词"""
        assert analyzer.segment("") == []
    
    def test_analyze_sentiment_chinese_positive(self, analyzer):
        """测试中文正面情感"""
        result = analyzer.analyze_sentiment("这个产品很棒，我非常喜欢！")
        
        assert isinstance(result, SentimentResult)
        assert result.language == 'zh'
        assert result.polarity > 0  # 正面
    
    def test_analyze_sentiment_chinese_negative(self, analyzer):
        """测试中文负面情感"""
        result = analyzer.analyze_sentiment("这个产品太糟糕了，完全不满意")
        
        assert result.language == 'zh'
        assert result.polarity < 0  # 负面
    
    def test_analyze_sentiment_english_positive(self, analyzer):
        """测试英文正面情感"""
        result = analyzer.analyze_sentiment("This product is amazing and wonderful!")
        
        assert result.language == 'en'
        assert result.polarity > 0  # 正面
    
    def test_analyze_sentiment_english_negative(self, analyzer):
        """测试英文负面情感"""
        result = analyzer.analyze_sentiment("This product is terrible and disappointing")
        
        assert result.language == 'en'
        assert result.polarity < 0  # 负面
    
    def test_extract_keywords_chinese(self, analyzer):
        """测试中文关键词提取"""
        text = "人工智能是计算机科学的一个重要分支，它研究如何实现智能机器"
        keywords = analyzer.extract_keywords(text, top_k=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        
        # 检查返回格式
        if keywords:
            word, weight = keywords[0]
            assert isinstance(word, str)
            assert isinstance(weight, float)
    
    def test_extract_keywords_english(self, analyzer):
        """测试英文关键词提取"""
        text = "Machine learning is a subset of artificial intelligence"
        keywords = analyzer.extract_keywords(text, top_k=5)
        
        assert isinstance(keywords, list)
        # 英文应该有关键词返回
        if keywords:
            assert len(keywords[0]) == 2  # (word, weight)
    
    def test_extract_keywords_empty(self, analyzer):
        """测试空文本关键词提取"""
        assert analyzer.extract_keywords("", top_k=5) == []
        assert analyzer.extract_keywords("text", top_k=0) == []
    
    def test_generate_summary(self, analyzer):
        """测试文本摘要"""
        text = """第一自然段。这是第二句话。这是第三句话。
        第二自然段。这里有一些内容。还有一些内容。
        第三自然段。最后的内容。结束。"""
        
        summary = analyzer.generate_summary(text, num_sentences=2)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert len(summary) < len(text)
    
    def test_generate_summary_short(self, analyzer):
        """测试短文本摘要"""
        text = "这是一个短文本。"
        summary = analyzer.generate_summary(text, num_sentences=3)
        
        # 短文本应该原样返回
        assert summary == text
    
    def test_word_frequency(self, analyzer):
        """测试词频统计"""
        text = "苹果 香蕉 苹果 橙子 香蕉 苹果"
        freq = analyzer.word_frequency(text, top_k=3)
        
        assert isinstance(freq, dict)
        if freq:  # 如果有停用词过滤后还有词
            # 苹果应该出现最多
            assert '苹果' in freq or 'apple' in freq or any('果' in k for k in freq.keys())
    
    def test_calculate_similarity_cosine(self, analyzer):
        """测试余弦相似度"""
        text1 = "人工智能 机器学习 深度学习"
        text2 = "机器学习 深度学习 神经网络"
        
        sim = analyzer.calculate_similarity(text1, text2, method='cosine')
        
        assert isinstance(sim, float)
        assert 0 <= sim <= 1
        # 有共同词汇，相似度应该大于0
        assert sim > 0
    
    def test_calculate_similarity_jaccard(self, analyzer):
        """测试Jaccard相似度"""
        text1 = "苹果 香蕉"
        text2 = "苹果 橙子"
        
        sim = analyzer.calculate_similarity(text1, text2, method='jaccard')
        
        assert isinstance(sim, float)
        assert 0 <= sim <= 1
    
    def test_calculate_similarity_empty(self, analyzer):
        """测试空文本相似度"""
        assert analyzer.calculate_similarity("", "text") == 0.0
        assert analyzer.calculate_similarity("text", "") == 0.0
    
    def test_analyze_comprehensive(self, analyzer):
        """测试综合分析"""
        text = "自然语言处理是人工智能的重要分支。它研究如何实现人与计算机之间的有效通信。"
        
        result = analyzer.analyze(text)
        
        assert isinstance(result, AnalysisResult)
        assert result.text == text
        assert result.language in ['zh', 'en', 'mixed', 'unknown']
        assert isinstance(result.tokens, list)
        assert isinstance(result.sentiment, SentimentResult)
        assert isinstance(result.keywords, list)
        assert isinstance(result.summary, str)
        assert isinstance(result.word_freq, dict)
        assert result.text_length > 0
        assert result.sentence_count > 0
    
    def test_add_stopwords(self, analyzer):
        """测试添加停用词"""
        initial_count = len(analyzer.stopwords)
        analyzer.add_stopwords(['custom_word'])
        assert len(analyzer.stopwords) == initial_count + 1
        assert 'custom_word' in analyzer.stopwords
    
    def test_remove_stopwords(self, analyzer):
        """测试移除停用词"""
        analyzer.add_stopwords(['test_word'])
        assert 'test_word' in analyzer.stopwords
        
        analyzer.remove_stopwords(['test_word'])
        assert 'test_word' not in analyzer.stopwords


class TestTextClassifier:
    """测试TextClassifier类"""
    
    @pytest.fixture
    def classifier(self):
        """创建分类器fixture"""
        return TextClassifier()
    
    def test_init(self, classifier):
        """测试初始化"""
        assert classifier.categories == {}
    
    def test_add_category(self, classifier):
        """测试添加分类"""
        classifier.add_category("科技", ["人工智能", "机器学习", "算法"])
        
        assert "科技" in classifier.categories
        assert classifier.categories["科技"] == ["人工智能", "机器学习", "算法"]
    
    def test_classify(self, classifier, analyzer):
        """测试文本分类"""
        classifier.add_category("科技", ["人工智能", "机器学习", "技术"])
        classifier.add_category("体育", ["比赛", "运动员", "球队"])
        
        text = "机器学习技术在人工智能领域有重要应用"
        results = classifier.classify(text, analyzer)
        
        assert isinstance(results, list)
        assert len(results) == 2
        # 按置信度排序
        assert results[0][1] >= results[1][1]
        # 科技类别应该有更高分数
        tech_score = next((s for c, s in results if c == "科技"), 0)
        sport_score = next((s for c, s in results if c == "体育"), 0)
        assert tech_score >= sport_score


class TestSentimentResult:
    """测试SentimentResult数据类"""
    
    def test_creation(self):
        """测试创建SentimentResult"""
        result = SentimentResult(
            polarity=0.5,
            subjectivity=0.8,
            confidence=0.9,
            language='zh',
            raw_score=0.75
        )
        
        assert result.polarity == 0.5
        assert result.subjectivity == 0.8
        assert result.confidence == 0.9
        assert result.language == 'zh'
        assert result.raw_score == 0.75


class TestAnalysisResult:
    """测试AnalysisResult数据类"""
    
    def test_creation(self):
        """测试创建AnalysisResult"""
        sentiment = SentimentResult(
            polarity=0.5, subjectivity=0.6, 
            confidence=0.8, language='zh'
        )
        
        result = AnalysisResult(
            text="测试文本",
            language="zh",
            tokens=["测试", "文本"],
            sentiment=sentiment,
            keywords=[("测试", 1.0)],
            summary="测试摘要",
            word_freq={"测试": 1},
            text_length=4,
            sentence_count=1
        )
        
        assert result.text == "测试文本"
        assert result.language == "zh"
        assert result.tokens == ["测试", "文本"]
        assert result.sentiment.polarity == 0.5


class TestEdgeCases:
    """测试边界情况"""
    
    def test_very_short_text(self, analyzer):
        """测试极短文本"""
        result = analyzer.analyze_sentiment("好")
        assert result.language == 'zh'
    
    def test_only_punctuation(self, analyzer):
        """测试仅标点符号"""
        lang = analyzer.detect_language("！？。，")
        assert lang == 'unknown'
    
    def test_only_numbers(self, analyzer):
        """测试仅数字"""
        lang = analyzer.detect_language("123 456 789")
        assert lang == 'unknown'
    
    def test_unicode_text(self, analyzer):
        """测试Unicode文本"""
        tokens = analyzer.segment("Hello 你好 🎉")
        assert isinstance(tokens, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
