#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 数据采集模块 v5.2

📋 数据源架构:
- 东方财富 — 行情K线/估值 → 优先级1（HTTP接口，最快）
- Tushare Pro — 日线/基本面 → 优先级2
- AKShare — 兜底方案 → 优先级3
- pywencai(同花顺问财) — 自然语言补充查询 → 优先级4（信号/资金流）
- 深交所(SZSE) / 上交所(SSE) — 辅助数据源

⚠️ JQData(聚宽) 已禁用 — 免费版数据截止2026-02-10，无最新数据
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import akshare as ak
import pickle
import time
import requests

# ===== 数据源 5: 深交所 (SZSE) =====
try:
    from szse_fetcher import SZSEFetcher
    SZSE_AVAILABLE = True
except Exception:
    SZSE_AVAILABLE = False

# ===== 数据源 6: 上交所 (SSE) =====
try:
    from sse_fetcher import SSEFetcher
    SSE_AVAILABLE = True
except Exception:
    SSE_AVAILABLE = False

from config import DATA_DIR, CACHE_CONFIG

# ===== 数据源 1: JQData =====
try:
    from jq_config import JQ_USER, JQ_PASSWORD, JQ_AUTH
    import jqdatasdk as _jq
    JQ_AVAILABLE = JQ_AUTH and True
except Exception:
    JQ_AVAILABLE = False

# ===== 数据源 2: Tushare Pro =====
try:
    from tushare_config import TUSHARE_TOKEN, TUSHARE_AUTH
    import tushare as _ts
    if TUSHARE_AUTH and TUSHARE_TOKEN:
        _ts.set_token(TUSHARE_TOKEN)
        TUSHARE_AVAILABLE = True
    else:
        TUSHARE_AVAILABLE = False
except Exception:
    TUSHARE_AVAILABLE = False

logger = logging.getLogger(__name__)

# ===== 数据源 7: pywencai(同花顺问财) =====
PYWENCAI_AVAILABLE = False
try:
    from pywencai_fetcher import PywencaiFetcher
    PYWENCAI_AVAILABLE = True
except Exception:
    pass


def _jq_login():
    if not JQ_AVAILABLE:
        return False
    try:
        _jq.auth(JQ_USER, JQ_PASSWORD)
        logger.info("✅ JQData 登录成功")
        return True
    except Exception as e:
        logger.warning(f"❌ JQData 登录失败: {e}")
        return False


def _get_tushare_pro():
    """获取 Tushare Pro 接口"""
    if not TUSHARE_AVAILABLE:
        return None
    try:
        pro = _ts.pro_api()
        return pro
    except Exception as e:
        logger.warning(f"❌ Tushare Pro 初始化失败: {e}")
        return None


class DataFetcher:
    """数据采集类 v5.2 — 三大数据源 + pywencai + 辅助数据源"""

    def __init__(self):
        self.cache_dir = CACHE_CONFIG['path']
        if CACHE_CONFIG['enable'] and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self._jq_logged_in = False
        self._tushare_pro = None
        self._szse_fetcher = None
        self._sse_fetcher = None
        self._pywencai_fetcher = None
        self._source_stats = {
            'eastmoney': 0, 'tushare': 0, 'akshare': 0, 'pywencai': 0,
            'szse': 0, 'sse': 0, 'failed': 0
        }

    def _get_jq_date(self):
        """获取 JQData 可用的最新日期（免费版有限制）"""
        today = datetime.now().strftime('%Y-%m-%d')
        # 免费版数据范围有限制，先用今天的日期尝试
        try:
            # 快速测试：用沪深300指数做简单查询
            _jq.get_price('000300.XSHG', start_date=today, end_date=today, frequency='daily')
            return today
        except Exception:
            # 自动回退到已知可用的最大日期
            # JQData 免费版数据范围：2025-02-03 至 2026-02-10
            # 如果查询失败，默认使用最后可用日期
            return '2026-02-10'

    def _ensure_jq(self):
        if not self._jq_logged_in and JQ_AVAILABLE:
            self._jq_logged_in = _jq_login()
        return self._jq_logged_in

    def _ensure_tushare(self):
        if self._tushare_pro is None and TUSHARE_AVAILABLE:
            self._tushare_pro = _get_tushare_pro()
        return self._tushare_pro is not None

    def _ensure_szse(self):
        if self._szse_fetcher is None and SZSE_AVAILABLE:
            try:
                cache_path = os.path.join(self.cache_dir, 'szse')
                self._szse_fetcher = SZSEFetcher(cache_dir=cache_path)
                return True
            except Exception as e:
                logger.warning(f"SZSE初始化失败: {e}")
                return False
        return self._szse_fetcher is not None

    def _ensure_sse(self):
        if self._sse_fetcher is None and SSE_AVAILABLE:
            try:
                cache_path = os.path.join(self.cache_dir, 'sse')
                self._sse_fetcher = SSEFetcher(cache_dir=cache_path)
                return True
            except Exception as e:
                logger.warning(f"SSE初始化失败: {e}")
                return False
        return self._sse_fetcher is not None

    def _ensure_pywencai(self):
        """确保 pywencai fetcher 已初始化"""
        if self._pywencai_fetcher is None and PYWENCAI_AVAILABLE:
            try:
                self._pywencai_fetcher = PywencaiFetcher()
                return True
            except Exception as e:
                logger.warning(f"pywencai初始化失败: {e}")
                return False
        return self._pywencai_fetcher is not None

    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f'{key}.pkl')

    def _load_cache(self, key, expire_hours=None):
        if not CACHE_CONFIG['enable']:
            return None
        path = self._get_cache_path(key)
        if not os.path.exists(path):
            return None
        expire = expire_hours or CACHE_CONFIG['expire_hours']
        if datetime.now() - datetime.fromtimestamp(os.path.getmtime(path)) > timedelta(hours=expire):
            return None
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    def _save_cache(self, key, data):
        if not CACHE_CONFIG['enable']:
            return
        try:
            with open(self._get_cache_path(key), 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.warning(f"保存缓存失败 {key}: {e}")

    def get_hs300_stocks(self):
        """获取沪深300成分股"""
        cached = self._load_cache('hs300_stocks', expire_hours=48)
        if cached:
            return cached
        try:
            df = ak.index_stock_cons(symbol="000300")
            if df is not None and len(df) > 0:
                if '品种代码' in df.columns:
                    df = df.rename(columns={'品种代码': 'code', '品种名称': 'name'})
                stocks = df[['code', 'name']].to_dict('records')
                self._save_cache('hs300_stocks', stocks)
                return stocks
            return []
        except Exception as e:
            logger.error(f"获取沪深300成分股失败: {e}")
            return []

    # ==================== 行情K线数据 ====================

    def get_stock_daily_eastmoney(self, stock_code):
        """
        东方财富接口获取日K线
        """
        cache_key = f'daily_em_{stock_code}'
        cached = self._load_cache(cache_key, expire_hours=6)
        if cached is not None:
            self._source_stats['eastmoney'] += 1
            return cached

        try:
            secid = f"1.{stock_code}" if stock_code.startswith('6') else f"0.{stock_code}"
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                "secid": secid,
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "klt": "101",
                "fqt": "1",
                "beg": "20250101",
                "end": "20261231",
                "lmt": "500",
            }
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()

            if data.get('data') and data['data'].get('klines'):
                klines = data['data']['klines']
                records = []
                for line in klines:
                    parts = line.split(',')
                    if len(parts) >= 6:
                        records.append({
                            'date': parts[0],
                            'open': float(parts[1]),
                            'close': float(parts[2]),
                            'high': float(parts[3]),
                            'low': float(parts[4]),
                            'volume': float(parts[5]),
                        })
                df = pd.DataFrame(records)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                df['pct_chg'] = df['close'].pct_change() * 100
                df['amount'] = df['volume'] * df['close']
                self._save_cache(cache_key, df)
                self._source_stats['eastmoney'] += 1
                return df
            return None
        except Exception as e:
            logger.warning(f"东方财富接口获取 {stock_code} 失败: {e}")
            return None

    def get_stock_daily_tushare(self, stock_code):
        """Tushare Pro 获取日线"""
        cache_key = f'daily_ts_{stock_code}'
        cached = self._load_cache(cache_key, expire_hours=6)
        if cached is not None:
            return cached

        if not self._ensure_tushare():
            return None

        try:
            ts_code = self._to_ts_code(stock_code)
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=400)).strftime('%Y%m%d')

            df = self._tushare_pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df is not None and len(df) > 0:
                df = df.rename(columns={
                    'trade_date': 'date', 'vol': 'volume'
                })
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                df['pct_chg'] = df.get('pct_chg', pd.Series(dtype=float))
                df['amount'] = df.get('amount', df.get('volume', pd.Series(dtype=float)) * df.get('close', pd.Series(dtype=float)))
                self._save_cache(cache_key, df)
                self._source_stats['tushare'] += 1
                return df
            return None
        except Exception as e:
            logger.debug(f"Tushare Pro 日线获取失败 {stock_code}: {e}")
            return None

    def get_stock_daily_jq(self, stock_code):
        """JQData 获取日线（注意：免费版数据范围有限制）"""
        cache_key = f'daily_jq_{stock_code}'
        cached = self._load_cache(cache_key, expire_hours=6)
        if cached is not None:
            return cached

        if not self._ensure_jq():
            return None

        try:
            jq_code = self._to_jq_code(stock_code)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=400)).strftime('%Y-%m-%d')

            try:
                df = _jq.get_price(jq_code, start_date=start_date, end_date=end_date,
                                   frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money'])
            except Exception as jq_err:
                err_msg = str(jq_err)
                # 自动从错误中提取可用日期范围并重试
                import re
                match = re.search(r'(\d{4}-\d{2}-\d{2}).*?(\d{4}-\d{2}-\d{2})', err_msg)
                if match:
                    new_start = match.group(1)
                    new_end = match.group(2)
                    logger.info(f"JQData 日期范围调整: {new_start} 至 {new_end}")
                    df = _jq.get_price(jq_code, start_date=new_start, end_date=new_end,
                                       frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money'])
                else:
                    logger.debug(f"JQData 日期错误无法解析: {err_msg[:100]}")
                    raise
            if df is not None and len(df) > 0:
                df = df.reset_index()
                # JQData 的 date 列可能叫 'date' 或 'index'
                date_col = 'date' if 'date' in df.columns else 'index'
                df = df.rename(columns={date_col: 'date', 'money': 'amount'})
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                df['pct_chg'] = df['close'].pct_change() * 100
                self._save_cache(cache_key, df)
                self._source_stats['jq'] += 1
                return df
            return None
        except Exception as e:
            logger.debug(f"JQData 日线获取失败 {stock_code}: {e}")
            return None

    def get_stock_daily_akshare(self, stock_code, start_date=None, end_date=None):
        """AKShare 获取日线（降级方案）"""
        cache_key = f'daily_ak_{stock_code}'
        cached = self._load_cache(cache_key)
        if cached is not None:
            return cached

        try:
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=400)).strftime('%Y%m%d')

            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily",
                                    start_date=start_date, end_date=end_date, adjust="qfq")
            if df is not None and len(df) > 0:
                df = df.rename(columns={
                    '日期': 'date', '开盘': 'open', '收盘': 'close',
                    '最高': 'high', '最低': 'low', '成交量': 'volume',
                    '成交额': 'amount', '涨跌幅': 'pct_chg'
                })
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                self._save_cache(cache_key, df)
                self._source_stats['akshare'] += 1
                return df
            return None
        except Exception as e:
            logger.warning(f"AKShare 获取 {stock_code} 失败: {e}")
            return None

    def get_stock_daily(self, stock_code, start_date=None, end_date=None):
        """
        获取个股日线 — 三数据源降级链:
        东方财富(最快) → Tushare Pro → AKShare(兜底)
        """
        # 优先级1: 东方财富（HTTP接口，最快）
        df = self.get_stock_daily_eastmoney(stock_code)
        if df is not None and len(df) >= 30:
            return df

        # 优先级2: Tushare Pro
        df = self.get_stock_daily_tushare(stock_code)
        if df is not None and len(df) >= 30:
            return df

        # 优先级3: AKShare（降级方案）
        df = self.get_stock_daily_akshare(stock_code, start_date, end_date)
        if df is not None and len(df) >= 30:
            return df

        self._source_stats['failed'] += 1
        return None

    # ==================== 基本面数据 ====================

    def get_stock_valuation(self, stock_code):
        """估值指标（PE/PB/PS/PCF/市值）"""
        cache_key = f'valuation_{stock_code}'
        cached = self._load_cache(cache_key, expire_hours=6)
        if cached is not None:
            return cached

        result = {}

        # 优先级1: Tushare Pro
        if not result.get('pe_ttm') and self._ensure_tushare():
            try:
                jq_code = self._to_jq_code(stock_code)
                jq_date = self._get_jq_date()
                df = _jq.get_fundamentals(
                    _jq.query(_jq.valuation.pe_ratio, _jq.valuation.pb_ratio,
                              _jq.valuation.ps_ratio, _jq.valuation.pcf_ratio,
                              _jq.valuation.market_cap)
                    .filter(_jq.valuation.code == jq_code),
                    date=jq_date
                )
                if df is not None and len(df) > 0:
                    result = {
                        'pe_ttm': self._safe_f(df['pe_ratio'].iloc[0]),
                        'pb': self._safe_f(df['pb_ratio'].iloc[0]),
                        'ps_ttm': self._safe_f(df['ps_ratio'].iloc[0]),
                        'pcf': self._safe_f(df['pcf_ratio'].iloc[0]),
                        'market_cap': self._safe_f(df['market_cap'].iloc[0]),
                    }
                    self._source_stats['jq'] += 1
            except Exception as e:
                logger.debug(f"JQData 估值获取失败: {e}")

        # 优先级2: Tushare Pro
        if not result.get('pe_ttm') and self._ensure_tushare():
            try:
                ts_code = self._to_ts_code(stock_code)
                today = datetime.now().strftime('%Y%m%d')
                # 日线数据中有PE/PB
                df = self._tushare_pro.daily_basic(ts_code=ts_code, start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'), end_date=today,
                                                    fields='ts_code,trade_date,pe_ttm,pb,ps_ttm,total_mv')
                if df is not None and len(df) > 0:
                    latest = df.iloc[0]
                    if result:
                        result['pe_ttm'] = result.get('pe_ttm') or self._safe_f(latest.get('pe_ttm'))
                        result['pb'] = result.get('pb') or self._safe_f(latest.get('pb'))
                        result['ps_ttm'] = result.get('ps_ttm') or self._safe_f(latest.get('ps_ttm'))
                        result['market_cap'] = result.get('market_cap') or self._safe_f(latest.get('total_mv'))
                    else:
                        result = {
                            'pe_ttm': self._safe_f(latest.get('pe_ttm')),
                            'pb': self._safe_f(latest.get('pb')),
                            'ps_ttm': self._safe_f(latest.get('ps_ttm')),
                            'market_cap': self._safe_f(latest.get('total_mv')),
                        }
                    self._source_stats['tushare'] += 1
            except Exception as e:
                logger.debug(f"Tushare Pro 估值获取失败: {e}")

        # 优先级2: 东方财富
        if not result.get('pe_ttm'):
            try:
                df = ak.stock_individual_info_em(symbol=stock_code)
                val = {'pe_ttm': None, 'pb': None, 'ps_ttm': None, 'pcf': None, 'market_cap': None}
                for _, row in df.iterrows():
                    item = str(row.get('item', ''))
                    value = row.get('value', '')
                    try:
                        if '市盈率' in item:
                            val['pe_ttm'] = float(value)
                        elif '市净率' in item:
                            val['pb'] = float(value)
                        elif '总市值' in item:
                            val['market_cap'] = float(value) / 1e8
                    except (ValueError, TypeError):
                        pass
                if val.get('pe_ttm'):
                    result.update(val)
                    self._source_stats['eastmoney'] += 1
            except Exception as e:
                logger.debug(f"东方财富 估值获取失败 {stock_code}: {e}")

        # 优先级3: AKShare
        if not result.get('pe_ttm'):
            try:
                df = ak.stock_a_indicator_lg(symbol=stock_code)
                if df is not None and len(df) > 0:
                    latest = df.iloc[0]
                    result = {
                        'pe_ttm': self._safe_f(latest.get('pe')),
                        'pb': self._safe_f(latest.get('pb')),
                        'ps_ttm': self._safe_f(latest.get('ps')),
                        'pcf': self._safe_f(latest.get('pcf')),
                        'market_cap': self._safe_f(latest.get('total_mv')) / 1e8 if latest.get('total_mv') else None,
                    }
                    self._source_stats['akshare'] += 1
            except Exception as e:
                logger.debug(f"AKShare 估值获取失败 {stock_code}: {e}")

        if not result:
            self._source_stats['failed'] += 1
            return None

        self._save_cache(cache_key, result)
        return result

    def get_stock_financial_indicator(self, stock_code):
        """财务指标（ROE/ROA/毛利率/净利率）"""
        cache_key = f'fin_indicator_{stock_code}'
        cached = self._load_cache(cache_key, expire_hours=720)
        if cached is not None:
            return cached

        result = {}

        # 优先级1: Tushare Pro
        if not result.get('roe') and self._ensure_tushare():
            try:
                jq_code = self._to_jq_code(stock_code)
                jq_date = self._get_jq_date()
                df = _jq.get_fundamentals(
                    _jq.query(_jq.indicator.roe, _jq.indicator.roa,
                              _jq.indicator.gross_profit_margin,
                              _jq.indicator.net_profit_margin)
                    .filter(_jq.indicator.code == jq_code),
                    date=jq_date
                )
                if df is not None and len(df) > 0:
                    result = {
                        'roe': self._safe_f(df['roe'].iloc[0]),
                        'roa': self._safe_f(df['roa'].iloc[0]),
                        'gross_profit_margin': self._safe_f(df['gross_profit_margin'].iloc[0]),
                        'net_profit_margin': self._safe_f(df['net_profit_margin'].iloc[0]),
                    }
                    self._source_stats['jq'] += 1
            except Exception as e:
                logger.debug(f"JQData 财务指标获取失败: {e}")

        # 优先级2: Tushare Pro
        if not result.get('roe') and self._ensure_tushare():
            try:
                ts_code = self._to_ts_code(stock_code)
                df = self._tushare_pro.fina_indicator(ts_code=ts_code)
                if df is not None and len(df) > 0:
                    latest = df.iloc[0]
                    result = {
                        'roe': self._safe_f(latest.get('roe')) * 100 if latest.get('roe') else None,
                        'roa': self._safe_f(latest.get('roa')) * 100 if latest.get('roa') else None,
                        'gross_profit_margin': self._safe_f(latest.get('gross_margin')) * 100 if latest.get('gross_margin') else None,
                        'net_profit_margin': self._safe_f(latest.get('netprofit_margin')) * 100 if latest.get('netprofit_margin') else None,
                    }
                    result = {k: v if (v is None or -50 < v < 100) else None for k, v in result.items()}
                    self._source_stats['tushare'] += 1
            except Exception as e:
                logger.debug(f"Tushare Pro 财务指标获取失败: {e}")

        # 优先级2: AKShare
        if not result.get('roe'):
            try:
                df = ak.stock_financial_analysis_indicator(symbol=stock_code)
                if df is not None and len(df) > 0:
                    latest = df.iloc[0]
                    result = {
                        'roe': self._safe_float(self._find_col(latest, '净资产收益率')),
                        'roa': self._safe_float(self._find_col(latest, '总资产净利率')),
                        'gross_profit_margin': self._safe_float(self._find_col(latest, '销售毛利率')),
                        'net_profit_margin': self._safe_float(self._find_col(latest, '销售净利率')),
                    }
                    self._source_stats['akshare'] += 1
            except Exception as e:
                logger.debug(f"AKShare 财务指标获取失败 {stock_code}: {e}")

        if not result:
            self._source_stats['failed'] += 1
            return None

        self._save_cache(cache_key, result)
        return result

    def get_stock_income(self, stock_code):
        """利润表（营收/利润增长）"""
        cache_key = f'income_{stock_code}'
        cached = self._load_cache(cache_key, expire_hours=720)
        if cached is not None:
            return cached

        result = {}

        # 优先级1: Tushare Pro
        if not result.get('revenue_growth') and self._ensure_tushare():
            try:
                jq_code = self._to_jq_code(stock_code)
                jq_date = self._get_jq_date()
                # JQData 收入表需要 date 参数（返回最近一季数据）
                # 需要查多个日期来获取同比数据
                curr = _jq.get_fundamentals(
                    _jq.query(_jq.income.operating_revenue, _jq.income.net_profit)
                    .filter(_jq.income.code == jq_code),
                    date=jq_date
                )
                if curr is not None and len(curr) > 0:
                    curr_rev = self._safe_f(curr['operating_revenue'].iloc[0])
                    curr_prof = self._safe_f(curr['net_profit'].iloc[0])
                    # 查去年同期数据
                    try:
                        prev_date = str(int(jq_date.split('-')[0]) - 1) + '-' + jq_date.split('-')[1] + '-' + jq_date.split('-')[2]
                        prev = _jq.get_fundamentals(
                            _jq.query(_jq.income.operating_revenue, _jq.income.net_profit)
                            .filter(_jq.income.code == jq_code),
                            date=prev_date
                        )
                        if prev is not None and len(prev) > 0:
                            prev_rev = self._safe_f(prev['operating_revenue'].iloc[0])
                            prev_prof = self._safe_f(prev['net_profit'].iloc[0])
                            if curr_rev and prev_rev and prev_rev > 0:
                                result['revenue_growth'] = (curr_rev / prev_rev - 1) * 100
                            if curr_prof and prev_prof and prev_prof > 0:
                                result['profit_growth'] = (curr_prof / prev_prof - 1) * 100
                            self._source_stats['jq'] += 1
                    except Exception:
                        # 去年同期数据不可用，仅保留当前值
                        pass
            except Exception as e:
                logger.debug(f"JQData 利润表获取失败: {e}")

        # 优先级2: Tushare Pro
        if not result.get('revenue_growth') and self._ensure_tushare():
            try:
                ts_code = self._to_ts_code(stock_code)
                df = self._tushare_pro.income(ts_code=ts_code, limit=8)
                if df is not None and len(df) >= 2:
                    rev = pd.to_numeric(df.get('n_income', df.get('revenue', pd.Series(dtype=float))), errors='coerce')
                    if rev.notna().sum() >= 2 and rev.iloc[1] > 0:
                        result['revenue_growth'] = (rev.iloc[0] / rev.iloc[1] - 1) * 100
                    prof = pd.to_numeric(df.get('n_income', pd.Series(dtype=float)), errors='coerce')
                    if prof.notna().sum() >= 2 and prof.iloc[1] > 0:
                        result['profit_growth'] = (prof.iloc[0] / prof.iloc[1] - 1) * 100
                    self._source_stats['tushare'] += 1
            except Exception as e:
                logger.debug(f"Tushare Pro 利润表获取失败: {e}")

        # 优先级2: AKShare
        if not result.get('revenue_growth'):
            try:
                df = ak.stock_profit_sheet_by_report_em(symbol=stock_code)
                if df is not None and len(df) > 0:
                    row = df.iloc[0]
                    rg = self._safe_float(row.get('营业收入同比增长'))
                    if rg is not None:
                        result['revenue_growth'] = rg
                    pg = self._safe_float(row.get('净利润同比增长'))
                    if pg is not None:
                        result['profit_growth'] = pg
                    self._source_stats['akshare'] += 1
            except Exception as e:
                logger.debug(f"AKShare 利润表获取失败 {stock_code}: {e}")

        if not result:
            self._source_stats['failed'] += 1
            return None

        self._save_cache(cache_key, result)
        return result

    def get_stock_fundamentals(self, stock_code):
        """一次性获取全部基本面数据（估值 + 财务指标 + 收入增长）"""
        result = {}

        val = self.get_stock_valuation(stock_code)
        if val:
            result.update(val)

        ind = self.get_stock_financial_indicator(stock_code)
        if ind:
            result.update(ind)

        inc = self.get_stock_income(stock_code)
        if inc:
            result.update(inc)

        return result if result else None

    # ==================== 指数数据 ====================

    def get_index_daily(self, index_code='000300'):
        """获取指数日线"""
        cache_key = f'index_{index_code}'
        cached = self._load_cache(cache_key, expire_hours=6)
        if cached is not None:
            return cached

        try:
            df = ak.stock_zh_index_daily(symbol=f"sh{index_code}")
            if df is not None and len(df) > 0:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                self._save_cache(cache_key, df)
                return df
            return None
        except Exception as e:
            logger.error(f"获取指数 {index_code} 失败: {e}")
            return None

    def get_market_status(self):
        """获取市场状态"""
        try:
            return {
                'hs300': self.get_index_daily('000300'),
                'update_time': datetime.now()
            }
        except Exception:
            return None

    # ==================== pywencai(同花顺问财) 补充数据 ====================

    def get_pywencai_signal_stocks(self, signal_type='dual_golden'):
        """
        通过 pywencai 获取信号共振股票

        Args:
            signal_type: 信号类型
                - 'dual_golden': MACD+KDJ双金叉
                - 'macd_golden': MACD金叉
                - 'kdj_golden': KDJ金叉
                - 'limit_up': 涨停
                - 'breakout': 突破
                - 'oversold': 超跌反弹
                - 'volume_breakout': 放量突破

        Returns:
            pd.DataFrame 或 None
        """
        if not self._ensure_pywencai():
            return None

        signal_map = {
            'dual_golden': 'get_stock_dual_golden',
            'macd_golden': 'get_stock_macd_golden',
            'kdj_golden': 'get_stock_kdj_golden',
            'limit_up': 'get_stock_limit_up',
            'breakout': 'get_stock_breakout',
            'oversold': 'get_stock_oversold',
            'volume_breakout': 'get_stock_volume_breakout',
        }

        method_name = signal_map.get(signal_type)
        if method_name and hasattr(self._pywencai_fetcher, method_name):
            return getattr(self._pywencai_fetcher, method_name)()
        return None

    def get_pywencai_fund_flow(self, period='今日'):
        """
        通过 pywencai 获取个股资金流向排行

        Args:
            period: 时间周期 (今日/3日/5日/10日/20日)

        Returns:
            pd.DataFrame 或 None
        """
        if not self._ensure_pywencai():
            return None
        return self._pywencai_fetcher.get_stock_fund_flow(period)

    def get_pywencai_industry_flow(self, period='今日'):
        """
        通过 pywencai 获取行业资金流向

        Args:
            period: 时间周期

        Returns:
            pd.DataFrame 或 None
        """
        if not self._ensure_pywencai():
            return None
        return self._pywencai_fetcher.get_industry_fund_flow(period)

    def get_pywencai_north_bound(self):
        """
        获取北向资金增持股票

        Returns:
            pd.DataFrame 或 None
        """
        if not self._ensure_pywencai():
            return None
        return self._pywencai_fetcher.get_north_bound_flow()

    def get_pywencai_high_dividend(self):
        """
        获取高股息股票(股息率>4%)

        Returns:
            pd.DataFrame 或 None
        """
        if not self._ensure_pywencai():
            return None
        return self._pywencai_fetcher.get_stock_high_dividend()

    def pywencai_query(self, query_str, **kwargs):
        """
        直接执行 pywencai 自然语言查询

        Args:
            query_str: 问财语句
            **kwargs: 其他参数

        Returns:
            pd.DataFrame 或 None
        """
        if not self._ensure_pywencai():
            return None
        return self._pywencai_fetcher.query(query_str, **kwargs)

    def get_source_stats(self):
        """获取数据源使用统计"""
        return self._source_stats.copy()

    # ==================== 辅助方法 ====================

    def _to_jq_code(self, code):
        c = code.replace('sh', '').replace('sz', '')
        if c.startswith('6'):
            return f'{c}.XSHG'
        elif c.startswith(('0', '3')):
            return f'{c}.XSHE'
        return code

    def _to_ts_code(self, code):
        """转换为 Tushare 格式: 600519.SH / 000858.SZ"""
        c = code.replace('sh', '').replace('sz', '')
        if c.startswith('6'):
            return f'{c}.SH'
        elif c.startswith(('0', '3')):
            return f'{c}.SZ'
        return code

    def _safe_f(self, val):
        try:
            f = float(val)
            return f if not (np.isinf(f) or np.isnan(f)) else None
        except Exception:
            return None

    def _safe_float(self, val):
        if val is None or val == '' or str(val) == 'nan':
            return None
        try:
            f = float(val)
            return f if not (np.isinf(f) or np.isnan(f)) else None
        except Exception:
            return None

    def _find_col(self, row, keyword):
        for k, v in row.items():
            if keyword in str(k):
                return v
        return None

    # ==================== 深交所 (SZSE) 数据 ====================

    def get_szse_stock_list(self, page_no=1, page_count=50):
        """获取深交所A股列表"""
        if not self._ensure_szse():
            return []
        result = self._szse_fetcher.get_a_stock_list(page_no=page_no, page_count=page_count)
        if result and result.get('stocks'):
            self._source_stats['szse'] += 1
        return result

    def get_szse_index_quote(self):
        """获取深市指数行情"""
        if not self._ensure_szse():
            return []
        indices = self._szse_fetcher.get_index_quote()
        if indices:
            self._source_stats['szse'] += 1
        return indices

    def get_szse_announcements(self, stock_code=None, start_date=None, end_date=None,
                                page_no=1, page_size=10):
        """
        获取深交所公告
        stock_code: 股票代码，如 '000858'
        """
        if not self._ensure_szse():
            return None
        ann = self._szse_fetcher.get_announcements(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            page_no=page_no,
            page_size=page_size
        )
        if ann and ann.get('announcements'):
            self._source_stats['szse'] += 1
        return ann

    def get_szse_announcement_pdf(self, attach_path, save_dir=None):
        """下载深交所公告PDF"""
        if not self._ensure_szse():
            return None
        return self._szse_fetcher.download_announcement_pdf(attach_path, save_dir)

    # ==================== 上交所(SSE) 数据 ====================

    def get_sse_stock_list(self):
        """获取沪市A股股票列表"""
        if not self._ensure_sse():
            return None
        stocks = self._sse_fetcher.get_sh_stocks()
        if stocks:
            self._source_stats['sse'] += 1
        return stocks

    def get_sse_index(self):
        """获取沪市指数行情"""
        if not self._ensure_sse():
            return None
        indices = self._sse_fetcher.get_sh_index()
        if indices:
            self._source_stats['sse'] += 1
        return indices

    def get_sse_new_ipo(self):
        """获取新股上市信息"""
        if not self._ensure_sse():
            return None
        ipos = self._sse_fetcher.get_new_ipo()
        if ipos:
            self._source_stats['sse'] += 1
        return ipos

    def print_source_stats(self):
        """打印数据源使用统计"""
        stats = self.get_source_stats()
        total = sum(stats.values())
        if total > 0:
            logger.info("=" * 50)
            logger.info("📊 数据源使用统计:")
            for src, count in stats.items():
                src_name = {'jq': 'JQData(已禁用)',
                            'tushare': 'Tushare Pro',
                            'eastmoney': '东方财富', 'akshare': 'AKShare',
                            'pywencai': '同花顺问财',
                            'szse': '深交所(SZSE)',
                            'sse': '上交所(SSE)',
                            'failed': '失败'}.get(src, src)
                pct = count / total * 100
                logger.info(f"  {src_name}: {count}次 ({pct:.1f}%)")
            logger.info("=" * 50)


if __name__ == '__main__':
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    logging.basicConfig(level=logging.INFO)
    fetcher = DataFetcher()

    print("=" * 60)
    print("数据获取模块 v5.2 测试 — 三大主数据源 + pywencai + 交易所")
    print("=" * 60)
    print(f"  东方财富:     [OK] HTTP接口")
    print(f"  Tushare Pro:  {'[OK] 已启用' if TUSHARE_AVAILABLE else '[--] 未启用'}")
    print(f"  AKShare:      [OK] 降级兜底")
    print(f"  同花顺问财:   {'[OK] 已启用' if PYWENCAI_AVAILABLE else '[--] 未安装'}")
    print(f"  深交所SZSE:   {'[OK] 已启用' if SZSE_AVAILABLE else '[--] 未启用'}")
    print(f"  上交所SSE:    {'[OK] 已启用' if SSE_AVAILABLE else '[--] 未启用'}")
    print(f"  JQData:       [--] 已禁用（免费版数据截止2026-02-10）")
    print("=" * 60)

    # 测试日线
    print("\n[测试] 贵州茅台日线...")
    df = fetcher.get_stock_daily('600519')
    if df is not None:
        print(f"  [OK] 获取到 {len(df)} 条日线数据")
        print(f"  最新收盘价: {df['close'].iloc[-1]:.2f}")
    else:
        print("  [FAIL] 获取失败")

    # 测试估值
    print("\n[测试] 贵州茅台估值...")
    val = fetcher.get_stock_valuation('600519')
    if val:
        print(f"  PE: {val.get('pe_ttm')} | PB: {val.get('pb')}")
    else:
        print("  [FAIL] 获取失败")

    # 打印统计
    fetcher.print_source_stats()

    # 测试深交所
    if SZSE_AVAILABLE:
        print("\n[测试] 深交所A股列表...")
        szse_result = fetcher.get_szse_stock_list(page_no=1, page_count=5)
        if szse_result and szse_result.get('stocks'):
            print(f"  [OK] 总计: {szse_result['total']} 只")
            for s in szse_result['stocks'][:3]:
                print(f"  {s['code']} | {s['name']} | {s['industry']}")

        print("\n[测试] 深市指数行情...")
        indices = fetcher.get_szse_index_quote()
        if indices:
            print(f"  [OK] 获取到 {len(indices)} 个指数")
            for idx in indices[:3]:
                print(f"  {idx['name']}: {idx['close']} (涨跌:{idx['change_pct']}%)")

        print("\n[测试] 深交所公告 (平安银行)...")
        ann = fetcher.get_szse_announcements(stock_code='000001', page_size=3)
        if ann and ann.get('announcements'):
            print(f"  [OK] 总公告: {ann['total']} 条")
            for a in ann['announcements'][:3]:
                print(f"  {a.get('publishTime','')[:10]} | {a.get('title','')[:40]}")

    # 测试上交所
    if SSE_AVAILABLE:
        print("\n[测试] 上交所A股列表...")
        sse_stocks = fetcher.get_sse_stock_list()
        if sse_stocks:
            print(f"  [OK] 沪市A股: {len(sse_stocks)} 只")
            for s in sse_stocks[:3]:
                print(f"  {s.get('code','')} | {s.get('name','')}")

        print("\n[测试] 上交所新股上市...")
        ipos = fetcher.get_sse_new_ipo()
        if ipos:
            print(f"  [OK] 新股: {len(ipos)} 只")
            for ip in ipos[:3]:
                print(f"  {ip.get('name','')} | {ip.get('code','')}")

    # 测试同花顺问财
    if PYWENCAI_AVAILABLE:
        print("\n[测试] pywencai 问财: MACD金叉股票...")
        df = fetcher.get_pywencai_signal_stocks('macd_golden')
        if df is not None:
            print(f"  [OK] 获取到 {len(df)} 只")
            print(df.head(3).to_string())
        else:
            print("  [FAIL] 获取失败")

        print("\n[测试] pywencai 问财: 自定义查询...")
        df = fetcher.pywencai_query('市盈率小于20并且ROE大于15%', sort_key='总市值')
        if df is not None:
            print(f"  [OK] 获取到 {len(df)} 只")
            print(df.head(3).to_string())
        else:
            print("  [FAIL] 获取失败")

    # 打印统计
    fetcher.print_source_stats()
