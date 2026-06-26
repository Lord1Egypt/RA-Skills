"""数据采集层 v2 - 全面使用 Tushare 结构化数据 + NeoData 辅助"""
import json
import subprocess
import urllib.request
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from config import TUSHARE_TOKEN, TUSHARE_API_URL, TUSHARE_RATE_LIMIT, NEODATA_SCRIPT


class TushareFetcher:
    """Tushare 数据源 - 全接口版"""

    def __init__(self):
        self.token = TUSHARE_TOKEN
        self.api_url = TUSHARE_API_URL
        self._last_call = 0

    def _call(self, api_name: str, params: dict, fields: str = "") -> Optional[dict]:
        """调用 Tushare API（带限速）"""
        # 限速
        elapsed = time.time() - self._last_call
        if elapsed < TUSHARE_RATE_LIMIT:
            time.sleep(TUSHARE_RATE_LIMIT - elapsed)

        req = {"api_name": api_name, "token": self.token, "params": params, "fields": fields}
        data = json.dumps(req).encode("utf-8")
        request = urllib.request.Request(
            self.api_url, data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                self._last_call = time.time()
                if result.get("code") == 0:
                    return result.get("data")
                return None
        except Exception as e:
            print(f"  [Tushare Error] {api_name}: {e}")
            self._last_call = time.time()
            return None

    def _to_dicts(self, data: Optional[dict]) -> List[Dict]:
        """将 Tushare 返回数据转为 dict 列表"""
        if not data or not data.get("items"):
            return []
        fields = data["fields"]
        return [dict(zip(fields, row)) for row in data["items"]]

    # === 行情数据 ===
    def get_daily(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取日线行情 OHLCV"""
        data = self._call("daily", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date})
        return self._to_dicts(data)

    def get_daily_basic(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取每日指标（换手率、量比、PE等）"""
        data = self._call("daily_basic", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date},
                         "ts_code,trade_date,turnover_rate,volume_ratio,pe_ttm,pb,total_mv,circ_mv")
        return self._to_dicts(data)

    def get_index_daily(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取指数日线"""
        data = self._call("index_daily", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date})
        return self._to_dicts(data)

    # === 资金流向 ===
    def get_moneyflow(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取个股资金流向（超大/大/中/小单）"""
        data = self._call("moneyflow", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date})
        return self._to_dicts(data)

    def get_moneyflow_by_date(self, trade_date: str) -> List[Dict]:
        """获取某日全市场资金流向"""
        data = self._call("moneyflow", {"trade_date": trade_date})
        return self._to_dicts(data)

    def get_north_money(self, start_date: str, end_date: str) -> List[Dict]:
        """获取北向资金"""
        data = self._call("moneyflow_hsgt", {"start_date": start_date, "end_date": end_date})
        return self._to_dicts(data)

    def get_hsgt_top10(self, trade_date: str, market_type: str = "1") -> List[Dict]:
        """获取北向十大成交股"""
        data = self._call("hsgt_top10", {"trade_date": trade_date, "market_type": market_type})
        return self._to_dicts(data)

    # === 板块数据 ===
    def get_ths_index_list(self, index_type: str = "N") -> List[Dict]:
        """获取同花顺板块列表 (N=概念, I=行业)"""
        data = self._call("ths_index", {"exchange": "A", "type": index_type},
                         "ts_code,name,count,exchange,list_date,type")
        return self._to_dicts(data)

    def get_ths_daily(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取同花顺板块行情"""
        data = self._call("ths_daily", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date})
        return self._to_dicts(data)

    # === 涨跌停 ===
    def get_limit_list(self, trade_date: str) -> List[Dict]:
        """获取涨跌停列表"""
        data = self._call("limit_list_d", {"trade_date": trade_date},
                         "trade_date,ts_code,industry,name,close,pct_chg,fd_amount,first_time,last_time,open_times,up_stat,limit_times,limit")
        return self._to_dicts(data)

    # === 融资融券 ===
    def get_margin(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取个股融资融券"""
        data = self._call("margin_detail", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date},
                         "trade_date,ts_code,rzye,rqye,rzmre,rqmcl,rzche,rqche")
        return self._to_dicts(data)

    # === 全球指数 ===
    def get_global_index(self, ts_code: str, start_date: str = "", end_date: str = "") -> List[Dict]:
        """获取全球指数 (HSI=恒生, SPX=标普500, IXIC=纳斯达克)"""
        params = {"ts_code": ts_code}
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        data = self._call("index_global", params)
        return self._to_dicts(data)

    # === 基础数据 ===
    def get_stock_list(self) -> List[Dict]:
        """获取A股列表"""
        data = self._call("stock_basic", {"list_status": "L"},
                         "ts_code,name,industry,market,list_date")
        return self._to_dicts(data)

    def get_stk_factor(self, ts_code: str, start_date: str, end_date: str) -> List[Dict]:
        """获取复权因子"""
        data = self._call("stk_factor", {"ts_code": ts_code, "start_date": start_date, "end_date": end_date})
        return self._to_dicts(data)

    # === 龙虎榜 ===
    def get_top_list(self, trade_date: str) -> List[Dict]:
        """获取龙虎榜明细"""
        data = self._call("top_list", {"trade_date": trade_date})
        return self._to_dicts(data)

    def get_top_inst(self, trade_date: str) -> List[Dict]:
        """获取龙虎榜机构明细（哪些营业部在买卖）"""
        data = self._call("top_inst", {"trade_date": trade_date})
        return self._to_dicts(data)

    # === 大宗交易 ===
    def get_block_trade(self, trade_date: str = "", ts_code: str = "",
                        start_date: str = "", end_date: str = "") -> List[Dict]:
        """获取大宗交易"""
        params = {}
        if trade_date: params["trade_date"] = trade_date
        if ts_code: params["ts_code"] = ts_code
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        data = self._call("block_trade", params)
        return self._to_dicts(data)

    # === 港股通持股 ===
    def get_hk_hold(self, trade_date: str) -> List[Dict]:
        """获取港股通持股明细（北向持仓变动）"""
        data = self._call("hk_hold", {"trade_date": trade_date},
                         "trade_date,ts_code,name,vol,ratio,exchange")
        return self._to_dicts(data)

    # === 股东人数 ===
    def get_holder_number(self, ts_code: str) -> List[Dict]:
        """获取股东人数变化"""
        data = self._call("stk_holdernumber", {"ts_code": ts_code})
        return self._to_dicts(data)

    # === 分钟线数据 (v11新增) ===
    def get_mins(self, ts_code: str, freq: str = "5min",
                 start_date: str = "", end_date: str = "",
                 trade_date: str = "") -> List[Dict]:
        """获取分钟K线（1min/5min/15min/30min/60min）
        注意: freq必须用'5min'格式(不是'5'), 日期格式'YYYY-MM-DD HH:MM:SS'或trade_date='YYYYMMDD'
        """
        params = {"ts_code": ts_code, "freq": freq}
        if trade_date:
            params["trade_date"] = trade_date
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        data = self._call("stk_mins", params)
        return self._to_dicts(data)


class NeoDataFetcher:
    """NeoData 金融搜索 - 辅助数据源"""

    def query(self, query_text: str, data_type: str = "api") -> dict:
        try:
            result = subprocess.run(
                ["python3", str(NEODATA_SCRIPT), "--query", query_text, "--data-type", data_type],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout
            idx = output.find("{")
            if idx >= 0:
                return json.loads(output[idx:])
        except Exception as e:
            print(f"  [NeoData Error] {e}")
        return {}

    def get_sector_ranking(self) -> list:
        """获取板块涨幅排名"""
        data = self.query("今天涨幅最大的板块")
        results = []
        for item in data.get("data", {}).get("apiData", {}).get("apiRecall", []):
            content = item.get("content", "")
            if "|" in content:
                for line in content.split("\n"):
                    if "|" in line and "---" not in line:
                        cols = [c.strip() for c in line.split("|") if c.strip()]
                        if len(cols) >= 5:
                            try:
                                results.append({
                                    "name": cols[0],
                                    "change_pct": float(cols[5]) if len(cols) > 5 else 0,
                                    "leader": cols[-1] if cols[-1] else "",
                                })
                            except:
                                pass
                break
        return results
