"""market MCP tool implementations."""

import asyncio  # noqa: F401
import json  # noqa: F401
import os  # noqa: F401
import re  # noqa: F401
import time  # noqa: F401
from typing import Optional  # noqa: F401

from .binding import bind_runtime
from .night_estimate_contract import normalize_night_response as _normalize_night_response

_RUNTIME_DEPENDENCIES = ("_get", "_post", "_require_token", "_validate_date", "_validate_fund_code")

if False:  # pragma: no cover - populated by bind() before tool registration
    _get = None
    _post = None
    _require_token = None
    _validate_date = None
    _validate_fund_code = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)


_NIGHT_MAX_CODES = 30


async def get_status() -> dict:
    """
    查询今日状态。
    返回 is_trading_day: true/false。
    """
    _require_token()
    return await _get("/api/market/status")


async def get_overview() -> dict:
    """
    获取整体概览数据，包括主要指数涨跌、热门板块、涨跌排行。
    仅适合独立查询市场；综合持仓投资分析使用 compact 策略上下文，避免重复取数。
    各数据块独立降级；单个接口失败时对应字段返回 error，不拖垮其余概览。
    """
    _require_token()
    async def safe_get(name: str, path: str, params: dict = None):
        try:
            return name, await _get(path, params=params)
        except Exception as exc:
            return name, {"error": str(exc)}

    catalog_task = asyncio.create_task(
        safe_get("instrumentCatalog", "/api/market/indices/catalog")
    )
    independent_tasks = [
        asyncio.create_task(safe_get("status", "/api/market/status")),
        asyncio.create_task(safe_get("todayRank", "/api/fund/today-rank")),
        asyncio.create_task(safe_get("sectorWind", "/api/market/sector-wind")),
        asyncio.create_task(safe_get("yesterdayRank", "/api/market/yesterday-rank")),
    ]
    tasks = [catalog_task, *independent_tasks]
    try:
        _, catalog = await catalog_task
        default_codes = catalog.get("defaultCodes", []) if isinstance(catalog, dict) else []
        default_codes = [str(code) for code in default_codes if code][:10]
        indices_coro = (
            safe_get(
                "indices",
                "/api/market/indices/latest",
                params={"codes": ",".join(default_codes)},
            )
            if default_codes
            else asyncio.sleep(0, result=("indices", {"quotes": []}))
        )
        indices_task = asyncio.create_task(indices_coro)
        tasks.append(indices_task)
        results = await asyncio.gather(*independent_tasks, indices_task)
        overview = {name: value for name, value in results}
        overview["instrumentCatalog"] = catalog
        return overview
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def get_sector_wind() -> dict:
    """
    获取市场板块风向数据，包含领涨/领跌板块和数据时间。
    适合单独回答"今天哪些板块强/弱"。
    """
    _require_token()
    return await _get("/api/market/sector-wind")


async def get_yesterday_rank() -> dict:
    """
    获取上一交易日基金涨跌榜。
    适合回答"昨天哪些基金涨得多/跌得多"，或和今日榜做对比。
    """
    _require_token()
    return await _get("/api/market/yesterday-rank")


async def get_fund_flow() -> dict:
    """
    获取资金流向数据，包括主力资金流向和板块资金流向。
    需要 PRO 会员权限。适合回答"资金在流向哪里""哪些板块受追捧"等问题。

    Returns:
        dict 包含 fundFlow、sectorFlow 和 polledAt。sectorFlow 非空时，
        byCategory 同时给出 industry/concept；必须结合 partial、
        categoriesPresent/categoriesFailed 和 sectorFlow.freshness 判断完整性。
        categoryFreshness/categoryPolledAt 仅在服务端用 last-good 补齐
        分类时存在，存在时再用它们判断各分类时点。
    """
    _require_token()
    return await _get("/api/market/fund-flow")


async def get_sector_metrics() -> dict:
    """
    获取全部已配置行业/主题 ETF 代理的服务端量化指标。

    返回实时价、MA20/MA60、20/60/120/250 交易日收益、均线偏离、
    趋势、回撤、波动率和 20 日强弱排名，并分别给出报价与历史日线
    新鲜度和 historyFreshnessBasis。优先基于场内收盘价；基金净值降级
    会明确标记且不得进入
    场内强弱排名。Agent 不应再拉取日线自行计算。ETF 仅作为板块代理，
    不会冒充其底层指数。
    """
    _require_token()
    return await _get("/api/market/sector-metrics")


async def get_index_metrics(codes: Optional[list[str]] = None) -> dict:
    """
    获取全部或指定指数的服务端量化指标，不依赖用户持仓。

    返回实时价、MA20/MA60、20/60/120/250 交易日收益、趋势、回撤、
    波动率、跨市场分组及强弱排名。`historyFreshness` 和
    `historyExpectedAsOf` 按所属市场时区、收盘时刻和交易日历，
    说明服务器当前时刻已完成的最新收盘日；`historyLagCalendarDays`
    仅作时间跨度展示。必须检查 `historyFreshnessBasis`：交易日历不可证明
    完整或市场未配置时，日线会标记 unknown 并退出排名。即使
    实时报价新鲜，陈旧历史也不会参与排名。Agent 不得再拉取原始日线
    自行计算。

    Args:
        codes: 可选指数代码列表，例如 ["399006", "000688", "KS11"]；
            留空返回全部已启用指数，最多 20 个。
    """
    _require_token()
    normalized = list(dict.fromkeys(
        str(code or "").strip().upper()
        for code in (codes or [])
        if str(code or "").strip()
    ))
    if len(normalized) > 20:
        raise ValueError("codes 最多支持 20 个指数")
    params = {"codes": ",".join(normalized)} if normalized else None
    return await _get("/api/market/index-metrics", params=params)


async def get_indices() -> list:
    """
    获取默认主要指数的便捷报价列表（上证、深证、创业板、沪深300、纳斯达克等）。
    该兼容工具只返回 quotes，若需要 cacheMeta、repairingCodes、缺失代码和轮询时间，
    请先调用 get_instrument_catalog，再使用 get_instrument_quotes。
    """
    _require_token()
    catalog = await _get("/api/market/indices/catalog")
    default_codes = catalog.get("defaultCodes", []) if isinstance(catalog, dict) else []
    code_str = ",".join(str(code) for code in default_codes if code)
    if not code_str:
        return []
    data = await _get("/api/market/indices/latest", params={"codes": code_str})
    return data.get("quotes", []) if isinstance(data, dict) else []


async def get_holder_ranking() -> dict:
    """
    获取 App 内持有人数排行榜（持有用户最多的 30 只基金）。
    返回每只基金的持有人数、最新涨跌幅，按涨幅排序。
    适合了解"大家都在买什么"的社区热度。
    """
    _require_token()
    return await _get("/api/market/holder-ranking")


async def get_night_estimate(codes: list[str], force: bool = False, view: str = "forecast") -> dict:
    """
    获取 QDII 基金最近已物化的五阶段夜盘估值帧：overnight、premarket、
    regular、after_hours 和 closed。
    返回每只基金的盘后涨跌幅、持仓穿透明细、汇率变动等数据。
    closed 是固定的最近交易时段收盘快照，其余阶段按各自 phase scope 解释；
    不得把 closed 的历史快照冒充当前实时行情。需要会员权限。
    最多 30 个代码；超过上限或传入未知 view 会直接报错，不会静默截断。
    force 仅为旧客户端兼容参数，服务端不允许请求穿透共享帧缓存或触发 Yahoo 抓取。

    item.view 是请求视图，estimateMode 是行情阶段；旧 forecast 标记只表示隔夜/假日合成预测，盘前为 false 并非拿错视图。
    与 App 同口径，逐只以 usable 判断涨幅可用性（ready 且有有限涨幅）。
    currentComplete、warming、frameRefreshing、staleCodes 是整批时效审计，不得
    据此否决已经 usable 的单只涨幅；保留 quoteAsOf/phase，说明数据时间与刷新状态。
    estimatedNav=null 是净值尚未公布的正常情况，不影响涨幅可用性。
    涨幅单位为百分点：0.0582 表示 +0.0582%，不得乘以 100；coverage 为持仓披露权重，
    不是行情拉取成功率。夜盘读取不触发预热，不要因刷新中立即重复请求同一缓存帧。
    item.fxStatus=omitted 表示本地资产涨幅仍可用、仅缺少汇率腿，不是整只基金无行情；
    此时 item 仍可 ready，但 evidenceComplete=false。QDII 持仓模型存在时，item.calibration
    统一返回 applied/reason/weight/modelVersion；夜盘只读取已验证模型，不在请求中训练。
    last_close 的 freshness=stale 是固定历史收盘快照的正常语义，此时看 complete，
    currentComplete 固定为 false。actual_session_date 是海外行情交易日，date 是
    北京时间响应日，item.navRequiredDate/lastNavDate 才是基金净值 D 日；均不可当作
    基金收益归属 G 日。

    Args:
        codes: 基金代码列表，如 ["016665", "018147"]，最多 30 个
        force: 已废弃兼容参数；true/false 都只读取共享物化帧
        view: forecast（预测口径）或 last_close（上一收盘快照口径）
    """
    _require_token()
    if len(codes) > _NIGHT_MAX_CODES:
        raise ValueError("codes 最多支持 30 只基金")
    if view not in {"forecast", "last_close"}:
        raise ValueError("view 仅支持 forecast 或 last_close")
    validated_codes = []
    seen = set()
    for code in codes:
        normalized = _validate_fund_code(code)
        if normalized not in seen:
            validated_codes.append(normalized)
            seen.add(normalized)
    if not validated_codes:
        return _normalize_night_response(
            {"status": "empty", "items": []},
            view,
        )
    code_str = ",".join(validated_codes)
    # Referencing the compatibility argument makes the ignored behavior
    # explicit while ensuring it never becomes an upstream-cache bypass again.
    _ = force
    payload = await _get(
        "/api/market/night-est",
        params={"codes": code_str, "view": view},
    )
    return _normalize_night_response(payload, view)


async def get_benchmark_history(code: str = "sh000300") -> list:
    """
    获取指数或 ETF 的历史走势数据，用于与持仓基金进行基准对比。
    默认返回沪深300（sh000300）的历史数据。

    支持两类代码：
    - 指数代码：如 "sh000300"（沪深300）、"sh000001"（上证指数）、"sz399001"（深证成指）
    - ETF 代码（纯数字）：如 "510300"（沪深300ETF）

    适合回答"我的基金跑赢大盘了吗"、"与沪深300比较"等问题。

    Args:
        code: 指数或 ETF 代码，默认 "sh000300"（沪深300）
    """
    _require_token()
    normalized = str(code or "").strip().lower()
    # 验证格式：指数代码（sh/sz开头+6位数字）或 ETF 代码（6位数字）
    if not re.fullmatch(r'(sh|sz)\d{6}|\d{6}', normalized):
        raise ValueError(f"基准代码格式无效：{code}，应为 sh000300 或 510300 格式")
    data = await _get(
        f"/api/market/benchmark-history/{normalized}",
        params={"strictFreshness": True},
    )
    return data if isinstance(data, list) else []


async def get_instrument_catalog() -> dict:
    """
    获取市场行情仪表盘的可选指数/ETF 目录。
    返回完整的标的分类列表和默认展示代码，用于了解可查询的指数/ETF 范围。
    """
    _require_token()
    return await _get("/api/market/indices/catalog")


async def get_instrument_quotes(codes: list[str]) -> dict:
    """
    批量获取指数/ETF 最近已物化的行情快照。
    适合同时查看多个指数的最近价格、涨跌幅；请求本身只读缓存，缺失或陈旧
    标的由后台修复，不会在本次请求中等待 Yahoo。

    返回时必须检查 cacheMeta.freshness、missingCodes、staleCodes 和
    repairingCodes。每项 updatedAt/quoteDate 是源行情时点，polledAt 是缓存采集
    时点，不能用 polledAt 冒充报价发生时间。

    Args:
        codes: 目录中的标准代码，如 ["000300", "000001", "399001"]，最多 20 个
    """
    _require_token()
    validated = list(dict.fromkeys(
        str(code or "").strip().upper()
        for code in (codes or [])
        if str(code or "").strip()
    ))
    if len(validated) > 20:
        raise ValueError("codes 最多支持 20 个市场标的")
    if not validated:
        return {
            "quotes": [],
            "polledAt": None,
            "cacheMeta": {
                "freshness": "empty",
                "requestedCount": 0,
                "validCount": 0,
                "returnedCount": 0,
                "readyCount": 0,
                "emptyCount": 0,
                "staleCount": 0,
                "missingCodes": [],
                "staleCodes": [],
                "repairingCodes": [],
                "sources": {},
                "freshnessCounts": {},
                "polledAtMin": None,
                "polledAtMax": None,
            },
        }
    code_str = ",".join(validated)
    return await _get("/api/market/indices/latest", params={"codes": code_str})


async def get_instrument_timeline(code: str, range: str = "1d") -> dict:
    """
    获取单个指数/ETF 的分时走势，可包含同一交易会话的最新真实报价点。
    点的 time 保留实际观察时间，不保证等间隔；latestQuote 与尾点配对。
    latestQuote.stale 或 freshness=stale 表示保留的旧帧，不能当作当前实时行情。

    Args:
        code: 目录中的标准代码，如 "000300"、"399006" 或 "KS11"
        range: 时间范围，默认 "1d"（当日）
    """
    _require_token()
    normalized = str(code or "").strip().upper()
    if not normalized:
        raise ValueError("标的代码不能为空")
    return await _get("/api/market/indices/timeline", params={"code": normalized, "range": range})


async def get_instrument_history(code: str, period: str = "1m") -> dict:
    """
    获取单个指数/ETF 的日线历史数据。服务端严格校验最近已收盘交易日；
    stale/unknown 时本工具报错，不向 Agent 返回旧日线。
    适合分析中长期走势。

    Args:
        code: 目录中的标准代码，如 "000300"、"399006" 或 "KS11"
        period: 时间周期，可选 "1m"（1个月）、"3m"（3个月）、"6m"（6个月）、"1y"（1年）
    """
    _require_token()
    normalized = str(code or "").strip().upper()
    if not normalized:
        raise ValueError("标的代码不能为空")
    if period not in ("1m", "3m", "6m", "1y"):
        raise ValueError("period 仅支持 1m、3m、6m 或 1y")
    return await _get(
        "/api/market/indices/history",
        params={
            "code": normalized,
            "period": period,
            "strictFreshness": True,
        },
    )


async def calculate_trading_dates(
    date: str,
    time_mode: str = "PRE_MARKET",
    confirm_days: int = 1,
) -> dict:
    """
    计算基金申赎的净值日、估值反映日、确认到账日（T+N 日期推算）。
    跳过周末和法定节假日，适合辅助用户规划买卖时机。
    返回的 data_date 是按 nav_date 和 confirm_days 反推的兼容字段，
    data_date_inferred=true；它不是上游已观察到的官方净值 D 日、公布日或收益归属 G 日。

    Args:
        date: 操作日期，格式 "YYYY-MM-DD"
        time_mode: 操作时间段。
            "PRE_MARKET"（默认）= 当日收盘前买入，T 日起算；
            "POST_MARKET" = 收盘后买入，T+1 日起算
        confirm_days: 确认天数（即 T+N 的 N），常见值：
            1 = T+1（货币基金、部分债基）
            2 = T+2（多数股票型/混合型基金）
            3 = T+3（部分 QDII、特殊基金）

    Returns:
        dict 包含：
            nav_date: 净值日（基金以哪天净值计算）
            data_date: 按净值日和确认天数反推的估值反映日
            confirm_date: 确认到账日（份额/资金到账日）
            data_date_inferred: 恒为 true，表示 data_date 不是上游观测值
            data_date_basis: 反推公式标识 nav_date_minus_confirm_days_offset
    """
    _require_token()
    validated_date = _validate_date(date)
    if time_mode not in ("PRE_MARKET", "POST_MARKET"):
        raise ValueError(f"time_mode 必须是 PRE_MARKET 或 POST_MARKET，收到：{time_mode}")
    if not (1 <= confirm_days <= 30):
        raise ValueError(f"confirm_days 必须在 1-30 之间，收到：{confirm_days}")
    return await _post("/api/market/calculate-dates", {
        "date": validated_date,
        "time_mode": time_mode,
        "confirm_days": confirm_days,
    })


async def get_next_trading_day(date: str) -> dict:
    """
    获取指定日期起（含当日）的下一个交易日，自动跳过周末和法定节假日。
    适合回答"元旦后第一个交易日是哪天"、"这个日期能买基金吗"等问题。

    Args:
        date: 起始日期，格式 "YYYY-MM-DD"

    Returns:
        dict 包含 date 字段，值为下一个交易日日期（"YYYY-MM-DD"）
    """
    _require_token()
    validated_date = _validate_date(date)
    return await _get("/api/market/next-trading-day", params={"date": validated_date})
