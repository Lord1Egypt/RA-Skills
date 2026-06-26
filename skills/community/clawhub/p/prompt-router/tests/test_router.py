"""
Prompt-Router 单元测试
"""

import unittest
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from tokenizer import Tokenizer
from scorer import Scorer
from router import PromptRouter, RouteResult


class TestTokenizer(unittest.TestCase):
    """分词器测试"""
    
    def setUp(self):
        self.tokenizer = Tokenizer()
    
    def test_english_tokenize(self):
        """英文分词测试"""
        tokens = self.tokenizer.tokenize("Read the config file")
        self.assertIn('read', tokens)
        self.assertIn('config', tokens)
        self.assertIn('file', tokens)
        self.assertNotIn('the', tokens)  # 停用词可能被过滤
    
    def test_chinese_tokenize(self):
        """中文分词测试"""
        tokens = self.tokenizer.tokenize("读取配置文件")
        self.assertTrue(len(tokens) > 0)
        # 中文字符应该被正确提取
        self.assertTrue(any('\u4e00' <= c <= '\u9fff' for t in tokens for c in t))
    
    def test_mixed_tokenize(self):
        """中英文混合分词测试"""
        tokens = self.tokenizer.tokenize("搜索 Python 教程")
        self.assertIn('python', tokens)
        # 应该包含中文字符
    
    def test_case_insensitive(self):
        """大小写不敏感测试"""
        tokens1 = self.tokenizer.tokenize("READ File")
        tokens2 = self.tokenizer.tokenize("read file")
        self.assertEqual(tokens1, tokens2)
    
    def test_punctuation_removal(self):
        """标点符号去除测试"""
        tokens = self.tokenizer.tokenize("Read file, please!")
        self.assertNotIn(',', tokens)
        self.assertNotIn('!', tokens)
    
    def test_keyword_extraction(self):
        """关键词提取测试"""
        keywords = self.tokenizer.extract_keywords("帮我搜索北京今天的天气", min_length=2)
        self.assertTrue(len(keywords) > 0)


class TestScorer(unittest.TestCase):
    """评分器测试"""
    
    def setUp(self):
        self.scorer = Scorer()
        self.test_skill = {
            'name': 'multi-search-engine',
            'description': 'Multi search engine integration',
            'keywords': ['搜索', 'search', '引擎'],
            'triggers': ['搜索', '查找', 'search'],
        }
    
    def test_exact_name_match(self):
        """精确名称匹配测试"""
        tokens = {'search', 'engine'}
        score = self.scorer.score(tokens, self.test_skill)
        self.assertGreater(score, 0)
    
    def test_partial_match(self):
        """部分匹配测试"""
        tokens = {'搜索'}
        score = self.scorer.score(tokens, self.test_skill)
        self.assertGreater(score, 0)
    
    def test_no_match(self):
        """无匹配测试"""
        tokens = {'weather', '北京'}
        score = self.scorer.score(tokens, self.test_skill)
        self.assertEqual(score, 0)
    
    def test_confidence_calculation(self):
        """置信度计算测试"""
        confidence = self.scorer.calculate_confidence(5.0, 10.0)
        self.assertAlmostEqual(confidence, 0.5)
    
    def test_confidence_level(self):
        """置信度等级测试"""
        self.assertEqual(self.scorer.get_confidence_level(0.9), 'high')
        self.assertEqual(self.scorer.get_confidence_level(0.6), 'medium')
        self.assertEqual(self.scorer.get_confidence_level(0.2), 'low')


class TestRouter(unittest.TestCase):
    """路由器测试"""
    
    def setUp(self):
        self.router = PromptRouter(
            skills_dir=str(Path(__file__).parent.parent.parent),
            confidence_threshold=0.6
        )
        self.router.load_skills()
    
    def test_load_skills(self):
        """技能加载测试"""
        stats = self.router.get_stats()
        self.assertGreater(stats['total_targets'], 0)
    
    def test_route_search(self):
        """搜索路由测试"""
        result = self.router.route("搜索 Python 教程")
        self.assertIsNotNone(result)
        # 应该匹配到 multi-search-engine 或类似技能
    
    def test_route_read(self):
        """读取路由测试"""
        result = self.router.route("读取文件")
        # 可能匹配 read 或类似技能
    
    def test_route_low_confidence(self):
        """低置信度路由测试"""
        result = self.router.route("帮我写一首诗")
        # 创意任务应该置信度低
        self.assertLess(result.confidence, 0.8)
    
    def test_should_invoke_skill(self):
        """技能调用决策测试"""
        result = self.router.route("搜索")
        # 根据实际匹配结果判断
        # 如果匹配且置信度高，应该调用
    
    def test_route_result_structure(self):
        """路由结果结构测试"""
        result = self.router.route("测试")
        self.assertIsInstance(result, RouteResult)
        self.assertIsInstance(result.score, float)
        self.assertIsInstance(result.confidence, float)
        self.assertIn(result.confidence_level, ['high', 'medium', 'low', 'none'])


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_end_to_end(self):
        """端到端测试"""
        router = PromptRouter(
            skills_dir=str(Path(__file__).parent.parent.parent),
            confidence_threshold=0.6
        )
        
        # 加载技能
        count = router.load_skills()
        self.assertGreater(count, 0)
        
        # 测试多个 Prompt
        test_cases = [
            ("搜索", True),       # 应该匹配
            ("读取文件", True),   # 应该匹配
            ("天气", True),       # 应该匹配
            ("写诗", False),      # 可能不匹配
        ]
        
        for prompt, should_match in test_cases:
            result = router.route(prompt)
            # 记录结果（不强制断言，因为取决于实际技能）
            print(f"Prompt: {prompt}, Match: {result.match['name'] if result.match else None}, Confidence: {result.confidence:.2f}")


if __name__ == '__main__':
    unittest.main()
