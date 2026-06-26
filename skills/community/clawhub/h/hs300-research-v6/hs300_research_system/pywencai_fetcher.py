#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺问财 (pywencai) 数据源模块

用于通过自然语言查询获取财经数据，作为投研系统的补充数据源。
"""

import os
import sys
import io
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import pywencai
    PYWENCAI_AVAILABLE = True
except ImportError:
    PYWENCAI_AVAILABLE = False
    pywencai = None

logger = logging.getLogger(__name__)


class PywencaiFetcher:
    """
    同花顺问财数据获取器

    通过自然语言问句查询各类财经数据，返回 DataFrame 格式。
    作为投研系统的补充数据源（优先级3，位于东方财富/Tushare之后）。
    """

    def __init__(self, cookie=None):
        self.cookie = cookie
        self._source_stats = {'pywencai': 0, 'failed': 0}

    def query(self, query_str, query_type='stock', sort_key=None, sort_order='desc',
              perpage=100, page=1, loop=False, no_detail=True):
        """
        执行问财自然语言查询

        Args:
            query_str: 自然语言查询问句
            query_type: 查询类型 (stock/zhishu/fund/hkstock/usstock/conbond)
            sort_key: 排序字段
            sort_order: 排序规则 (asc/desc)
            perpage: 每页条数 (默认100, 最大100)
            page: 页码
            loop: 是否循环获取全部数据
            no_detail: True 时只返回DataFrame, False 时详情查询返回字典

        Returns:
            pd.DataFrame 或 None
        """
        if not PYWENCAI_AVAILABLE:
            logger.warning("pywencai 未安装")
            self._source_stats['failed'] += 1
            return None

        try:
            kwargs = {
                'query': query_str,
                'query_type': query_type,
                'perpage': min(perpage, 100),
                'page': page,
                'loop': loop,
                'no_detail': no_detail,
                'retry': 3,
            }
            if sort_key:
                kwargs['sort_key'] = sort_key
            if sort_order:
                kwargs['sort_order'] = sort_order
            if self.cookie:
                kwargs['cookie'] = self.cookie

            result = pywencai.get(**kwargs)
            if result is not None and isinstance(result, pd.DataFrame) and len(result) > 0:
                self._source_stats['pywencai'] += 1
                return result
            return None
        except Exception as e:
            logger.debug(f"pywencai 查询失败 [{query_str[:50]}]: {e}")
            self._source_stats['failed'] += 1
            return None

    # ====== 预设查询方法 ======

    def get_hs300_stocks_fundamentals(self):
        """获取沪深300成分股 + 基本面数据"""
        return self.query(
            '沪深300成分股',
            sort_key='总市值',
            sort_order='desc',
            perpage=100
        )

    def get_stock_with_filters(self, conditions, fields=None, sort_key=None):
        """
        按条件筛选股票

        Args:
            conditions: 筛选条件字符串，如 '市盈率小于20并且ROE大于15'
            fields: 返回字段列表
            sort_key: 排序字段

        Returns:
            pd.DataFrame
        """
        return self.query(conditions, sort_key=sort_key or '总市值')

    def get_stock_fund_flow(self, period='今日'):
        """
        获取个股资金流向排行

        Args:
            period: 时间周期 (今日/3日/5日/10日/20日)

        Returns:
            pd.DataFrame
        """
        return self.query(f'{period}主力资金净流入排行', sort_key='主力资金净流入(元)')

    def get_industry_fund_flow(self, period='今日'):
        """
        获取行业板块资金流向

        Args:
            period: 时间周期

        Returns:
            pd.DataFrame
        """
        return self.query(f'{period}行业板块资金流向', sort_key='主力净流入(元)',
                          query_type='zhishu')

    def get_concept_fund_flow(self, period='今日'):
        """
        获取概念板块资金流向

        Args:
            period: 时间周期

        Returns:
            pd.DataFrame
        """
        return self.query(f'{period}概念板块资金流向', sort_key='主力净流入(元)',
                          query_type='zhishu')

    def get_stock_rise_fall(self, days):
        """
        获取连涨/连跌股票

        Args:
            days: 连涨/连跌天数，如 5

        Returns:
            pd.DataFrame
        """
        return self.query(f'连续{days}天上涨', sort_key='涨跌幅')

    def get_stock_new_high(self, days=60):
        """
        获取创新高的股票

        Args:
            days: 周期天数

        Returns:
            pd.DataFrame
        """
        return self.query(f'{days}日新高', sort_key='涨跌幅')

    def get_stock_breakout(self):
        """获取突破重要压力位的股票"""
        return self.query('突破重要压力位', sort_key='涨跌幅')

    def get_stock_macd_golden(self):
        """获取MACD金叉股票"""
        return self.query('MACD金叉', sort_key='涨跌幅')

    def get_stock_kdj_golden(self):
        """获取KDJ金叉股票"""
        return self.query('KDJ金叉', sort_key='涨跌幅')

    def get_stock_dual_golden(self):
        """获取MACD和KDJ同时金叉的股票"""
        return self.query('MACD金叉并且KDJ金叉', sort_key='涨跌幅')

    def get_stock_limit_up(self):
        """获取涨停股票"""
        return self.query('今日涨停', sort_key='封板资金(元)')

    def get_stock_limit_down(self):
        """获取跌停股票"""
        return self.query('今日跌停', sort_key='涨跌幅')

    def get_stock_oversold(self):
        """获取超跌反弹股票"""
        return self.query('RSI超卖', sort_key='涨跌幅')

    def get_stock_high_dividend(self):
        """获取高股息股票"""
        return self.query('股息率大于4%', sort_key='股息率')

    def get_stock_low_pe(self, pe_threshold=15):
        """获取低PE股票"""
        return self.query(f'市盈率小于{pe_threshold}', sort_key='市盈率')

    def get_stock_high_roe(self, roe_threshold=20):
        """获取高ROE股票"""
        return self.query(f'ROE大于{roe_threshold}%', sort_key='ROE')

    def get_stock_revenue_growth(self, growth_threshold=30):
        """获取营收高增长股票"""
        return self.query(f'营收增长率大于{growth_threshold}%', sort_key='营收增长率')

    def get_north_bound_flow(self):
        """获取北向资金持仓变动"""
        return self.query('北向资金增持', sort_key='北向资金净买入(股)')

    def get_institution_buy(self):
        """获取机构买入股票"""
        return self.query('机构买入评级', sort_key='目标价')

    def get_fund_hold_change(self, quarter=None):
        """获取基金持仓变动"""
        if quarter:
            return self.query(f'{quarter}基金加仓', sort_key='基金持股变动(股)')
        return self.query('最近一季基金加仓', sort_key='基金持股变动(股)')

    def get_stock_volume_breakout(self):
        """获取放量突破的股票"""
        return self.query('放量突破', sort_key='成交量/均价')

    def get_stock_price_break_ma(self, ma_days=60):
        """获取股价突破均线的股票"""
        return self.query(f'股价突破{ma_days}日均线', sort_key='涨跌幅')

    def custom_query(self, query_str, **kwargs):
        """自定义查询 — 直接传入问财语句"""
        return self.query(query_str, **kwargs)

    def get_source_stats(self):
        """获取数据源使用统计"""
        return self._source_stats.copy()

    def print_source_stats(self):
        """打印数据源统计"""
        stats = self.get_source_stats()
        total = sum(stats.values())
        if total > 0:
            logger.info(f"  问财(pywencai): {stats['pywencai']}次")
            logger.info(f"  失败: {stats['failed']}次")


def demo():
    """演示用法"""
    if not PYWENCAI_AVAILABLE:
        print("pywencai 未安装: pip install pywencai")
        return

    fetcher = PywencaiFetcher()

    print("=" * 60)
    print("  pywencai 同花顺问财数据源演示")
    print("=" * 60)

    # 1. 沪深300成分股
    print("\n[1] 沪深300成分股（前10）...")
    df = fetcher.get_hs300_stocks_fundamentals()
    if df is not None:
        print(f"  获取到 {len(df)} 只股票")
        print(df.head(3).to_string())
    else:
        print("  获取失败")

    # 2. MACD金叉
    print("\n[2] MACD金叉股票（前5）...")
    df = fetcher.get_stock_macd_golden()
    if df is not None:
        print(f"  获取到 {len(df)} 只")
        print(df.head(5).to_string())
    else:
        print("  获取失败")

    # 3. 资金流向
    print("\n[3] 今日主力资金净流入（前5）...")
    df = fetcher.get_stock_fund_flow('今日')
    if df is not None:
        print(f"  获取到 {len(df)} 只")
        print(df.head(5).to_string())
    else:
        print("  获取失败")

    # 4. 自定义查询
    print("\n[4] 自定义查询: 市盈率小于20并且ROE大于15% ...")
    df = fetcher.custom_query('市盈率小于20并且ROE大于15%', sort_key='总市值')
    if df is not None:
        print(f"  获取到 {len(df)} 只")
        print(df.head(3).to_string())
    else:
        print("  获取失败")

    print("\n" + "=" * 60)
    fetcher.print_source_stats()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    demo()
