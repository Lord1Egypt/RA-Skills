"""AiPO 数据源适配器。

数据源: https://aipo.myiqdii.com
港股打新数据宝藏，提供：
- 孖展数据（各券商孖展资金）
- 评级数据（各机构评级评分）⭐
- 暗盘数据（暗盘价格、成交）
- IPO 详情（保荐人、基石投资者等）
- 历史数据（IPO 表现历史）

返回纯数据字典，不做评分或判断。
"""

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import httpx

# 常量
BASE_URL = "https://aipo.myiqdii.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class BrokerMargin:
    """单个券商的孖展数据"""
    
    broker_name: str  # 券商名称
    margin_amount: float  # 孖展金额（亿港元）
    interest_rate: float  # 孖展利率（%）
    change_amount: float  # 较上次变化（亿港元）
    
    def to_dict(self) -> dict:
        return {
            "broker_name": self.broker_name,
            "margin_amount": self.margin_amount,
            "interest_rate": self.interest_rate,
            "change_amount": self.change_amount,
        }


@dataclass
class MarginSummary:
    """IPO 孖展汇总"""
    
    code: str  # 股票代码
    name: str  # 股票名称
    apply_start: str | None  # 招股开始日期
    apply_end: str | None  # 招股截止日期
    listing_date: str | None  # 上市日期
    total_margin: float  # 孖展总额（亿港元）
    raise_money: float  # 募资金额（亿港元）
    oversubscription_actual: float | None  # 实际超购倍数
    oversubscription_forecast: float | None  # 预测超购倍数
    broker_margins: list[BrokerMargin] = field(default_factory=list)  # 各券商明细
    update_time: str | None = None  # 数据更新时间
    
    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "apply_start": self.apply_start,
            "apply_end": self.apply_end,
            "listing_date": self.listing_date,
            "total_margin": self.total_margin,
            "raise_money": self.raise_money,
            "oversubscription_actual": self.oversubscription_actual,
            "oversubscription_forecast": self.oversubscription_forecast,
            "broker_margins": [b.to_dict() for b in self.broker_margins],
            "update_time": self.update_time,
        }


@dataclass
class AgencyRating:
    """机构评级"""
    agency_name: str  # 机构名称
    score: float  # 评分（0-100）
    rating: str  # 评级文字描述
    
    def to_dict(self) -> dict:
        return {
            "agency_name": self.agency_name,
            "score": self.score,
            "rating": self.rating,
        }


@dataclass 
class GreyMarketData:
    """暗盘数据"""
    code: str
    name: str
    ipo_price: float  # 发行价
    grey_price: float  # 暗盘价
    grey_change_pct: float  # 暗盘涨跌幅%
    grey_volume: float  # 暗盘成交量
    grey_turnover: float  # 暗盘成交额
    result_date: str | None  # 配售结果日期
    listing_date: str | None  # 上市日期
    
    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "ipo_price": self.ipo_price,
            "grey_price": self.grey_price,
            "grey_change_pct": self.grey_change_pct,
            "grey_volume": self.grey_volume,
            "grey_turnover": self.grey_turnover,
            "result_date": self.result_date,
            "listing_date": self.listing_date,
        }


@dataclass
class CornerstoneInvestor:
    """基石投资者"""
    name: str
    shareholding: float  # 持股数
    shareholding_pct: float  # 持股比例%
    release_date: str | None  # 解禁日期
    profile: str  # 简介
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "shareholding": self.shareholding,
            "shareholding_pct": self.shareholding_pct,
            "release_date": self.release_date,
            "profile": self.profile,
        }


# =============================================================================
# Client
# =============================================================================

class AiPOClient:
    """AiPO API 客户端"""
    
    def __init__(self):
        self._client: httpx.Client | None = None
        self._token: str | None = None
    
    def _get_client(self) -> httpx.Client:
        """获取或创建 HTTP 客户端"""
        if self._client is None:
            self._client = httpx.Client(follow_redirects=True, timeout=30)
            self._refresh_token()
        return self._client
    
    def _refresh_token(self) -> None:
        """刷新请求验证 Token"""
        client = self._client
        if client is None:
            raise RuntimeError("Client not initialized")
        
        resp = client.get(f"{BASE_URL}/margin/index", headers=HEADERS)
        resp.raise_for_status()
        
        match = re.search(r'name="__RequestVerificationToken"[^>]+value="([^"]+)"', resp.text)
        if match:
            self._token = match.group(1)
        else:
            raise ValueError("Failed to extract RequestVerificationToken from page")
    
    def _get_headers(self) -> dict:
        """获取包含 Token 的请求头"""
        if self._token is None:
            self._refresh_token()
        return {
            **HEADERS,
            "RequestVerificationToken": self._token or "",
            "Referer": f"{BASE_URL}/margin/index",
        }
    
    def _request(self, endpoint: str, params: dict | None = None) -> dict:
        """发送 API 请求"""
        client = self._get_client()
        
        for attempt in range(2):
            try:
                resp = client.get(
                    f"{BASE_URL}{endpoint}",
                    params=params,
                    headers=self._get_headers(),
                )
                resp.raise_for_status()
                data = resp.json()
                
                # 检查是否需要重新获取 token
                if isinstance(data, str) and "非法訪問" in data:
                    self._refresh_token()
                    continue
                
                return data
            except httpx.HTTPStatusError as e:
                if attempt == 0 and e.response.status_code in (401, 403):
                    self._refresh_token()
                    continue
                raise
        
        raise RuntimeError("Failed to get valid response after retries")
    
    def close(self) -> None:
        """关闭客户端"""
        if self._client:
            self._client.close()
            self._client = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# =============================================================================
# Helpers
# =============================================================================

def _parse_datetime(value: str | None) -> str | None:
    """解析日期时间字符串为 YYYY-MM-DD 格式"""
    if not value:
        return None
    try:
        # 格式: "2026-02-27T00:00:00" 或 "2026-02-27 00:00:00"
        if "T" in value:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            dt = datetime.strptime(value.split()[0], "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return value


def _parse_float(value: Any) -> float:
    """解析浮点数"""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return 0.0
    return 0.0


def _normalize_code(code: str) -> str:
    """规范化股票代码为5位格式"""
    return code.lstrip("0").zfill(5)


def _code_with_prefix(code: str) -> str:
    """添加 E 前缀"""
    code = _normalize_code(code)
    return f"E{code}"


# =============================================================================
# Margin APIs (孖展数据)
# =============================================================================

def fetch_margin_list(sector: str = "") -> list[dict]:
    """获取当前招股中 IPO 的孖展列表。
    
    Args:
        sector: 板块过滤，空字符串=全部, "主板"=主板, "创业板"=创业板
        
    Returns:
        IPO 孖展列表，包含基本信息和孖展总额
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetMarginList",
            params={"sector": sector, "pageIndex": 1, "pageSize": 100}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", "") or row.get("shortname", ""),
            "apply_start": _parse_datetime(row.get("startdate")),
            "apply_end": _parse_datetime(row.get("enddate")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "total_margin": _parse_float(row.get("marginData")),
            "margin_type": row.get("marginType"),  # "上升"/"抽飛"/null
            "interest_rate": _parse_float(row.get("interestRate")),
        })
    
    return result


def fetch_margin_detail(code: str) -> MarginSummary | None:
    """获取单只股票的孖展详情，包含各券商明细。
    
    Args:
        code: 股票代码（如 "03268" 或 "3268"）
        
    Returns:
        MarginSummary 对象，包含孖展汇总和各券商明细；未找到返回 None
    """
    code = _normalize_code(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetMarginInfo",
            params={"stockCode": f"E{code}"}
        )
    
    if data.get("result") != 1:
        return None
    
    # msg 字段包含 JSON 字符串
    msg_str = data.get("msg", "{}")
    try:
        info = json.loads(msg_str).get("data", {})
    except json.JSONDecodeError:
        return None
    
    if not info:
        return None
    
    # 解析各券商孖展数据
    broker_margins = []
    margin_info = info.get("margininfo", [])
    
    for item in margin_info:
        broker_name = item.get("ratingagency", "")
        if broker_name == "其他":
            # "其他"包含多个小券商，展开显示
            sub_list = item.get("list", [])
            for sub in sub_list:
                broker_margins.append(BrokerMargin(
                    broker_name=sub.get("ratingagency", ""),
                    margin_amount=_parse_float(sub.get("latedmargin")),
                    interest_rate=_parse_float(sub.get("rate")),
                    change_amount=_parse_float(sub.get("ChangeMargin")),
                ))
        else:
            broker_margins.append(BrokerMargin(
                broker_name=broker_name,
                margin_amount=_parse_float(item.get("latedmargin")),
                interest_rate=_parse_float(item.get("rate")),
                change_amount=_parse_float(item.get("ChangeMargin")),
            ))
    
    # 按孖展金额降序排序
    broker_margins.sort(key=lambda x: x.margin_amount, reverse=True)
    
    return MarginSummary(
        code=info.get("code", code),
        name=info.get("name", ""),
        apply_start=_parse_datetime(info.get("StartDate")),
        apply_end=_parse_datetime(info.get("EndDate")),
        listing_date=None,  # detail API 不返回上市日期
        total_margin=_parse_float(info.get("totalmargin")),
        raise_money=_parse_float(info.get("raisemoney")),
        oversubscription_actual=_parse_float(info.get("RateOver")) if info.get("RateOver") else None,
        oversubscription_forecast=_parse_float(info.get("RateForcast")) if info.get("RateForcast") else None,
        broker_margins=broker_margins,
        update_time=info.get("modifytime"),
    )


def get_margin_by_code(code: str) -> dict | None:
    """获取指定股票代码的孖展数据（便捷函数）。"""
    summary = fetch_margin_detail(code)
    if summary:
        return summary.to_dict()
    return None


# =============================================================================
# Rating APIs (评级数据) ⭐
# =============================================================================

def fetch_rating_list(sector: str = "", page_size: int = 100) -> list[dict]:
    """获取新股评级列表。
    
    Args:
        sector: 板块过滤，空字符串=全部, "主板", "创业板"
        page_size: 每页数量
        
    Returns:
        评级列表，包含综合评分
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetNewStockRatingList",
            params={"sector": sector, "pageIndex": 1, "pageSize": page_size}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    seen = set()
    
    for row in rows:
        code = row.get("symbol", "").strip()
        if code in seen:
            continue
        seen.add(code)
        result.append({
            "code": code,
            "name": row.get("shortName", "").strip(),
            "sector": row.get("sector", "").strip(),
            "rating_count": row.get("number", 0),  # 评分家数
            "avg_score": _parse_float(row.get("avgScore")),  # 综合评分 0-100
            "max_score": _parse_float(row.get("maxScore")),
            "min_score": _parse_float(row.get("minScore")),
        })
    
    return result


def fetch_rating_detail(code: str) -> list[AgencyRating]:
    """获取单只股票各机构评级详情。
    
    Args:
        code: 股票代码
        
    Returns:
        各机构评级列表
    """
    code = _code_with_prefix(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetAgencyRatingInfo",
            params={"code": code}
        )
    
    if data.get("result") != 1:
        return []
    
    # 数据在 msg JSON 中
    try:
        msg_data = json.loads(data.get("msg", "{}"))
        ratings_data = msg_data.get("data", [])
    except json.JSONDecodeError:
        return []
    
    result = []
    for item in ratings_data:
        result.append(AgencyRating(
            agency_name=item.get("ratingagency", ""),
            score=_parse_float(item.get("score")),
            rating=item.get("rating", ""),
        ))
    
    # 按评分降序
    result.sort(key=lambda x: x.score, reverse=True)
    return result


def get_rating_by_code(code: str) -> dict | None:
    """获取指定股票的评级汇总（便捷函数）。"""
    ratings = fetch_rating_detail(code)
    if not ratings:
        return None
    
    scores = [r.score for r in ratings]
    return {
        "code": _normalize_code(code),
        "rating_count": len(ratings),
        "avg_score": sum(scores) / len(scores) if scores else 0,
        "max_score": max(scores) if scores else 0,
        "min_score": min(scores) if scores else 0,
        "ratings": [r.to_dict() for r in ratings],
    }


# =============================================================================
# Grey Market APIs (暗盘数据) 🌙
# =============================================================================

def fetch_grey_list(
    sector: str = "",
    order_by: str = "resultDate",
    order_dir: str = "desc",
    page_size: int = 100
) -> list[dict]:
    """获取暗盘数据列表。
    
    Args:
        sector: 板块过滤
        order_by: 排序字段 (resultDate, grayPriceChg)
        order_dir: 排序方向 (desc, asc)
        page_size: 每页数量
        
    Returns:
        暗盘数据列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetGreyList",
            params={
                "symbol": "",
                "sector": sector,
                "pageIndex": 1,
                "pageSize": page_size,
                "orderField": order_by,
                "orderBy": order_dir,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", ""),
            "ipo_price": _parse_float(row.get("ipoPricing")),
            "grey_price": _parse_float(row.get("grayPrice")),
            "grey_change_pct": _parse_float(row.get("grayPriceChg")),
            "grey_volume": _parse_float(row.get("grayZl")),
            "grey_turnover": _parse_float(row.get("grayZe")),
            "result_date": _parse_datetime(row.get("resultDate")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "issue_number": _parse_float(row.get("issueNumber")),
            "issue_number_hk": _parse_float(row.get("issueNumber_HK")),
            "issue_number_intl": _parse_float(row.get("issueNumber_Other")),
        })
    
    return result


def fetch_allotment_results(page_size: int = 100) -> list[dict]:
    """获取配售结果列表。
    
    Returns:
        配售结果列表，包含超购倍数、中签率等
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetAllotmentResultList",
            params={"pageIndex": 1, "pageSize": page_size}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", ""),
            "sector": row.get("sector", ""),
            "industry": row.get("industry", ""),
            "apply_start": _parse_datetime(row.get("startdate")),
            "apply_end": _parse_datetime(row.get("enddate")),
            "result_date": _parse_datetime(row.get("resultDate")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "ipo_price": _parse_float(row.get("ipoPricing")),
            "price_range": f"{row.get('price_Floor', '')}-{row.get('price_Ceiling', '')}",
            "subscribed": _parse_float(row.get("subscribed")),  # 超购倍数
            "sponsors": row.get("sponsors", ""),
            "market_value": _parse_float(row.get("marketValue")),
            "pe": _parse_float(row.get("pe")),
            "margin_data": _parse_float(row.get("marginData")),
        })
    
    return result


def fetch_today_grey_market(top: int = 10) -> list[dict]:
    """获取今日暗盘股票列表（首页用）。
    
    Args:
        top: 返回数量
        
    Returns:
        今日暗盘股票列表，包含发行价、超购倍数、回拨比例、中签率等
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetDarkDiskInfo",
            params={"top": top}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", ""),
            "ipo_price": _parse_float(row.get("ipoPricing")),
            "subscribed": _parse_float(row.get("subscribed")),  # 超购倍数
            "clawback": _parse_float(row.get("clawback")),  # 回拨比例%
            "codes_rate": _parse_float(row.get("codesRate")),  # 中签率%
            "result_date": _parse_datetime(row.get("resultDate")),
        })
    
    return result


def fetch_grey_trade_details(
    code: str,
    trade_date: str,
    page_size: int = 100
) -> dict | None:
    """获取暗盘交易明细。
    
    Args:
        code: 股票代码（如 "00600"）
        trade_date: 交易日期（格式 "YYYY-MM-DD"）
        page_size: 每页数量
        
    Returns:
        交易明细，包含总成交笔数和逐笔成交记录
    """
    code = _normalize_code(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetTradeDateData",
            params={
                "code": code,
                "tradeDate": trade_date,
                "pageIndex": 1,
                "pageSize": page_size,
            }
        )
    
    if data.get("result") != 1:
        return None
    
    result_data = data.get("data", {})
    trades = result_data.get("dataList", [])
    
    return {
        "code": code,
        "trade_date": trade_date,
        "total_trades": result_data.get("totalRows", 0),
        "trades": [
            {
                "time": t.get("time", ""),  # 格式: "182900"
                "direction": t.get("buySell", ""),  # 買入/賣出/其他
                "volume": _parse_float(t.get("zl")),  # 成交量
                "amount": _parse_float(t.get("ze")),  # 成交额
                "price": _parse_float(t.get("price")),  # 成交价
            }
            for t in trades
        ],
    }


def fetch_grey_price_distribution(
    code: str,
    trade_date: str
) -> list[dict]:
    """获取暗盘分价统计。
    
    Args:
        code: 股票代码
        trade_date: 交易日期（格式 "YYYY-MM-DD"）
        
    Returns:
        分价统计列表，每个价位的成交量和占比
    """
    code = _normalize_code(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetTradeDateStatisticsData",
            params={
                "code": code,
                "tradeDate": trade_date,
                "pageIndex": 1,
                "pageSize": 100,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "price": _parse_float(row.get("price")),
            "volume": _parse_float(row.get("zl")),
            "rate": _parse_float(row.get("rate")),  # 占比 (0-1)
        })
    
    # 按价格降序排序
    result.sort(key=lambda x: x["price"], reverse=True)
    return result


def fetch_grey_price_distribution_detail(
    code: str,
    trade_date: str
) -> list[dict]:
    """获取暗盘详细分价明细（含内外盘）。
    
    Args:
        code: 股票代码
        trade_date: 交易日期（格式 "YYYY-MM-DD"）
        
    Returns:
        详细分价明细，包含内盘(卖)、外盘(买)成交量
    """
    code = _normalize_code(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetTradeDateStatisticsMore",
            params={
                "code": code,
                "tradeDate": trade_date,
                "pageIndex": 1,
                "pageSize": 100,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "price": _parse_float(row.get("price")),
            "volume": _parse_float(row.get("zl")),
            "rate": _parse_float(row.get("rate")),  # 占比 (0-1)
            "inner_volume": _parse_float(row.get("innerZl")),  # 内盘（主动卖）
            "outer_volume": _parse_float(row.get("outerZl")),  # 外盘（主动买）
        })
    
    # 按价格降序排序
    result.sort(key=lambda x: x["price"], reverse=True)
    return result


def fetch_grey_placing_detail(code: str) -> dict | None:
    """获取暗盘配售详情（甲乙组分配）。
    
    Args:
        code: 股票代码
        
    Returns:
        配售详情，包含申购人数、一手股数、各档位中签情况
    """
    code = _code_with_prefix(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetPlacingResult",
            params={"code": code}
        )
    
    if data.get("result") != 1:
        return None
    
    try:
        msg_data = json.loads(data.get("msg", "{}"))
        info = msg_data.get("data", {})
    except json.JSONDecodeError:
        return None
    
    if not info:
        return None
    
    # 解析分组配售明细
    placing_list = []
    for item in info.get("list", []):
        if len(item) >= 5:
            placing_list.append({
                "apply_shares": _parse_float(item[0]),  # 申购股数
                "applicants": _parse_float(item[1]),  # 申购人数
                "win_rate": _parse_float(item[3]) if item[3] else None,  # 中签率
                "description": item[4] if item[4] else "",  # 描述
                "min_amount": _parse_float(item[6]) if len(item) > 6 else None,  # 最低入场费
            })
    
    return {
        "code": code.replace("E", ""),
        "name": info.get("name", ""),
        "total_applicants": _parse_float(info.get("num")),  # 总申购人数
        "lot_size": _parse_float(info.get("lot")),  # 一手股数
        "min_entry_amount": _parse_float(info.get("sz")),  # 最低入场费
        "clawback_rate": info.get("rate", ""),  # 回拨比例描述，如 "50/1"
        "result_pdf": info.get("rlink", ""),  # 配售结果 PDF 链接
        "placing_list": placing_list,
    }


def fetch_market_scroll_messages(top: int = 20) -> list[dict]:
    """获取市场滚动消息（含暗盘、孖展、持股异动）。
    
    Args:
        top: 返回数量
        
    Returns:
        滚动消息列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetBottomScrollList",
            params={"top": top, "per": 10}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        msg_type = row.get("type", "")
        type_name = {
            "1": "孖展异动",
            "2": "持股异动", 
            "3": "暗盘异动",
        }.get(msg_type, "其他")
        
        result.append({
            "code": row.get("symbol", ""),
            "message": row.get("message", ""),
            "type": type_name,
            "type_code": msg_type,
            "trader_id": row.get("traderId"),
            "modify_time": _parse_datetime(row.get("modifyTime")),
        })
    
    return result


# =============================================================================
# Statistics APIs (年度统计)
# =============================================================================

def fetch_ipo_summary(year: int) -> list[dict]:
    """获取 IPO 年度汇总（含孖展总额）。
    
    Args:
        year: 年份，如 2025
        
    Returns:
        各市场 IPO 汇总列表，包含上市数量和孖展总额
        
    Note:
        此 API 返回孖展总额（loanAmount），但不含表现数据
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetIPOSummary",
            params={"year": year}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        # loanAmount 是港元，转换为亿港元
        loan_amount = _parse_float(row.get("loanAmount", 0))
        loan_amount_billion = loan_amount / 1e8 if loan_amount else 0
        
        result.append({
            "market": row.get("market", ""),  # HK=港股, N=美股, A=A股
            "list_amount": row.get("listAmount", 0),  # 上市数量
            "total_margin_billion": round(loan_amount_billion, 2),  # 孖展总额（亿港元）
            "update_time": _parse_datetime(row.get("updateTime")),
        })
    
    return result


def fetch_ipo_performance_by_year(year: int) -> list[dict]:
    """获取 IPO 年度表现统计。
    
    Args:
        year: 年份，如 2025
        
    Returns:
        各市场 IPO 表现统计，包含涨跌分布和平均涨跌幅
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetIPOSummaryByYear",
            params={"year": year}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        list_amount = row.get("listAmount", 0)
        first_up = row.get("firstZs", 0)
        first_down = row.get("firstDs", 0)
        first_flat = row.get("plateAmount", 0)
        
        # 计算首日上涨率
        up_rate = round(first_up / list_amount * 100, 1) if list_amount > 0 else 0
        
        result.append({
            "market": row.get("market", ""),  # HK=港股, N=美股, A=A股
            "list_amount": list_amount,  # 上市数量
            "first_day_up": first_up,  # 首日上涨数
            "first_day_down": first_down,  # 首日下跌数
            "first_day_flat": first_flat,  # 首日平盘/破板数
            "first_day_up_rate": up_rate,  # 首日上涨率 %
            "avg_gain_pct": round(_parse_float(row.get("avgZf")), 2),  # 平均涨幅 %
            "avg_loss_pct": round(_parse_float(row.get("avgDf")), 2),  # 平均跌幅 %
        })
    
    return result


def fetch_ipo_by_registered_office(year: int) -> list[dict]:
    """获取 IPO 按注册地统计。
    
    Args:
        year: 年份，如 2025
        
    Returns:
        按注册地分组的 IPO 数量统计
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetIPORegisteredByYear",
            params={"year": year}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        if row.get("listAmount", 0) > 0:  # 只返回有上市的
            result.append({
                "registered_office": row.get("registeredOffice", ""),
                "list_amount": row.get("listAmount", 0),
            })
    
    # 按上市数量降序
    result.sort(key=lambda x: x["list_amount"], reverse=True)
    return result


# =============================================================================
# IPO Detail APIs (IPO详情)
# =============================================================================

def fetch_ipo_brief(code: str) -> dict | None:
    """获取新股简况。
    
    Args:
        code: 股票代码
        
    Returns:
        IPO 简况，包含保荐人、发行价、招股日期等
    """
    code = _code_with_prefix(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/NewStockBrief",
            params={"code": code}
        )
    
    if data.get("result") != 1:
        return None
    
    try:
        msg_data = json.loads(data.get("msg", "{}"))
        info = msg_data.get("data", {})
    except json.JSONDecodeError:
        return None
    
    if not info:
        return None
    
    institution = info.get("institutioninfo", {})
    issuance = info.get("issuanceinfo", {})
    ipo_price = issuance.get("ipoprice", {})
    ipo_date = issuance.get("ipodate", {})
    
    return {
        "code": code.replace("E", ""),
        # 机构信息
        "principal_office": institution.get("principaloffice", ""),
        "registrars": institution.get("registrars", ""),
        "chairman": institution.get("chairman", ""),
        "secretary": institution.get("secretary", ""),
        "principal_activities": institution.get("principalactivities", ""),
        "substantial_shareholders": institution.get("substantialshareholders", ""),
        # 发行信息
        "industry": issuance.get("industry", ""),
        "sponsors": issuance.get("sponsors", ""),
        "bookrunners": issuance.get("bookrunners", ""),
        "lead_agent": issuance.get("leadagent", ""),
        "coordinator": issuance.get("coordinator", ""),
        "ipo_price_floor": _parse_float(ipo_price.get("floor")),
        "ipo_price_ceiling": _parse_float(ipo_price.get("ceiling")),
        "ipo_pricing": issuance.get("ipopricing", ""),
        "apply_start": _parse_datetime(ipo_date.get("start")),
        "apply_end": _parse_datetime(ipo_date.get("end")),
        "listing_date": _parse_datetime(issuance.get("listeddate")),
        "shares": _parse_float(issuance.get("shares")),
        "minimum_capital": _parse_float(issuance.get("minimumcapital")),
        "subscribed_count": _parse_float(issuance.get("subscribed")),
        "market_cap": issuance.get("marketcap", ""),
        "pe": _parse_float(issuance.get("pe")),
        "codes_rate": issuance.get("codesrate", ""),
    }


def fetch_cornerstone_investors(code: str) -> list[CornerstoneInvestor]:
    """获取基石投资者信息。
    
    Args:
        code: 股票代码
        
    Returns:
        基石投资者列表
    """
    code = _code_with_prefix(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetInvestorInfoByCode",
            params={"code": code}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        result.append(CornerstoneInvestor(
            name=row.get("investorName", ""),
            shareholding=_parse_float(row.get("shareholding")),
            shareholding_pct=_parse_float(row.get("shareholding_percentage")),
            release_date=_parse_datetime(row.get("releaseDate")),
            profile=row.get("profile", ""),
        ))
    
    return result


def fetch_placing_result(code: str) -> dict | None:
    """获取配售结果详情。
    
    Args:
        code: 股票代码
        
    Returns:
        配售结果，包含申购人数、中签率、配售明细
    """
    code = _code_with_prefix(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetPlacingResult",
            params={"code": code}
        )
    
    if data.get("result") != 1:
        return None
    
    try:
        msg_data = json.loads(data.get("msg", "{}"))
    except json.JSONDecodeError:
        return None
    
    if msg_data.get("result") != 1:
        return None
    
    info = msg_data.get("data", {})
    if not info:
        return None
    
    return {
        "code": code.replace("E", ""),
        "applicants": _parse_float(info.get("num")),  # 申购人数
        "codes_rate": _parse_float(info.get("codes_rate")),  # 中签率%
        "head_hammer": info.get("head_hammer", ""),  # 一手股数
        "subscribed": _parse_float(info.get("subscribed")),  # 超购倍数
        "rate_desc": info.get("rate", ""),  # "申购X手稳获Y手"
        "claw_back": _parse_float(info.get("claw_back")),  # 回拨比例%
        "placing_list": info.get("list", []),  # 分组配售明细
    }


def fetch_company_managers(code: str) -> list[dict]:
    """获取公司管理层信息。
    
    Args:
        code: 股票代码（不带E前缀）
    """
    code = _normalize_code(code)
    
    with AiPOClient() as client:
        data = client._request(
            "/Home/GetCompanyManager",
            params={"symbol": code}
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", [])
    result = []
    
    for row in rows:
        result.append({
            "name": row.get("name", ""),
            "post": row.get("post", ""),
            "age": row.get("age"),
            "start_year": row.get("startYear"),
            "resume": row.get("resume", ""),
        })
    
    return result


# =============================================================================
# Sponsor/Broker APIs (保荐人数据)
# =============================================================================

def fetch_sponsor_history(
    sponsor_name: str,
    sponsor_type: int = 0,
    page_size: int = 20
) -> list[dict]:
    """获取保荐人/承销商历史项目。
    
    Args:
        sponsor_name: 保荐人名称
        sponsor_type: 0=保荐人, 2=账簿管理人, 5=承销团
        page_size: 每页数量
        
    Returns:
        历史项目列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Home/SpoHisProjects",
            params={
                "market": "mkt_hk",
                "sponsor": sponsor_name,
                "type": sponsor_type,
                "pageIndex": 1,
                "pageSize": page_size,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", "").replace("E", ""),
            "name": row.get("shortName", ""),
            "grey_change_pct": _parse_float(row.get("grayPriceChg")),
            "first_day_change_pct": _parse_float(row.get("firstDayChg")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "current_price": _parse_float(row.get("nowprice")),
            "total_change_pct": _parse_float(row.get("zdf")),
        })
    
    return result


# =============================================================================
# Broker Ranking APIs (券商排名数据) 🏆
# =============================================================================

def fetch_bookrunner_ranking(
    start_date: str,
    end_date: str,
    sector: str = "",
    page_size: int = 50,
    page_index: int = 1,
) -> list[dict]:
    """获取账簿管理人排名。
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        sector: 板块过滤，空=全部, "主板", "创业板"
        page_size: 每页数量
        page_index: 页码
        
    Returns:
        账簿管理人排名列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Margin/GetBookrunnerJoinSort",
            params={
                "sector": sector,
                "pageIndex": page_index,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "rank": row.get("rowNo", 0),
            "name": row.get("name", ""),
            "count": row.get("number", 0),  # 参与家数
            "grey_rise_count": row.get("darkMarketRiserCompanies", 0),  # 暗盘上涨家数
            "first_day_rise_count": row.get("firstDayFallCompanies", 0),  # 首日上涨家数（字段名有误导）
        })
    
    return result


def fetch_bookrunner_details(
    name: str,
    start_date: str,
    end_date: str,
    sector: str = "",
    page_size: int = 50,
    page_index: int = 1,
) -> list[dict]:
    """获取账簿管理人参与的 IPO 详情。
    
    Args:
        name: 账簿管理人名称
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        sector: 板块过滤
        page_size: 每页数量
        page_index: 页码
        
    Returns:
        该账簿管理人参与的 IPO 列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Margin/GetBookrunnerJoinDetails",
            params={
                "sector": sector,
                "pageIndex": page_index,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
                "name": name,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", ""),
            "ipo_price": _parse_float(row.get("ipoPricing")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "first_day_change_pct": _parse_float(row.get("firstDayChg")),
            "grey_change_pct": _parse_float(row.get("grayPriceChg")),
        })
    
    return result


def fetch_broker_participation_ranking(
    start_date: str,
    end_date: str,
    sector: str = "",
    page_size: int = 50,
    page_index: int = 1,
) -> list[dict]:
    """获取券商参与排名（打新券商参与度）。
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        sector: 板块过滤，空=全部, "主板", "创业板"
        page_size: 每页数量
        page_index: 页码
        
    Returns:
        券商参与排名列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Margin/GetJoinSort",
            params={
                "sector": sector,
                "pageIndex": page_index,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "rank": row.get("rowNo", 0),
            "name": row.get("name", ""),
            "count": row.get("number", 0),  # 参与家数
            "grey_rise_count": row.get("darkMarketRiserCompanies", 0),  # 暗盘上涨家数
            "first_day_rise_count": row.get("firstDayFallCompanies", 0),  # 首日上涨家数
        })
    
    return result


def fetch_broker_participation_details(
    name: str,
    start_date: str,
    end_date: str,
    sector: str = "",
    page_size: int = 50,
    page_index: int = 1,
) -> list[dict]:
    """获取券商参与的 IPO 详情。
    
    Args:
        name: 券商名称
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        sector: 板块过滤
        page_size: 每页数量
        page_index: 页码
        
    Returns:
        该券商参与的 IPO 列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Margin/GetJoinDetails",
            params={
                "sector": sector,
                "pageIndex": page_index,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
                "name": name,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", ""),
            "ipo_price": _parse_float(row.get("ipoPricing")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "first_day_change_pct": _parse_float(row.get("firstDayChg")),
            "grey_change_pct": _parse_float(row.get("grayPriceChg")),
        })
    
    return result


def fetch_stableprice_ranking(
    start_date: str,
    end_date: str,
    sector: str = "",
    page_size: int = 50,
    page_index: int = 1,
) -> list[dict]:
    """获取稳价人排名。
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        sector: 板块过滤，空=全部, "主板", "创业板"
        page_size: 每页数量
        page_index: 页码
        
    Returns:
        稳价人排名列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Margin/GetStablepriceJoinSort",
            params={
                "sector": sector,
                "pageIndex": page_index,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "rank": row.get("rowNo", 0),
            "name": row.get("name", ""),
            "count": row.get("number", 0),  # 参与家数
            "grey_rise_count": row.get("darkMarketRiserCompanies", 0),  # 暗盘上涨家数
            "first_day_rise_count": row.get("firstDayFallCompanies", 0),  # 首日上涨家数
        })
    
    return result


def fetch_stableprice_details(
    name: str,
    start_date: str,
    end_date: str,
    sector: str = "",
    page_size: int = 50,
    page_index: int = 1,
) -> list[dict]:
    """获取稳价人参与的 IPO 详情。
    
    Args:
        name: 稳价人名称
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        sector: 板块过滤
        page_size: 每页数量
        page_index: 页码
        
    Returns:
        该稳价人参与的 IPO 列表
    """
    with AiPOClient() as client:
        data = client._request(
            "/Margin/GetStablepriceJoinDetails",
            params={
                "sector": sector,
                "pageIndex": page_index,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
                "name": name,
            }
        )
    
    if data.get("result") != 1:
        return []
    
    rows = data.get("data", {}).get("dataList", [])
    result = []
    
    for row in rows:
        result.append({
            "code": row.get("symbol", ""),
            "name": row.get("shortName", ""),
            "ipo_price": _parse_float(row.get("ipoPricing")),
            "listing_date": _parse_datetime(row.get("listedDate")),
            "first_day_change_pct": _parse_float(row.get("firstDayChg")),
            "grey_change_pct": _parse_float(row.get("grayPriceChg")),
        })
    
    return result


# =============================================================================
# Formatting Functions
# =============================================================================

def format_margin_table(summary: MarginSummary) -> str:
    """格式化孖展数据为表格字符串。"""
    lines = [
        f"=== {summary.name} ({summary.code}) 孖展数据 ===",
        f"招股期间: {summary.apply_start} - {summary.apply_end}",
        f"孖展总额: {summary.total_margin:.2f} 亿港元",
        f"募资金额: {summary.raise_money:.2f} 亿港元",
    ]
    
    if summary.oversubscription_actual:
        lines.append(f"实际超购: {summary.oversubscription_actual:.2f} 倍")
    if summary.oversubscription_forecast:
        lines.append(f"预测超购: {summary.oversubscription_forecast:.2f} 倍")
    
    if summary.update_time:
        lines.append(f"更新时间: {summary.update_time}")
    
    lines.append("")
    lines.append("各券商孖展明细:")
    lines.append("-" * 60)
    lines.append(f"{'券商名称':<15} {'孖展金额':>12} {'利率':>8} {'变化':>12}")
    lines.append("-" * 60)
    
    for b in summary.broker_margins:
        rate_str = f"{b.interest_rate:.2f}%" if b.interest_rate > 0 else "-"
        change_str = f"+{b.change_amount:.4f}" if b.change_amount > 0 else (f"{b.change_amount:.4f}" if b.change_amount < 0 else "-")
        lines.append(f"{b.broker_name:<15} {b.margin_amount:>12.4f} {rate_str:>8} {change_str:>12}")
    
    lines.append("-" * 60)
    
    return "\n".join(lines)


def format_rating_table(ratings: list[AgencyRating]) -> str:
    """格式化评级数据为表格字符串。"""
    if not ratings:
        return "暂无评级数据"
    
    lines = ["=== 机构评级 ===", "-" * 50]
    lines.append(f"{'机构名称':<20} {'评分':>10} {'评级':>15}")
    lines.append("-" * 50)
    
    for r in ratings:
        lines.append(f"{r.agency_name:<20} {r.score:>10.0f} {r.rating:>15}")
    
    lines.append("-" * 50)
    scores = [r.score for r in ratings]
    lines.append(f"综合评分: {sum(scores)/len(scores):.1f} ({len(ratings)}家)")
    
    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def main(argv=None):
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="AiPO 港股打新数据查询")
    parser.add_argument("command", choices=[
        "margin-list", "margin-detail",
        "rating-list", "rating-detail",
        "grey-list", "grey-today", "grey-trades", "grey-prices", "grey-placing",
        "allotment", "scroll",
        "ipo-brief", "cornerstone", "placing",
        "summary", "performance", "by-office",
        "bookrunner-rank", "broker-rank", "stableprice-rank",
    ], help="命令")
    parser.add_argument("code", nargs="?", help="股票代码 (detail 类命令需要)")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="json", help="输出格式")
    parser.add_argument("--sector", default="", help="板块过滤")
    parser.add_argument("--limit", type=int, default=20, help="结果数量限制")
    parser.add_argument("--date", help="交易日期 (YYYY-MM-DD)")
    parser.add_argument("--year", type=int, help="统计年份 (summary/performance/by-office 命令需要)")
    parser.add_argument("--start-date", help="开始日期 (YYYY-MM-DD, 排名命令需要)")
    parser.add_argument("--end-date", help="结束日期 (YYYY-MM-DD, 排名命令需要)")
    parser.add_argument("--name", help="机构名称 (查询详情时需要)")

    args = parser.parse_args(argv)

    if args.command == "margin-list":
        result = fetch_margin_list(sector=args.sector)
        if args.format == "json":
            print(json.dumps(result[:args.limit], ensure_ascii=False, indent=2))
        else:
            for m in result[:args.limit]:
                status = m.get("margin_type") or ""
                print(f"{m['code']} {m['name']}: {m['total_margin']:.2f}亿 {status}")
    
    elif args.command == "margin-detail":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        summary = fetch_margin_detail(args.code)
        if summary:
            if args.format == "json":
                print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
            else:
                print(format_margin_table(summary))
        else:
            print(f"未找到股票 {args.code} 的孖展数据")
    
    elif args.command == "rating-list":
        result = fetch_rating_list(sector=args.sector, page_size=args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for r in result:
                stars = "★" * int(r['avg_score'] / 20)
                print(f"{r['code']} {r['name']}: {r['avg_score']:.1f}分 {stars} ({r['rating_count']}家)")
    
    elif args.command == "rating-detail":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        ratings = fetch_rating_detail(args.code)
        if ratings:
            if args.format == "json":
                print(json.dumps([r.to_dict() for r in ratings], ensure_ascii=False, indent=2))
            else:
                print(format_rating_table(ratings))
        else:
            print(f"未找到股票 {args.code} 的评级数据")
    
    elif args.command == "grey-list":
        result = fetch_grey_list(sector=args.sector, page_size=args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for g in result:
                chg = g['grey_change_pct']
                sign = "+" if chg >= 0 else ""
                print(f"{g['code']} {g['name']}: 暗盘{sign}{chg:.1f}% (发行价:{g['ipo_price']:.2f})")
    
    elif args.command == "grey-today":
        result = fetch_today_grey_market(top=args.limit)
        if args.format == "json":
            if not result:
                print(json.dumps({"message": "今日无暗盘交易"}, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if not result:
                print("今日无暗盘交易")
            else:
                for g in result:
                    print(f"{g['code']} {g['name']}: 发行价{g['ipo_price']:.2f} 超购{g['subscribed']:.1f}倍 中签{g['codes_rate']:.2f}%")
    
    elif args.command == "grey-trades":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        if not args.date:
            print("Error: 需要 --date YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        result = fetch_grey_trade_details(args.code, args.date, page_size=args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "grey-prices":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        if not args.date:
            print("Error: 需要 --date YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        result = fetch_grey_price_distribution_detail(args.code, args.date)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"{'价格':>10} {'成交量':>12} {'占比':>10} {'内盘':>10} {'外盘':>10}")
            print("-" * 56)
            for p in result:
                rate_pct = p['rate'] * 100
                inner = p.get('inner_volume') or 0
                outer = p.get('outer_volume') or 0
                print(f"{p['price']:>10.2f} {p['volume']:>12.0f} {rate_pct:>9.2f}% {inner:>10.0f} {outer:>10.0f}")
    
    elif args.command == "grey-placing":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        result = fetch_grey_placing_detail(args.code)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "allotment":
        result = fetch_allotment_results(page_size=args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for a in result:
                print(f"{a['code']} {a['name']}: 超购{a['subscribed']:.1f}倍 上市:{a['listing_date']}")
    
    elif args.command == "scroll":
        result = fetch_market_scroll_messages(top=args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for m in result:
                print(f"[{m['type']}] {m['message']}")
    
    elif args.command == "ipo-brief":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        result = fetch_ipo_brief(args.code)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "cornerstone":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        result = fetch_cornerstone_investors(args.code)
        if args.format == "json":
            print(json.dumps([r.to_dict() for r in result], ensure_ascii=False, indent=2))
        else:
            for c in result:
                print(f"{c.name}: {c.shareholding_pct:.2f}% (解禁:{c.release_date})")
    
    elif args.command == "placing":
        if not args.code:
            print("Error: 需要股票代码", file=sys.stderr)
            sys.exit(1)
        result = fetch_placing_result(args.code)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "summary":
        year = args.year or datetime.now().year
        result = fetch_ipo_summary(year)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"=== {year}年 IPO 年度汇总 ===")
            for r in result:
                market_name = {"HK": "港股", "N": "美股", "A": "A股"}.get(r["market"], r["market"])
                print(f"{market_name}: {r['list_amount']}只 | 孖展总额: {r['total_margin_billion']:.2f}亿港元")
    
    elif args.command == "performance":
        year = args.year or datetime.now().year
        result = fetch_ipo_performance_by_year(year)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"=== {year}年 IPO 表现统计 ===")
            for r in result:
                market_name = {"HK": "港股", "N": "美股", "A": "A股"}.get(r["market"], r["market"])
                print(f"{market_name}: {r['list_amount']}只 | 首日↑{r['first_day_up']}只({r['first_day_up_rate']}%) ↓{r['first_day_down']}只")
                print(f"      平均涨幅: +{r['avg_gain_pct']}% | 平均跌幅: {r['avg_loss_pct']}%")
    
    elif args.command == "by-office":
        year = args.year or datetime.now().year
        result = fetch_ipo_by_registered_office(year)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"=== {year}年 IPO 按注册地分布 ===")
            for r in result:
                print(f"{r['registered_office']}: {r['list_amount']}只")
    
    elif args.command == "bookrunner-rank":
        start_date = args.start_date or f"{datetime.now().year}-01-01"
        end_date = args.end_date or f"{datetime.now().year}-12-31"
        if args.name:
            # 查询详情
            result = fetch_bookrunner_details(args.name, start_date, end_date, args.sector, args.limit)
        else:
            # 查询排名
            result = fetch_bookrunner_ranking(start_date, end_date, args.sector, args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"=== 账簿管理人排名 ({start_date} ~ {end_date}) ===")
            for r in result:
                if "rank" in r:
                    print(f"{r['rank']:>2}. {r['name']}: {r['count']}只 (暗盘↑{r['grey_rise_count']}只, 首日↑{r['first_day_rise_count']}只)")
                else:
                    chg = r.get('first_day_change_pct', 0)
                    sign = "+" if chg >= 0 else ""
                    print(f"{r['code']} {r['name']}: 首日{sign}{chg:.1f}% 暗盘{r.get('grey_change_pct', 0):+.1f}%")
    
    elif args.command == "broker-rank":
        start_date = args.start_date or f"{datetime.now().year}-01-01"
        end_date = args.end_date or f"{datetime.now().year}-12-31"
        if args.name:
            # 查询详情
            result = fetch_broker_participation_details(args.name, start_date, end_date, args.sector, args.limit)
        else:
            # 查询排名
            result = fetch_broker_participation_ranking(start_date, end_date, args.sector, args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"=== 券商参与排名 ({start_date} ~ {end_date}) ===")
            for r in result:
                if "rank" in r:
                    print(f"{r['rank']:>2}. {r['name']}: {r['count']}只 (暗盘↑{r['grey_rise_count']}只, 首日↑{r['first_day_rise_count']}只)")
                else:
                    chg = r.get('first_day_change_pct', 0)
                    sign = "+" if chg >= 0 else ""
                    print(f"{r['code']} {r['name']}: 首日{sign}{chg:.1f}% 暗盘{r.get('grey_change_pct', 0):+.1f}%")
    
    elif args.command == "stableprice-rank":
        start_date = args.start_date or f"{datetime.now().year}-01-01"
        end_date = args.end_date or f"{datetime.now().year}-12-31"
        if args.name:
            # 查询详情
            result = fetch_stableprice_details(args.name, start_date, end_date, args.sector, args.limit)
        else:
            # 查询排名
            result = fetch_stableprice_ranking(start_date, end_date, args.sector, args.limit)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"=== 稳价人排名 ({start_date} ~ {end_date}) ===")
            for r in result:
                if "rank" in r:
                    print(f"{r['rank']:>2}. {r['name']}: {r['count']}只 (暗盘↑{r['grey_rise_count']}只, 首日↑{r['first_day_rise_count']}只)")
                else:
                    chg = r.get('first_day_change_pct', 0)
                    sign = "+" if chg >= 0 else ""
                    print(f"{r['code']} {r['name']}: 首日{sign}{chg:.1f}% 暗盘{r.get('grey_change_pct', 0):+.1f}%")



if __name__ == "__main__":
    main()

