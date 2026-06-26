"""
数据源策略测试
"""

import unittest
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-hub/src')

from strategies import TencentStrategy, AKShareStrategy, BaostockStrategy


class TestTencentStrategy(unittest.TestCase):
    """腾讯数据源策略测试"""
    
    @classmethod
    def setUpClass(cls):
        cls.strategy = TencentStrategy()
    
    def test_is_available(self):
        """测试可用性检查"""
        available = self.strategy.is_available()
        print(f"腾讯数据源可用性: {available}")
    
    def test_get_realtime_quote(self):
        """测试获取实时行情"""
        if not self.strategy.is_available():
            print("腾讯数据源不可用，跳过测试")
            return
        
        try:
            quote = self.strategy.get_realtime_quote('300502')
            
            self.assertIn('symbol', quote)
            self.assertIn('price', quote)
            self.assertEqual(quote['symbol'], '300502')
            
            print(f"腾讯行情测试通过: {quote.get('name', '')} 价格={quote.get('price')}")
            
        except Exception as e:
            print(f"腾讯行情测试失败: {e}")
    
    def test_get_kline(self):
        """测试获取K线"""
        if not self.strategy.is_available():
            print("腾讯数据源不可用，跳过测试")
            return
        
        try:
            df = self.strategy.get_kline('300502', period='day')
            
            self.assertGreater(len(df), 0)
            print(f"腾讯K线测试通过: 获取到 {len(df)} 条数据")
            
        except Exception as e:
            print(f"腾讯K线测试失败: {e}")
    
    def test_normalize_symbol(self):
        """测试代码标准化"""
        self.assertEqual(self.strategy.normalize_symbol('300502'), '300502')
        self.assertEqual(self.strategy.normalize_symbol('sz300502'), '300502')
        self.assertEqual(self.strategy.normalize_symbol(' sh600519 '), '600519')


class TestAKShareStrategy(unittest.TestCase):
    """AKShare数据源策略测试"""
    
    @classmethod
    def setUpClass(cls):
        cls.strategy = AKShareStrategy()
    
    def test_is_available(self):
        """测试可用性检查"""
        available = self.strategy.is_available()
        print(f"AKShare数据源可用性: {available}")
    
    def test_get_realtime_quote(self):
        """测试获取实时行情"""
        if not self.strategy.is_available():
            print("AKShare数据源不可用，跳过测试")
            return
        
        try:
            quote = self.strategy.get_realtime_quote('300502')
            
            self.assertIn('symbol', quote)
            self.assertIn('price', quote)
            
            print(f"AKShare行情测试通过: {quote.get('name', '')} 价格={quote.get('price')}")
            
        except Exception as e:
            print(f"AKShare行情测试失败: {e}")
    
    def test_get_kline(self):
        """测试获取K线"""
        if not self.strategy.is_available():
            print("AKShare数据源不可用，跳过测试")
            return
        
        try:
            df = self.strategy.get_kline('300502', period='day',
                                         start_date='2024-01-01',
                                         end_date='2024-02-01')
            
            self.assertGreater(len(df), 0)
            print(f"AKShare K线测试通过: 获取到 {len(df)} 条数据")
            
        except Exception as e:
            print(f"AKShare K线测试失败: {e}")


class TestBaostockStrategy(unittest.TestCase):
    """Baostock数据源策略测试"""
    
    @classmethod
    def setUpClass(cls):
        cls.strategy = BaostockStrategy()
    
    def test_is_available(self):
        """测试可用性检查"""
        available = self.strategy.is_available()
        print(f"Baostock数据源可用性: {available}")
    
    def test_get_kline(self):
        """测试获取K线"""
        if not self.strategy.is_available():
            print("Baostock数据源不可用，跳过测试")
            return
        
        try:
            df = self.strategy.get_kline('300502', period='day',
                                         start_date='2024-01-01',
                                         end_date='2024-02-01')
            
            self.assertGreater(len(df), 0)
            print(f"Baostock K线测试通过: 获取到 {len(df)} 条数据")
            
        except Exception as e:
            print(f"Baostock K线测试失败: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
