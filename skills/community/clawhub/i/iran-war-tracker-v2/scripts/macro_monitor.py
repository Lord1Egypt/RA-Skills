#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宏观数据抓取模块

整合了金十 MCP 行情数据源，用于获取布伦特原油、黄金、天然气、美元/人民币等
关键风险资产价格。保留 AlphaVantage / Stooq / Tushare 作为补充来源。

使用方式：
    python scripts/macro_monitor.py [--use-backup]
"""

from __future__ import annotations

import io
import logging
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd
import requests

# 复用同目录下的金十 MCP 客户端
from jin10_mcp import Jin10McpClient, Jin10McpError

logger = logging.getLogger(__name__)

# 金十 MCP 默认关注品种代码
JIN10_DEFAULT_CODES = ["UKOIL", "XAUUSD", "NGAS", "USDCNH"]
# 金十代码 → 内部统一命名映射
JIN10_CODE_MAP = {
    "UKOIL": "BRENT",
    "XAUUSD": "GOLD",
    "NGAS": "NATURAL_GAS",
    "USDCNH": "USD_CNY",
}

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN")

STOOQ_BACKUP_URLS = {
    "BTC": "https://stooq.com/q/l/?s=btcusd&i=d",
    "GOLD": "https://stooq.com/q/l/?s=xauusd&i=d",
    "WTI": "https://stooq.com/q/l/?s=cl.f&i=d",
    "BRENT": "https://stooq.com/q/l/?s=bz.f&i=d",
    "NATURAL_GAS": "https://stooq.com/q/l/?s=ng.f&i=d",
    "NASDAQ_FUTURES": "https://stooq.com/q/l/?s=nq.f&i=d",
}

# ---------------------------------------------------------------------------
# 原有 AlphaVantage / Stooq / Tushare 客户端（保持不变）
# ---------------------------------------------------------------------------

class AlphaVantageClient:
    """Alpha Vantage 客户端，内置免费额度限流控制。"""

    _last_request_time = 0.0
    _request_count = 0
    _minute_start = 0.0

    @classmethod
    def is_configured(cls) -> bool:
        return bool(ALPHAVANTAGE_API_KEY)

    @classmethod
    def _rate_limited_request(cls, url: str, max_retries: int = 3) -> Dict:
        if not ALPHAVANTAGE_API_KEY:
            logger.warning("ALPHAVANTAGE_API_KEY 未配置，跳过 Alpha Vantage 请求")
            return {"_error": True}

        for attempt in range(max_retries):
            try:
                current_time = time.time()
                if current_time - cls._minute_start >= 60:
                    cls._minute_start = current_time
                    cls._request_count = 0

                if cls._request_count >= 5:
                    sleep_time = max(0, 60 - (current_time - cls._minute_start) + 1)
                    logger.warning("Alpha Vantage 限流，等待 %.0f 秒", sleep_time)
                    time.sleep(sleep_time)
                    cls._minute_start = time.time()
                    cls._request_count = 0

                elapsed = current_time - cls._last_request_time
                if elapsed < 12:
                    time.sleep(12 - elapsed)

                response = requests.get(url, timeout=30)
                cls._last_request_time = time.time()
                cls._request_count += 1

                if response.status_code != 200:
                    logger.error("HTTP %s: %s", response.status_code, response.text)
                    return {}

                data = response.json()
                if "Note" in data or "Information" in data:
                    logger.warning("Alpha Vantage API limit: %s", data)
                    if attempt < max_retries - 1:
                        time.sleep(15)
                        continue
                    return {"_limited": True}

                return data
            except Exception as exc:
                logger.error("Request failed (attempt %s): %s", attempt + 1, exc)
                if attempt < max_retries - 1:
                    time.sleep(5)

        return {"_error": True}

    @classmethod
    def get_usd_cny_rate(cls) -> Optional[float]:
        url = (
            "https://www.alphavantage.co/query?"
            f"function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=CNY&apikey={ALPHAVANTAGE_API_KEY}"
        )
        data = cls._rate_limited_request(url)
        if data.get("_limited") or data.get("_error"):
            return None
        try:
            rate_data = data.get("Realtime Currency Exchange Rate", {})
            return float(rate_data.get("5. Exchange Rate", 0))
        except Exception as exc:
            logger.error("解析汇率失败: %s", exc)
            return None

    @classmethod
    def get_treasury_yield(cls, maturity: str = "10year") -> Optional[float]:
        url = (
            "https://www.alphavantage.co/query?"
            f"function=TREASURY_YIELD&interval=daily&maturity={maturity}&apikey={ALPHAVANTAGE_API_KEY}"
        )
        data = cls._rate_limited_request(url)
        if data.get("_limited") or data.get("_error"):
            return None
        try:
            data_list = data.get("data", [])
            if data_list:
                return float(data_list[0].get("value", 0))
            return None
        except Exception as exc:
            logger.error("解析美债收益率失败: %s", exc)
            return None

    @classmethod
    def get_btc_price(cls) -> Optional[float]:
        url = (
            "https://www.alphavantage.co/query?"
            f"function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={ALPHAVANTAGE_API_KEY}"
        )
        data = cls._rate_limited_request(url)
        if data.get("_limited") or data.get("_error"):
            return None
        try:
            rate_data = data.get("Realtime Currency Exchange Rate", {})
            return float(rate_data.get("5. Exchange Rate", 0))
        except Exception as exc:
            logger.error("解析 BTC 价格失败: %s", exc)
            return None

    @classmethod
    def get_commodity_price(cls, commodity: str) -> Optional[float]:
        url = (
            "https://www.alphavantage.co/query?"
            f"function={commodity.upper()}&interval=daily&apikey={ALPHAVANTAGE_API_KEY}"
        )
        data = cls._rate_limited_request(url)
        if data.get("_limited") or data.get("_error"):
            return None
        try:
            data_list = data.get("data", [])
            if data_list:
                return float(data_list[0].get("value", 0))
            return None
        except Exception as exc:
            logger.error("解析商品价格失败: %s", exc)
            return None


class StooqBackupClient:
    """Stooq 备用数据源。"""

    @staticmethod
    def get_price(symbol_key: str) -> Optional[float]:
        url = STOOQ_BACKUP_URLS.get(symbol_key)
        if not url:
            return None
        try:
            df = pd.read_csv(url)
            if not df.empty and "Close" in df.columns:
                return float(df["Close"].iloc[-1])
            return None
        except Exception as exc:
            logger.error("Stooq 获取 %s 失败: %s", symbol_key, exc)
            return None

    @classmethod
    def get_all_prices(cls) -> Dict[str, Optional[float]]:
        results: Dict[str, Optional[float]] = {}
        for key in STOOQ_BACKUP_URLS:
            results[key] = cls.get_price(key)
            time.sleep(0.5)
        return results


class TushareMacroClient:
    """Tushare 中国宏观数据客户端。"""

    _pro = None

    @classmethod
    def is_configured(cls) -> bool:
        return bool(TUSHARE_TOKEN)

    @classmethod
    def _get_pro(cls):
        if not cls.is_configured():
            logger.warning("TUSHARE_TOKEN 未配置，跳过 Tushare 请求")
            return None
        if cls._pro is None:
            try:
                import tushare as ts
                cls._pro = ts.pro_api(TUSHARE_TOKEN)
            except Exception as exc:
                logger.error("Tushare 初始化失败: %s", exc)
                return None
        return cls._pro

    @classmethod
    def get_latest_macro(cls) -> Dict[str, Dict]:
        results: Dict[str, Dict] = {}
        cpi = cls.get_latest_cpi()
        if cpi:
            results["CPI"] = cpi
        ppi = cls.get_latest_ppi()
        if ppi:
            results["PPI"] = ppi
        soci = cls.get_latest_soci()
        if soci:
            results["SOCI"] = soci
        pmi = cls.get_latest_pmi()
        if pmi:
            results["PMI"] = pmi
        return results

    @classmethod
    def get_latest_cpi(cls) -> Optional[Dict]:
        pro = cls._get_pro()
        if not pro:
            return None
        try:
            cpi = pro.cn_cpi(limit=1)
            if cpi.empty:
                return None
            return {
                "value": cpi.iloc[0].get("cpi"),
                "yoy": cpi.iloc[0].get("cpi_yoy"),
                "date": cpi.iloc[0].get("month"),
            }
        except Exception as exc:
            logger.error("获取 CPI 失败: %s", exc)
            return None

    @classmethod
    def get_latest_ppi(cls) -> Optional[Dict]:
        pro = cls._get_pro()
        if not pro:
            return None
        try:
            ppi = pro.cn_ppi(limit=1)
            if ppi.empty:
                return None
            return {
                "value": ppi.iloc[0].get("ppi"),
                "yoy": ppi.iloc[0].get("ppi_yoy"),
                "date": ppi.iloc[0].get("month"),
            }
        except Exception as exc:
            logger.error("获取 PPI 失败: %s", exc)
            return None

    @classmethod
    def get_latest_soci(cls) -> Optional[Dict]:
        pro = cls._get_pro()
        if not pro:
            return None
        try:
            soci = pro.cn_soci(limit=1)
            if soci.empty:
                return None
            return {
                "value": soci.iloc[0].get("total"),
                "date": soci.iloc[0].get("month"),
            }
        except Exception as exc:
            logger.error("获取社融失败: %s", exc)
            return None

    @classmethod
    def get_latest_pmi(cls) -> Optional[Dict]:
        pro = cls._get_pro()
        if not pro:
            return None
        try:
            pmi = pro.cn_pmi(limit=1)
            if pmi.empty:
                return None
            return {
                "value": pmi.iloc[0].get("pmi"),
                "date": pmi.iloc[0].get("month"),
            }
        except Exception as exc:
            logger.error("获取 PMI 失败: %s", exc)
            return None


# ---------------------------------------------------------------------------
# 金十 MCP 数据获取
# ---------------------------------------------------------------------------

class Jin10McpDataClient:
    """基于金十 MCP 的数据获取客户端。"""

    @staticmethod
    def fetch_quotes(codes: list[str] | None = None) -> Dict[str, Dict[str, Any]]:
        """
        获取金十报价数据。

        Returns:
            {内部命名: {name, code, time, open, close, high, low, volume, ups_price, ups_percent, source}}
        """
        target_codes = codes or JIN10_DEFAULT_CODES
        client = Jin10McpClient()
        results: Dict[str, Dict[str, Any]] = {}
        try:
            for code in target_codes:
                try:
                    payload = client.get_quote(code)
                    data = payload.get("data") or {}
                    internal_name = JIN10_CODE_MAP.get(code, code)
                    results[internal_name] = {
                        "name": data.get("name") or code,
                        "code": data.get("code") or code,
                        "time": data.get("time") or "",
                        "open": data.get("open"),
                        "close": data.get("close"),
                        "high": data.get("high"),
                        "low": data.get("low"),
                        "volume": data.get("volume"),
                        "ups_price": data.get("ups_price"),
                        "ups_percent": data.get("ups_percent"),
                        "source": "jin10_mcp",
                    }
                except Exception as exc:
                    results[JIN10_CODE_MAP.get(code, code)] = {
                        "_error": str(exc),
                        "source": "jin10_mcp",
                    }
        finally:
            client.close()
        return results

    @staticmethod
    def is_available() -> bool:
        """简单探测金十 MCP 是否可用。"""
        client = Jin10McpClient()
        try:
            client.ensure_initialized()
            return True
        except Exception:
            return False
        finally:
            client.close()


# ---------------------------------------------------------------------------
# 宏观数据聚合器（改造后）
# ---------------------------------------------------------------------------

class MacroDataMonitor:
    """宏观数据获取聚合器（整合金十 MCP）。"""

    def __init__(self):
        self.av_client = AlphaVantageClient()
        self.stooq_client = StooqBackupClient()
        self.tushare_client = TushareMacroClient()
        self.jin10_client = Jin10McpDataClient()

    # ---------- 金十 MCP 数据源 ----------

    def fetch_jin10_market_data(self) -> Dict[str, Dict[str, Any]]:
        """获取金十 MCP 市场行情。"""
        return self.jin10_client.fetch_quotes()

    # ---------- 原有 AlphaVantage / Stooq / Tushare 数据源 ----------

    def fetch_fx_data(self) -> Dict[str, Optional[float]]:
        return {"USD_CNY": self.av_client.get_usd_cny_rate()}

    def fetch_us_rates_data(self) -> Dict[str, Optional[float]]:
        return {"US_TREASURY_10Y": self.av_client.get_treasury_yield("10year")}

    def fetch_crypto_data(self) -> Dict[str, Optional[float]]:
        return {"BTC": self.av_client.get_btc_price()}

    def fetch_energy_data(self) -> Dict[str, Optional[float]]:
        return {
            "WTI": self.av_client.get_commodity_price("WTI"),
            "BRENT": self.av_client.get_commodity_price("BRENT"),
            "NATURAL_GAS": self.av_client.get_commodity_price("NATURAL_GAS"),
        }

    def fetch_alpha_vantage_market_data(self) -> Dict[str, Optional[float]]:
        data: Dict[str, Optional[float]] = {}
        data.update(self.fetch_fx_data())
        data.update(self.fetch_us_rates_data())
        data.update(self.fetch_crypto_data())
        data.update(self.fetch_energy_data())
        return data

    def fetch_backup_market_data(self) -> Dict[str, Optional[float]]:
        stooq_data = self.stooq_client.get_all_prices()
        return {
            "BTC": stooq_data.get("BTC"),
            "GOLD": stooq_data.get("GOLD"),
            "WTI": stooq_data.get("WTI"),
            "BRENT": stooq_data.get("BRENT"),
            "NATURAL_GAS": stooq_data.get("NATURAL_GAS"),
            "NASDAQ_FUTURES": stooq_data.get("NASDAQ_FUTURES"),
        }

    def fetch_china_macro_data(self) -> Dict[str, Dict]:
        return self.tushare_client.get_latest_macro()

    def fetch_china_cpi_data(self) -> Dict[str, Dict]:
        data = self.tushare_client.get_latest_cpi()
        return {"CPI": data} if data else {}

    def fetch_china_ppi_data(self) -> Dict[str, Dict]:
        data = self.tushare_client.get_latest_ppi()
        return {"PPI": data} if data else {}

    def fetch_china_soci_data(self) -> Dict[str, Dict]:
        data = self.tushare_client.get_latest_soci()
        return {"SOCI": data} if data else {}

    def fetch_china_pmi_data(self) -> Dict[str, Dict]:
        data = self.tushare_client.get_latest_pmi()
        return {"PMI": data} if data else {}

    # ---------- 统一聚合入口 ----------

    def fetch_market_data(self, use_backup: bool = False) -> Dict[str, Any]:
        """
        获取市场数据，策略：
        1. 优先使用金十 MCP 获取 Brent / Gold / Natural Gas / USD-CNY
        2. 金十缺失时回退到 AlphaVantage
        3. AlphaVantage 也缺失时（或限流）回退到 Stooq
        4. BTC / 美债 / 纳指期货仍由 AlphaVantage / Stooq 覆盖
        """
        results: Dict[str, Any] = {"sources": {}, "data": {}}

        # 1. 尝试金十 MCP
        jin10_available = False
        try:
            jin10_data = self.fetch_jin10_market_data()
            jin10_available = any(
                "_error" not in v for v in jin10_data.values()
            )
            if jin10_available:
                results["sources"]["jin10_mcp"] = "OK"
                results["data"].update(jin10_data)
            else:
                results["sources"]["jin10_mcp"] = "ERROR"
        except Exception as exc:
            logger.warning("金十 MCP 获取失败: %s", exc)
            results["sources"]["jin10_mcp"] = "ERROR"

        # 2. AlphaVantage（补充 BTC、美债、纳指期货，以及金十失败的品种）
        need_alpha = True
        if not self.av_client.is_configured():
            results["sources"]["alpha_vantage"] = "MISSING_CONFIG"
            need_alpha = False

        if need_alpha:
            alpha_data = self.fetch_alpha_vantage_market_data()
            alpha_available = any(value is not None for value in alpha_data.values())
            if alpha_available:
                results["sources"]["alpha_vantage"] = "OK"
                # 仅补充金十未覆盖或失败的品种
                for key, value in alpha_data.items():
                    if value is None:
                        continue
                    if key in results["data"] and "_error" not in results["data"][key]:
                        continue
                    results["data"][key] = {"close": value, "source": "alpha_vantage"}
            else:
                results["sources"]["alpha_vantage"] = "RATE_LIMITED"
                use_backup = True

        # 3. Stooq 备用
        if use_backup or not jin10_available:
            backup_data = self.fetch_backup_market_data()
            results["sources"]["stooq_backup"] = "OK"
            for key, value in backup_data.items():
                if value is None:
                    continue
                if key in results["data"] and "_error" not in results["data"].get(key, {}):
                    continue
                results["data"][key] = {"close": value, "source": "stooq_backup"}

        return results

    def get_all_data(self, use_backup: bool = False) -> Dict[str, Any]:
        """
        获取全部原始数据。

        返回结构：
        {
            "timestamp": "YYYY-MM-DD HH:MM:SS",
            "sources": {"jin10_mcp": "OK", "alpha_vantage": "OK", ...},
            "data": {
                "BRENT": {"name": "...", "close": ..., "ups_percent": ..., "source": "jin10_mcp"},
                "GOLD": {...},
                "NATURAL_GAS": {...},
                "USD_CNY": {...},
                "BTC": {...},
                "NASDAQ_FUTURES": {...},
                "US_TREASURY_10Y": {...},
                "CHINA_MACRO": {...}
            }
        }
        """
        results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": {},
            "data": {},
        }

        market_results = self.fetch_market_data(use_backup=use_backup)
        results["sources"].update(market_results["sources"])
        results["data"].update(market_results["data"])

        macro_data = self.fetch_china_macro_data()
        if macro_data:
            results["sources"]["tushare"] = "OK"
        elif self.tushare_client.is_configured():
            results["sources"]["tushare"] = "ERROR"
        else:
            results["sources"]["tushare"] = "MISSING_CONFIG"
        results["data"]["CHINA_MACRO"] = macro_data

        return results


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    import json

    monitor = MacroDataMonitor()
    data = monitor.get_all_data()
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
