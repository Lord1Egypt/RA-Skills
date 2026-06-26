#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股分析工具 - 基础功能测试
"""

import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_data import StockDataFetcher
from stock_analyzer import StockAnalyzer
from openclaw_notifier import OpenClawNotifier


class TestBasicFunctionality(unittest.TestCase):
    """基础功能测试"""
    
    def setUp(self):
        """测试前准备"""
        self.fetcher = StockDataFetcher()
        self.analyzer = StockAnalyzer()
        self.notifier = OpenClawNotifier()
    
    def test_data_fetcher_initialization(self):
        """测试数据获取器初始化"""
        self.assertIsNotNone(self.fetcher)
        self.assertIsNotNone(self.fetcher.session)
    
    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.industry_benchmarks)
    
    def test_notifier_initialization(self):
        """测试通知器初始化"""
        self.assertIsNotNone(self.notifier)
    
    def test_market_inference(self):
        """测试市场推断"""
        test_cases = [
            ("301682", "创业板"),
            ("688781", "科创板"),
            ("920188", "北交所"),
            ("001257", "深市主板"),
            ("600000", "沪市主板"),
        ]
        
        for code, expected_market in test_cases:
            inferred = self.analyzer._infer_market_from_code(code)
            self.assertEqual(inferred, expected_market, 
                           f"股票代码{code}应该推断为{expected_market}, 但得到{inferred}")
    
    def test_price_formatting(self):
        """测试价格格式化"""
        test_cases = [
            (14.04, "14.04元"),
            (None, "待定"),
            ("待定", "待定"),
            (69.66, "69.66元"),
        ]
        
        for price, expected in test_cases:
            formatted = self.fetcher._format_price(price)
            self.assertEqual(formatted, expected,
                           f"价格{price}应该格式化为{expected}, 但得到{formatted}")
    
    def test_date_formatting(self):
        """测试日期格式化"""
        test_cases = [
            ("2026-03-16", "2026-03-16"),
            ("2026-03-16 00:00:00", "2026-03-16"),
            (None, ""),
            ("", ""),
        ]
        
        for date_str, expected in test_cases:
            formatted = self.fetcher._format_date(date_str)
            self.assertEqual(formatted, expected,
                           f"日期{date_str}应该格式化为{expected}, 但得到{formatted}")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_end_to_end_flow(self):
        """测试端到端流程"""
        try:
            # 1. 初始化组件
            fetcher = StockDataFetcher()
            analyzer = StockAnalyzer()
            
            # 2. 获取数据（使用缓存或模拟数据）
            stocks = fetcher.get_today_stocks()
            
            if not stocks:
                # 如果没有数据，使用模拟数据测试
                print("⚠️ 无实时数据，使用模拟数据测试")
                stocks = [
                    {
                        'code': '301682',
                        'name': '测试股票',
                        'issue_price': 20.0,
                        'issue_pe': 25.0,
                        'industry_pe': 30.0,
                        'issue_num': 1000,
                        'market': '创业板',
                    }
                ]
            
            # 3. 分析数据
            analyses = analyzer.analyze_multiple_stocks(stocks)
            
            # 4. 验证分析结果
            self.assertGreater(len(analyses), 0, "应该至少有一个分析结果")
            
            for analysis in analyses:
                self.assertIn('basic_info', analysis)
                self.assertIn('valuation_analysis', analysis)
                self.assertIn('risk_assessment', analysis)
                self.assertIn('investment_advice', analysis)
                
                # 验证投资建议包含必要字段
                advice = analysis['investment_advice']
                self.assertIn('action', advice)
                self.assertIn('confidence', advice)
                self.assertIn('total_score', advice)
                
                # 验证评分在合理范围内
                self.assertGreaterEqual(advice['total_score'], 0)
                self.assertLessEqual(advice['total_score'], 100)
            
            print("✅ 端到端流程测试通过")
            
        except Exception as e:
            self.fail(f"端到端流程测试失败: {e}")


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def test_invalid_data_handling(self):
        """测试无效数据处理"""
        analyzer = StockAnalyzer()
        
        # 测试无效股票数据
        invalid_stocks = [
            {},  # 空字典
            {'code': None, 'name': None},  # 空值
            {'code': 'INVALID', 'name': '测试'},  # 无效代码
        ]
        
        for stock in invalid_stocks:
            try:
                analysis = analyzer.analyze_stock(stock)
                # 即使无效数据，也应该返回分析结果（可能包含错误标记）
                self.assertIsNotNone(analysis)
            except Exception as e:
                self.fail(f"无效数据处理失败: {e}")
    
    def test_network_error_simulation(self):
        """测试网络错误模拟"""
        fetcher = StockDataFetcher()
        
        # 保存原始session
        original_session = fetcher.session
        
        try:
            # 模拟网络错误（通过设置无效的session）
            class MockSession:
                def get(self, *args, **kwargs):
                    raise ConnectionError("模拟网络错误")
            
            fetcher.session = MockSession()
            
            # 应该能够处理网络错误
            stocks = fetcher.get_today_stocks()
            # 网络错误时应该返回空列表而不是抛出异常
            self.assertEqual(stocks, [])
            
        finally:
            # 恢复原始session
            fetcher.session = original_session


if __name__ == '__main__':
    print("=" * 60)
    print("新股分析工具 - 基础功能测试")
    print("=" * 60)
    
    # 运行测试
    unittest.main(verbosity=2)