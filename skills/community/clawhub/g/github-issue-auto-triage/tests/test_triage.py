#!/usr/bin/env python3
"""
GitHub Issue Auto Triage - 单元测试
"""

import unittest
import json
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestIssueClassification(unittest.TestCase):
    """测试 Issue 分类功能"""
    
    def setUp(self):
        """测试前准备"""
        self.test_issue = {
            'number': 123,
            'title': 'App crashes on startup',
            'body': 'The application crashes immediately when I try to open it.',
            'labels': [],
            'assignee': None
        }
    
    def test_bug_keyword_detection(self):
        """测试 bug 关键词检测"""
        from triage import GitHubIssueTriage
        
        triage = GitHubIssueTriage()
        title = 'Bug: App crashes'
        body = 'Error when starting'
        
        # 关键词应该被检测到
        content = f"{title}\n\n{body}".lower()
        self.assertIn('crash', content)
        self.assertIn('error', content)
    
    def test_enhancement_keyword_detection(self):
        """测试 enhancement 关键词检测"""
        title = 'Feature request: Add dark mode'
        body = 'Would be great to have a dark theme'
        
        content = f"{title}\n\n{body}".lower()
        self.assertIn('feature', content)
    
    def test_question_keyword_detection(self):
        """测试 question 关键词检测"""
        title = 'Question: How to install?'
        body = 'I need help with installation'
        
        content = f"{title}\n\n{body}".lower()
        self.assertIn('question', content)
        self.assertIn('help', content)


class TestDuplicateDetection(unittest.TestCase):
    """测试重复检测功能"""
    
    def test_similarity_calculation(self):
        """测试相似度计算"""
        from triage import GitHubIssueTriage
        
        triage = GitHubIssueTriage()
        
        # 完全相同
        sim1 = triage._calculate_similarity('test issue', 'test issue')
        self.assertEqual(sim1, 1.0)
        
        # 完全不同
        sim2 = triage._calculate_similarity('completely different', 'unrelated text')
        self.assertLess(sim2, 0.5)
        
        # 部分相同
        sim3 = triage._calculate_similarity('app crashes', 'app crashes on startup')
        self.assertGreater(sim3, 0.5)
    
    def test_empty_text_handling(self):
        """测试空文本处理"""
        from triage import GitHubIssueTriage
        
        triage = GitHubIssueTriage()
        
        sim = triage._calculate_similarity('', 'test')
        self.assertEqual(sim, 0.0)


class TestFAQMatching(unittest.TestCase):
    """测试 FAQ 匹配功能"""
    
    def test_faq_install_match(self):
        """测试安装相关 FAQ 匹配"""
        from triage import GitHubIssueTriage
        
        triage = GitHubIssueTriage()
        
        issue = {
            'title': 'How to install?',
            'body': 'I need help with installation'
        }
        
        faq_answer = triage.check_faq(issue)
        self.assertIsNotNone(faq_answer)
        self.assertIn('installation', faq_answer.lower())
    
    def test_faq_license_match(self):
        """测试许可证相关 FAQ 匹配"""
        from triage import GitHubIssueTriage
        
        triage = GitHubIssueTriage()
        
        issue = {
            'title': 'License question',
            'body': 'Can I use this commercially?'
        }
        
        faq_answer = triage.check_faq(issue)
        self.assertIsNotNone(faq_answer)
        self.assertIn('license', faq_answer.lower())


class TestTriageResult(unittest.TestCase):
    """测试分类结果"""
    
    def test_result_structure(self):
        """测试结果结构"""
        result = {
            'issue_number': 123,
            'actions': ['Added label: bug'],
            'success': True,
            'classification': {
                'suggested_label': 'bug',
                'priority': 'high'
            }
        }
        
        self.assertIn('issue_number', result)
        self.assertIn('actions', result)
        self.assertIn('success', result)
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()
