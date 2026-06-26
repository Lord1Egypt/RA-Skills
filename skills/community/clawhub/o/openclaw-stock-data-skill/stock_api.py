"""
股票数据 API Skill for OpenClaw

该 skill 提供了访问股票数据的完整功能，包括：
- 股票列表查询
- 日K线数据
- 历史分时数据
- 财务数据
- 实时数据（竞价、收盘快照）
- 股票估值数据

使用前请确保：
1. 已在 https://data.diemeng.chat/ 注册账号
2. 已获取 API Key
3. 设置环境变量 STOCK_API_KEY 或在代码中配置
"""

import os
import requests
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta


# API 基础配置
BASE_URL = "https://data.diemeng.chat/api"
API_KEY_ENV = "STOCK_API_KEY"


def get_api_key() -> Optional[str]:
    """获取 API Key，优先从环境变量读取"""
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"未找到 API Key！请设置环境变量 {API_KEY_ENV}，"
            f"或访问 https://data.diemeng.chat/ 注册并获取 API Key"
        )
    return api_key


def _make_request(
    method: str,
    endpoint: str,
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    发送 HTTP 请求的通用方法
    
    Args:
        method: HTTP 方法 (GET, POST)
        endpoint: API 端点路径
        headers: 请求头
        params: URL 参数（GET 请求）
        json_data: JSON 数据（POST 请求）
    
    Returns:
        API 响应数据
    """
    api_key = get_api_key()
    
    url = f"{BASE_URL}{endpoint}"
    request_headers = {
        "apiKey": api_key,
        "Content-Type": "application/json"
    }
    if headers:
        request_headers.update(headers)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=request_headers, params=params, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=request_headers, json=json_data, timeout=30)
        else:
            raise ValueError(f"不支持的 HTTP 方法: {method}")
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 200:
            raise Exception(f"API 错误: {result.get('msg', '未知错误')}")
        
        return result.get("data", {})
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


# ==================== 股票列表相关 ====================

def get_stock_list(
    stock_code: Optional[str] = None,
    page: int = 0,
    page_size: int = 20000
) -> Dict[str, Any]:
    """
    获取股票列表
    
    Args:
        stock_code: 股票代码（可选，用于筛选）
        page: 页码，从0开始
        page_size: 每页数量
    
    Returns:
        包含 total 和 list 的字典
    """
    params = {
        "page": page,
        "page_size": page_size
    }
    if stock_code:
        params["stock_code"] = stock_code
    
    return _make_request("GET", "/stock/list", params=params)


# ==================== 行情数据相关 ====================

def get_daily_data(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 0,
    page_size: int = 10000
) -> Dict[str, Any]:
    """
    获取日K线数据
    
    Args:
        stock_code: 股票代码，支持单个字符串或列表，例如 "600000.SH" 或 ["600000.SH", "000001.SZ"]
        start_time: 开始日期，格式 YYYY-MM-DD
        end_time: 结束日期，格式 YYYY-MM-DD
        page: 页码，从0开始
        page_size: 每页数量
    
    Returns:
        包含 total 和 list 的字典
    """
    if not start_time or not end_time:
        # 默认查询最近30天
        end_time = datetime.now().strftime("%Y-%m-%d")
        start_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size
    }
    
    if stock_code:
        payload["stock_code"] = stock_code
    
    return _make_request("POST", "/stock/daily", json_data=payload)


def get_history_data(
    stock_code: Optional[Union[str, List[str]]] = None,
    level: str = "5min",
    start_time: str = None,
    end_time: str = None,
    page: int = 0,
    page_size: int = 10000
) -> Dict[str, Any]:
    """
    获取历史分时数据
    
    Args:
        stock_code: 股票代码，支持单个字符串或列表
        level: 时间级别，可选值: "1min", "5min", "15min", "30min", "60min"
        start_time: 开始时间，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
        end_time: 结束时间，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
        page: 页码，从0开始
        page_size: 每页数量
    
    Returns:
        包含 total 和 list 的字典
    """
    if not start_time or not end_time:
        # 默认查询今天
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.now().strftime("%Y-%m-%d 00:00:00")
    
    payload = {
        "level": level,
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size
    }
    
    if stock_code:
        payload["stock_code"] = stock_code
    
    return _make_request("POST", "/stock/history", json_data=payload)


# ==================== 财务数据相关 ====================

def get_finance_data(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 0,
    page_size: int = 10000
) -> Dict[str, Any]:
    """
    获取每日财务数据
    
    Args:
        stock_code: 股票代码，支持单个字符串或列表
        start_time: 开始日期，格式 YYYY-MM-DD
        end_time: 结束日期，格式 YYYY-MM-DD
        page: 页码，从0开始
        page_size: 每页数量
    
    Returns:
        包含 total 和 list 的字典，包含 PE、PB、PS、市值等财务指标
    """
    if not start_time or not end_time:
        # 默认查询最近30天
        end_time = datetime.now().strftime("%Y-%m-%d")
        start_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size
    }
    
    if stock_code:
        payload["stock_code"] = stock_code
    
    return _make_request("POST", "/stock/finance", json_data=payload)


def get_stock_valuation(
    sort_by: str = "pe_ttm",
    sort_order: str = "asc",
    industry: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    获取股票估值列表
    
    Args:
        sort_by: 排序字段，可选值: "pe_ttm", "pe_percentile", "dividend_yield_ttm", "industry_pe_rank"
        sort_order: 排序方向，可选值: "asc", "desc"
        industry: 行业筛选（可选）
        limit: 返回数量限制
        offset: 偏移量
    
    Returns:
        股票估值数据列表
    """
    params = {
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "offset": offset
    }
    
    if industry:
        params["industry"] = industry
    
    return _make_request("GET", "/stock/valuation/list", params=params)


# ==================== 实时数据相关 ====================

def get_call_auction(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 0,
    page_size: int = 10000
) -> Dict[str, Any]:
    """
    获取集合竞价数据
    
    Args:
        stock_code: 股票代码，支持单个字符串或列表
        start_time: 开始时间，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
        end_time: 结束时间，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
        page: 页码，从0开始
        page_size: 每页数量
    
    Returns:
        包含 total 和 list 的字典
    """
    if not start_time or not end_time:
        # 默认查询今天
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.now().strftime("%Y-%m-%d 00:00:00")
    
    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size
    }
    
    if stock_code:
        payload["stock_code"] = stock_code
    
    return _make_request("POST", "/stock/call_auction", json_data=payload)


def get_closing_snapshot(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = None,
    end_time: str = None,
    page: int = 0,
    page_size: int = 10000
) -> Dict[str, Any]:
    """
    获取收盘快照数据
    
    Args:
        stock_code: 股票代码，支持单个字符串或列表
        start_time: 开始时间，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
        end_time: 结束时间，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
        page: 页码，从0开始
        page_size: 每页数量
    
    Returns:
        包含 total 和 list 的字典
    """
    if not start_time or not end_time:
        # 默认查询今天
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.now().strftime("%Y-%m-%d 00:00:00")
    
    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size
    }
    
    if stock_code:
        payload["stock_code"] = stock_code
    
    return _make_request("POST", "/stock/closing_snapshot", json_data=payload)


# ==================== 基础数据相关 ====================

def get_trade_calendar(
    start_time: str,
    end_time: str
) -> List[Dict[str, Any]]:
    """
    获取交易日历
    
    Args:
        start_time: 开始日期，格式 YYYY-MM-DD
        end_time: 结束日期，格式 YYYY-MM-DD
    
    Returns:
        交易日历列表，包含 date 和 is_open 字段
    """
    params = {
        "start_time": start_time,
        "end_time": end_time
    }
    
    return _make_request("GET", "/basic/calendar", params=params)


# ==================== 辅助函数 ====================

def search_stock_by_name(name: str) -> List[Dict[str, Any]]:
    """
    根据股票名称搜索股票
    
    Args:
        name: 股票名称（支持模糊匹配）
    
    Returns:
        匹配的股票列表
    """
    result = get_stock_list(page_size=20000)
    stocks = result.get("list", [])
    
    # 简单模糊匹配
    matched = [
        stock for stock in stocks
        if name.lower() in stock.get("name", "").lower()
    ]
    
    return matched


def get_stock_info(stock_code: str) -> Optional[Dict[str, Any]]:
    """
    获取单个股票的详细信息
    
    Args:
        stock_code: 股票代码，例如 "600000.SH"
    
    Returns:
        股票信息字典，如果未找到返回 None
    """
    result = get_stock_list(stock_code=stock_code, page_size=1)
    stocks = result.get("list", [])
    
    if stocks:
        return stocks[0]
    return None


# ==================== 复权与复权因子相关 ====================

def get_daily_adj_data(
    stock_code: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    algo: str = "recursive",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取复权日K线数据（前复权）。

    注意：后端要求必须至少提供 `stock_code` 或 (`start_time` 与 `end_time`) 之一。
    """
    payload: Dict[str, Any] = {
        "algo": algo,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code
    if start_time:
        payload["start_time"] = start_time
    if end_time:
        payload["end_time"] = end_time

    return _make_request("POST", "/stock/daily_adj", json_data=payload)


def get_adj_factor(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取自定义复权因子（递归算法因子），用于本地自行复权处理。

    Args:
        stock_code: 单个股票代码或股票代码列表
        start_time: 开始日期 YYYY-MM-DD（必填）
        end_time: 结束日期 YYYY-MM-DD（必填）
        page: 页码
        page_size: 每页数量，最大 10000
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/stock/adj_factor", json_data=payload)


# ==================== 条件搜索相关 ====================

def search_stock_by_condition(
    query: str,
    stock_code: Optional[str] = None,
    date: Optional[str] = None,
    page: int = 0,
    page_size: int = 10,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> Dict[str, Any]:
    """
    按条件搜索股票（支持中文/英文条件，如“pe_ttm < 20 且 turnover_rate > 3%”）。

    Args:
        query: 条件表达式，支持中文描述与 AND/OR 组合
        stock_code: 可选，限制在某一只股票内筛选
        date: 可选，YYYY-MM-DD 或 MM-DD；为空时为最新快照
        page: 页码，从 0 开始
        page_size: 每页数量，默认 10，最大 1000
        sort_by: 排序字段
        sort_order: 排序方向 asc/desc
    """
    payload: Dict[str, Any] = {
        "query": query,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code
    if date:
        payload["date"] = date
    if sort_by:
        payload["sort_by"] = sort_by
    if sort_order:
        payload["sort_order"] = sort_order

    return _make_request("POST", "/stock/search", json_data=payload)


def get_stock_search_fields() -> Dict[str, Any]:
    """
    获取条件搜索支持的字段列表和示例。
    """
    return _make_request("GET", "/stock/search/fields")


# ==================== 基础快照与停牌信息 ====================

def get_basic_snapshot(
    stock_code: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取最新集合竞价快照（基于 `stock_call_auction` 聚合）。

    Args:
        stock_code: 股票代码（可选）
        page: 页码
        page_size: 每页数量
    """
    params: Dict[str, Any] = {
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        params["stock_code"] = stock_code

    return _make_request("GET", "/basic/snapshot", params=params)


def get_stock_suspension(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取股票停牌信息。
    """
    params: Dict[str, Any] = {
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        params["stock_code"] = stock_code
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time

    return _make_request("GET", "/stock/suspension", params=params)


# ==================== 股票快照历史 ====================

def get_stock_snapshot_daily(
    stock_code: Optional[Union[str, List[str]]] = None,
    date: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取股票日度快照数据（`stock_snapshot_daily`）。

    Args:
        stock_code: 股票代码（可选，单个或列表）
        date: 交易日期 YYYY-MM-DD（可选，为空时后端使用最新日期）
        page: 页码
        page_size: 每页数量，最大 10000
    """
    payload: Dict[str, Any] = {
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code
    if date:
        payload["date"] = date

    return _make_request("POST", "/stock/snapshot_daily", json_data=payload)


def get_stock_snapshot_push_history(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = "",
    end_time: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取推送通道中的快照历史（Redis / Kafka 推送记录）。

    Args:
        stock_code: 股票代码（可选，单个或列表）
        start_time: 开始时间 YYYY-MM-DD HH:MM:SS
        end_time: 结束时间 YYYY-MM-DD HH:MM:SS（可选）
        page: 页码
        page_size: 每页数量
    """
    if not start_time:
        raise ValueError("start_time 为必填参数")

    payload: Dict[str, Any] = {
        "start_time": start_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code
    if end_time:
        payload["end_time"] = end_time

    return _make_request("POST", "/stock/snapshot_push_history", json_data=payload)


# ==================== 可转债相关 ====================

def get_bond_daily(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取可转债日线数据。
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/bond/daily", json_data=payload)


def get_bond_history(
    stock_code: Optional[Union[str, List[str]]] = None,
    level: str = "5min",
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取可转债分钟级历史数据。
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "level": level,
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/bond/history", json_data=payload)


def get_bond_indicator_daily(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取可转债日度指标数据（纯债价值、转股溢价等）。

    注意：至少需要提供 `stock_code` 或 `start_date` / `end_date` 之一。
    """
    if not stock_code and not start_date and not end_date:
        raise ValueError("stock_code 与 start_date/end_date 至少需要提供一个")

    payload: Dict[str, Any] = {
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code
    if start_date:
        payload["start_date"] = start_date
    if end_date:
        payload["end_date"] = end_date

    return _make_request("POST", "/bond/indicator_daily", json_data=payload)


def get_bond_closing_snapshot(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取可转债收盘快照数据。
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/bond/closing_snapshot", json_data=payload)


def get_bond_list(
    bond_code: Optional[Union[str, List[str]]] = None,
    stock_code: Optional[Union[str, List[str]]] = None,
    exchange: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取可转债基础信息列表。
    """
    payload: Dict[str, Any] = {
        "page": page,
        "page_size": page_size,
    }
    if bond_code:
        payload["bond_code"] = bond_code
    if stock_code:
        payload["stock_code"] = stock_code
    if exchange:
        payload["exchange"] = exchange

    return _make_request("POST", "/bond/list", json_data=payload)


# ==================== ETF 相关 ====================

def get_etf_daily(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取 ETF 日线数据。
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/etf/daily", json_data=payload)


def get_etf_history(
    stock_code: Optional[Union[str, List[str]]] = None,
    level: str = "5min",
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取 ETF 分钟级历史数据。
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "level": level,
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/etf/history", json_data=payload)


# ==================== 指数相关 ====================

def get_index_history(
    index_code: Optional[Union[str, List[str]]] = None,
    level: str = "1min",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取指数分钟级历史数据。

    注意：后端要求 `index_code` 与 `start_time/end_time` 至少提供一类。
    """
    payload: Dict[str, Any] = {
        "level": level,
        "page": page,
        "page_size": page_size,
    }
    if index_code:
        payload["index_code"] = index_code
    if start_time:
        payload["start_time"] = start_time
    if end_time:
        payload["end_time"] = end_time

    return _make_request("POST", "/index/history", json_data=payload)


# ==================== 港股相关 ====================

def get_hk_stock_list() -> List[Dict[str, Any]]:
    """
    获取港股基础信息列表。
    """
    return _make_request("GET", "/stock/hk/list")


def get_hk_finance_data(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_date: str = "",
    end_date: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取港股财务报表及财务指标数据。
    """
    if not start_date or not end_date:
        raise ValueError("start_date 与 end_date 为必填参数")

    payload: Dict[str, Any] = {
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/stock/hk/finance", json_data=payload)


def get_hk_stock_valuation() -> Dict[str, Any]:
    """
    获取港股综合估值信息（含行业分布与 10 年成长指标）。
    """
    return _make_request("GET", "/stock/hk/valuation")


def get_hk_closing_snapshot(
    stock_code: Optional[Union[str, List[str]]] = None,
    start_time: str = "",
    end_time: str = "",
    page: int = 0,
    page_size: int = 10000,
) -> Dict[str, Any]:
    """
    获取港股收盘快照数据。
    """
    if not start_time or not end_time:
        raise ValueError("start_time 与 end_time 为必填参数")

    payload: Dict[str, Any] = {
        "start_time": start_time,
        "end_time": end_time,
        "page": page,
        "page_size": page_size,
    }
    if stock_code:
        payload["stock_code"] = stock_code

    return _make_request("POST", "/stock/hk/closing_snapshot", json_data=payload)


def get_hk_connect(
    type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    获取最新一日港股互联互通成分（沪深港通标的）。

    Args:
        type: 可选，HK_SZ / SZ_HK / HK_SH / SH_HK
    """
    params: Dict[str, Any] = {}
    if type:
        params["type"] = type

    return _make_request("GET", "/stock/hk/connect", params=params)


# ==================== A 股综合估值（完整版） ====================

def get_stock_valuation_full() -> Dict[str, Any]:
    """
    获取 A 股完整综合估值列表（含行业分位与 10 年成长指标）。

    对应后端 `GET /api/stock/valuation` 接口。
    """
    return _make_request("GET", "/stock/valuation")