"""fund MCP tool implementations."""

from typing import Optional  # noqa: F401
from .binding import bind_runtime
from .fund_estimate_helpers import (
    estimate_evidence_summary as _estimate_evidence_summary,
    estimate_frame_available as _estimate_frame_available,
    sanitize_estimate_frame as _sanitize_estimate_frame,
    sanitize_source_preview_payload as _sanitize_source_preview_payload,
    validate_public_data_source_mode as _validate_public_data_source_mode,
)
from .fund_history_helpers import (
    get_strict_item_history as _get_strict_item_history,
    search_fund as _search_fund,
)
from .fund_rank_helpers import get_batch_period_ranks as _get_batch_period_ranks
from ..quant_validation import (
    validate_quant_current_frame as _validate_quant_current_frame,
    validate_quant_view as _validate_quant_view,
)

_RUNTIME_DEPENDENCIES = ("_fetch_estimates", "_get", "_post", "_require_token", "_validate_fund_code")
if False:  # pragma: no cover - populated by bind() before tool registration
    _fetch_estimates = None
    _get = None
    _post = None
    _require_token = None
    _validate_fund_code = None
def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)

async def search_item(query: str) -> list:
    """
    按编号或名称搜索项目，返回最多 20 条结果。
    仅在不知道基金代码时使用；若已知代码（如用户直接提供），可跳过此步骤直接查询。

    Args:
        query: 搜索关键词，如 "000001"、"华夏"
    """
    _require_token()
    return await _search_fund(_get, query)


async def get_item_detail(code: str) -> dict:
    """
    获取单只基金的基础详情与持仓信息。
    本工具不触发量化指标或历史统计计算；量化数据请按需调用
    get_fund_quant_metrics，当前净值/涨跌请调用 get_item_estimate。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/{validated_code}")


async def get_item_estimate(
    codes: list[str],
    default_data_source_mode: str = "source_a",
    data_source_mode_by_code: Optional[dict] = None,
) -> dict:
    """
    批量获取项目今日实时估算净值（最多 50 个）。
    适合查询"现在涨了多少""今天净值多少"等日常行情问题，不会附带量化计算。
    同一时刻的重叠请求会合并为一次后端读取，但不会跨调用缓存完整估值帧，
    避免后台基金调优后继续返回旧板块、确认天数或估算路由。
    支持新版后端多行情源：default_data_source_mode / data_source_mode_by_code。
    返回 requestedCodes、missingCodes、invalidCodes、unavailableCodes、timeoutCodes、
    staleCodes、decisionUnavailableCodes、partialCodes、complete 和 evidenceComplete。
    complete 只表示每个代码都有可用数值；evidenceComplete 还要求没有代理、
    汇率省略或输入不完整。每项 estimateEvidence 可给出 coverage、proxyCoverage、
    fxStatus/fxDegraded，并在 QDII 持仓模型存在时给出统一的 calibration
    （applied/reason/weight/modelVersion）。汇率 omitted 仍可保留本地资产涨幅和
    可用净值，但证据为 partial；部分失败、过期或决策不可用帧不会伪装成完整结果。
    来源 A/B 对部分基金没有覆盖时，只影响对应基金或来源；必须按上述集合逐项判断，
    不能把单来源缺失解释成整批基金请求失败。
    显式选择 A/B 但该源无覆盖时，后端会继续回退花花来源。所有可信主路径和
    同日快照均失败时，后端可能使用带审计标记的市场因子、QDII 市场代理或板块
    关联兜底。普通回答只给估值时间、类型、来源、涨幅、净值和官方日期，不主动
    枚举 partial、FX 或覆盖率；用户明确要求诊断时才展开审计证据，并且不能把
    代理估算描述成持仓股票完整覆盖。
    capabilities.trade=false 表示该场内标的仅支持查看，不得创建持仓、交易或定投。
    当前响应应优先读取 frameSemantics：exchange_close_price 表示已验证交易日的
    场内收盘价。静态 estimateSemantics=estimated_nav_not_trade_price 只描述该标的
    仍可能提供参考净值估算，不能用它覆盖当前收盘帧，也不能把收盘价称为官方净值。

    日期字段中，display_date 是估算展示/T 帧日期，target_nav_date 是当前帧对应的
    目标净值 D 日，last_nav_date 是最新官方净值 D 日；可靠收益 G 日只能读取
    get_records().returnAttributionDate，为 null 时不得用 D 日代替。

    Args:
        codes: 项目编号列表，如 ["000001", "110022"]，最多 50 个
        default_data_source_mode: 默认行情源模式：source_a/source_b/huahua。
        data_source_mode_by_code: 可选，每只基金单独指定行情源模式。
    """
    _require_token()
    if len(codes) > 50:
        raise ValueError("codes 最多支持 50 只基金")
    validated_default_mode = _validate_public_data_source_mode(
        default_data_source_mode,
        "default_data_source_mode",
    )
    # 验证并去重基金代码
    validated_codes = []
    invalid_codes = []
    seen = set()
    for code in codes:
        try:
            normalized = _validate_fund_code(code)
            if normalized not in seen:
                validated_codes.append(normalized)
                seen.add(normalized)
        except ValueError:
            invalid_codes.append(str(code or "").strip())
    if data_source_mode_by_code is not None and not isinstance(
        data_source_mode_by_code,
        dict,
    ):
        raise ValueError("data_source_mode_by_code 必须是对象")
    validated_mode_by_code = {
        _validate_fund_code(code): _validate_public_data_source_mode(
            mode,
            f"data_source_mode_by_code[{code}]",
        )
        for code, mode in (data_source_mode_by_code or {}).items()
    }
    unexpected_mode_codes = set(validated_mode_by_code) - set(validated_codes)
    if unexpected_mode_codes:
        raise ValueError("data_source_mode_by_code 只能包含本次请求的有效基金代码")
    if not validated_codes:
        return {
            "data": [],
            "requestedCodes": [],
            "missingCodes": [],
            "invalidCodes": invalid_codes,
            "unavailableCodes": [],
            "timeoutCodes": [],
            "staleCodes": [],
            "decisionUnavailableCodes": [],
            "partialCodes": [],
            "fxDegradedCodes": [],
            "evidenceComplete": not invalid_codes,
            "complete": not invalid_codes,
        }
    estimate_map = await _fetch_estimates(
        validated_codes,
        default_data_source_mode=validated_default_mode,
        data_source_mode_by_code=validated_mode_by_code,
    )
    normalized_map = {}
    for code, value in estimate_map.items():
        item = _sanitize_estimate_frame(value)
        if isinstance(item, dict):
            item = {
                **item,
                "estimateEvidence": _estimate_evidence_summary(item),
            }
        normalized_map[str(code)] = item
    missing_codes = [code for code in validated_codes if code not in normalized_map]
    unavailable_codes = [
        code
        for code in validated_codes
        if code in normalized_map and not _estimate_frame_available(normalized_map[code])
    ]
    timeout_codes = [
        code
        for code in unavailable_codes
        if str(normalized_map[code].get("source") or "").strip().lower() == "timeout"
    ]
    stale_codes = [
        code
        for code in unavailable_codes
        if normalized_map[code].get("stale") is True
        or normalized_map[code].get("estimateStale") is True
        or str(
            normalized_map[code].get("freshness")
            or normalized_map[code].get("estimateFreshness")
            or ""
        ).strip().lower() == "stale"
    ]
    decision_unavailable_codes = [
        code
        for code in unavailable_codes
        if isinstance(normalized_map[code].get("estimateDecision"), dict)
        and str(
            normalized_map[code]["estimateDecision"].get("status") or ""
        ).strip().lower() == "unavailable"
    ]
    partial_codes = [
        code
        for code in validated_codes
        if code in normalized_map
        and isinstance(normalized_map[code], dict)
        and isinstance(normalized_map[code].get("estimateEvidence"), dict)
        and normalized_map[code]["estimateEvidence"].get("partial") is True
    ]
    fx_degraded_codes = [
        code
        for code in validated_codes
        if code in normalized_map
        and isinstance(normalized_map[code], dict)
        and isinstance(normalized_map[code].get("estimateEvidence"), dict)
        and normalized_map[code]["estimateEvidence"].get("fxDegraded") is True
    ]
    complete = not missing_codes and not invalid_codes and not unavailable_codes
    return {
        "data": [
            normalized_map[code]
            for code in validated_codes
            if code in normalized_map
        ],
        "requestedCodes": validated_codes,
        "missingCodes": missing_codes,
        "invalidCodes": invalid_codes,
        "unavailableCodes": unavailable_codes,
        "timeoutCodes": timeout_codes,
        "staleCodes": stale_codes,
        "decisionUnavailableCodes": decision_unavailable_codes,
        "partialCodes": partial_codes,
        "fxDegradedCodes": fx_degraded_codes,
        "evidenceComplete": complete and not partial_codes,
        "complete": complete,
    }


async def get_fund_source_previews(code: str) -> dict:
    """
    获取单只基金在多个行情源下的来源预览。
    适合用户询问"不同数据源现在差多少"或需要选择基金级 dataSourceMode 时调用。
    净值公布后，只有同日收盘前归档估值才会出现在 last_estimate_snap；
    当前官方净值不会被改名为 A/B 的历史估值。数据来源 A/B 缺失表示
    单来源证据不足，不代表整个请求失败。
    花花项主路径均未命中时可能使用板块、市场因子或 QDII 市场代理作低置信
    partial 兜底；该结果不会再回流进聚合池。`last_estimate_snap` 会保留同日的
    market_factor_proxy_estimate / qdii_market_proxy_estimate 历史证据。

    Args:
        code: 项目编号，如 "000001"

    Returns:
        dict 包含 code 和 data。data 是 source_a/source_b/huahua 的部分映射；
        普通基金可能缺少未覆盖的 A/B，官方净值帧可通过 last_estimate_snap
        保留最后估值证据。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return _sanitize_source_preview_payload(
        await _get(f"/api/estimate/source-previews/{validated_code}")
    )


async def get_daily_rank() -> dict:
    """
    获取已形成今日估值或官方净值快照的活跃基金涨跌榜。
    返回当前活跃快照池中的涨幅、跌幅和板块概览，不代表全市场全量基金。
    """
    _require_token()
    return await _get("/api/fund/today-rank")


async def get_item_history(code: str) -> list:
    """
    获取项目历史净值数据（用于查看过去走势）。服务端会严格校验最新应有
    官方净值日；刷新失败且只能取得过期历史时，本工具报错而不返回旧列表。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    return await _get_strict_item_history(_get, _validate_fund_code, code)


async def get_item_dividends(code: str) -> list:
    """
    获取项目历史派息记录。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    data = await _get(f"/api/fund/dividends/{validated_code}")
    return data if isinstance(data, list) else []


async def get_fund_timeline(code: str, source_mode: str = "source_a") -> list:
    """
    获取指定项目今日分时估值走势（每隔几分钟一个数据点，盘中更新）。
    仅用于观察曲线；当前量化结论必须另外调用 get_item_estimate 并检查
    complete/staleCodes/evidenceComplete，不能把曲线尾点当作新鲜行情证明。
    非交易日或盘前返回空列表。

    Args:
        code: 项目编号，如 "000001"
        source_mode: 行情源模式：source_a/source_b/huahua。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    validated_source_mode = _validate_public_data_source_mode(
        source_mode,
        "source_mode",
    )
    data = await _get(
        f"/api/fund/today-timeline/{validated_code}",
        params={"sourceMode": validated_source_mode},
    )
    return data if isinstance(data, list) else []


async def get_fund_fees(code: str) -> dict:
    """
    获取项目交易规则，包括确认天数、申购状态、QDII/限大额日累计限购金额等。
    在制定买卖决策时可参考确认周期、限购状态和手续费成本。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/fees/{validated_code}")


async def get_batch_fund_fees(codes: list[str]) -> dict:
    """
    批量获取基金费率、申购状态、限购规则。最多 50 个代码。
    适合配合 get_purchase_limit_watchlist 一次性检查限购观察列表。
    超过 50 个会直接报错，不会静默截断。

    Args:
        codes: 6 位基金代码列表。
    """
    _require_token()
    if len(codes) > 50:
        raise ValueError("codes 最多支持 50 只基金")
    validated_codes = []
    seen = set()
    for code in codes:
        normalized = _validate_fund_code(code)
        if normalized not in seen:
            validated_codes.append(normalized)
            seen.add(normalized)
    if not validated_codes:
        return {
            "data": {},
            "truncated": False,
            "limit": 50,
            "requestedCodes": [],
            "missingCodes": [],
            "complete": True,
        }
    payload = await _post("/api/fund/fees/batch", {"codes": validated_codes})
    result = dict(payload) if isinstance(payload, dict) else {}
    data = result.get("data")
    data = data if isinstance(data, dict) else {}
    missing_codes = [code for code in validated_codes if code not in data]
    result.update({
        "data": data,
        "requestedCodes": validated_codes,
        "missingCodes": missing_codes,
        "complete": not missing_codes,
    })
    return result


async def get_fund_period_rank(code: str) -> dict:
    """
    获取项目近期业绩排名，包含近 1 个月、3 个月、6 个月、1 年的收益率及同类排名百分位。
    适合评估基金经理和产品的中长期表现。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/period-rank/{validated_code}")


async def get_fund_profile(code: str) -> dict:
    """
    获取基金画像，包含基本信息、费率、业绩排名、持仓、行业分布、分红、风险指标等综合数据。
    比 get_item_detail 更聚焦于基金本身的静态属性，适合深度分析和对比。

    Args:
        code: 项目编号，如 "000001"
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    return await _get(f"/api/fund/profile/{validated_code}")


async def get_batch_fund_profiles(codes: list[str]) -> dict:
    """
    批量获取多只基金的画像数据，一次最多 20 只。
    返回 data（code → 画像）、complete、missingCodes、timedOut；
    适合同时对比多只基金的基本面，并显式识别部分结果。

    Args:
        codes: 项目编号列表，如 ["000001", "161725"]，最多 20 个
    """
    _require_token()
    validated_codes = []
    seen = set()
    for code in codes:
        normalized = _validate_fund_code(code)
        if normalized not in seen:
            validated_codes.append(normalized)
            seen.add(normalized)
    if len(validated_codes) > 20:
        raise ValueError("codes 最多支持 20 只基金")
    if not validated_codes:
        return {
            "data": {},
            "requestedCodes": [],
            "missingCodes": [],
            "complete": True,
            "timedOut": False,
        }
    payload = await _post("/api/fund/profile/batch", {"codes": validated_codes})
    return payload if isinstance(payload, dict) else {
        "data": {},
        "requestedCodes": validated_codes,
        "missingCodes": validated_codes,
        "complete": False,
        "timedOut": False,
    }


async def get_fund_quant_metrics(
    code: str,
    view: str,
    technical_value: Optional[float] = None,
    value_basis: str = "official_nav",
    value_as_of: str = "",
    source: str = "",
    target_nav_date: str = "",
    latest_official_nav_date: str = "",
    estimate_freshness: str = "",
    estimate_stale: Optional[bool] = None,
    fallback_reason: str = "",
    last_good_captured_at: str = "",
) -> dict:
    """
    按语义视图获取单只基金由后端统一计算的量化数据。
    technical=技术卡、估值位置与历史统计；momentum=短中期收益/均线偏离/连跌；
    risk=中长期收益/回撤/波动；full=完整数据。必须按问题选择视图。
    默认使用最新官方净值；如已通过 get_item_estimate 取得盘中估算值，可传
    technical_value 和 value_basis="live_estimate"，避免 Agent 拉取净值历史重复计算。
    必须检查 historyFreshness/historyExpectedAsOf、metrics.complete 与 current.status；
    stale/missing/unknown 会 fail-closed，并在可行时后台刷新。顶层 retryAfterMs 存在时，
    按该间隔有界重试，最多 3 次；仍不完整则说明补数未完成。
    可精确关联境内指数时，technical.current.indexValuation 返回指数 PE 与历史分位；
    peBasis=live_index_price_estimate 表示 PE 按今日指数点位估算，officialPeAsOf 是官方 PE 基准日，
    peBasis=official_daily 表示直接使用 dataAsOf 当日官方 PE；estimateStale=true 表示正在后台刷新、
    当前返回的是短暂保留的最近估算帧；
    其他基金的 navPositionPercentilePct 使用近 250 个官方净值点作为分布，传入
    live_estimate 时以实时估算净值计算今日位置。必须检查 valueBasis 与数据日期。
    本工具只提供数据与统计，不输出买卖方向或建议金额。

    Args:
        code: 6 位基金代码。
        view: technical、momentum、risk 或 full；不要无条件使用 full。
        technical_value: 可选，当前有效估算净值；不传则使用官方净值口径。
        value_basis: official_nav 或 live_estimate。
        value_as_of: 当前值归属/观察日期，建议使用估算帧的 display_date。
        source: 当前值的数据源标识。
        target_nav_date: 当前估算帧对应的目标净值 D 日。
        latest_official_nav_date: 已公布的最新官方净值 D 日。
        estimate_freshness: 对应估算帧的 fresh、stale 或 unavailable 状态。
        estimate_stale: 对应估算帧是否来自陈旧兜底。
        fallback_reason: 估算帧发生降级时的原因。
        last_good_captured_at: last-good 估算帧的 ISO 8601 捕获时间。
    """
    _require_token()
    validated_code = _validate_fund_code(code)
    validated_view = _validate_quant_view(view)
    has_current_frame = any((
        technical_value is not None,
        value_basis != "official_nav",
        value_as_of,
        source,
        target_nav_date,
        latest_official_nav_date,
        estimate_freshness,
        estimate_stale is not None,
        fallback_reason,
        last_good_captured_at,
    ))
    if has_current_frame and validated_view not in {"technical", "full"}:
        raise ValueError("当前估算帧仅适用于 technical 或 full 视图")
    frame = _validate_quant_current_frame({
        "valueBasis": value_basis,
        **({"technicalValue": technical_value} if technical_value is not None else {}),
        **({"valueAsOf": value_as_of} if value_as_of else {}),
        **({"source": source} if source else {}),
        **({"targetNavDate": target_nav_date} if target_nav_date else {}),
        **({"latestOfficialNavDate": latest_official_nav_date} if latest_official_nav_date else {}),
        **({"estimateFreshness": estimate_freshness} if estimate_freshness else {}),
        **({"estimateStale": estimate_stale} if estimate_stale is not None else {}),
        **({"fallbackReason": fallback_reason} if fallback_reason else {}),
        **({"lastGoodCapturedAt": last_good_captured_at} if last_good_captured_at else {}),
    }) if validated_view in {"technical", "full"} else {}
    params = {"view": validated_view, **frame}
    return await _get(f"/api/fund/quant-metrics/{validated_code}", params=params)


async def get_batch_fund_quant_metrics(
    codes: list[str],
    view: str,
    current_frames: Optional[dict] = None,
) -> dict:
    """
    批量获取后端统一量化数据。technical、momentum、risk 最多 50 只，
    full 最多 10 只。服务端按视图加载依赖并批量读缓存/数据库；
    不要为每只基金并发调用单只接口。本工具不输出投资建议。
    顶层 complete 仅在所有代码都有官方净值且 freshness 可验证时为 true；指标视图的
    251 点窗口检查 item.metrics.complete，full 检查 item.official.metrics.complete；还必须检查
    staleCodes、unverifiedCodes、refreshingCodes 与 item.historyFreshness。历史统计检查
    item.current.status。过期历史会 fail-closed 为 complete=false/computing，并后台刷新；
    顶层或 current 的 retryAfterMs 存在时可按该间隔有界重试，最多 3 次；
    insufficient_history / insufficient_samples 是当前数据集下的终态。

    Args:
        codes: 6 位基金代码列表，最多 50 只；非法代码会直接报错。
        view: technical、momentum、risk 或 full；不要无条件使用 full。
        current_frames: 可选，code 到当前估算帧的映射；字段使用 technicalValue、
            valueBasis、valueAsOf、source、targetNavDate、latestOfficialNavDate，及可选的
            estimateFreshness、estimateStale、fallbackReason、lastGoodCapturedAt。
    """
    _require_token()
    validated_view = _validate_quant_view(view)
    if len(codes) > 50:
        raise ValueError("codes 最多支持 50 只基金")
    validated_codes = []
    seen = set()
    for code in codes:
        normalized = _validate_fund_code(code)
        if normalized not in seen:
            validated_codes.append(normalized)
            seen.add(normalized)
    if not validated_codes:
        raise ValueError("codes 不能为空")
    if validated_view == "full" and len(validated_codes) > 10:
        raise ValueError("full 视图批量请求最多支持 10 只基金")
    if current_frames is not None and not isinstance(current_frames, dict):
        raise ValueError("current_frames 必须是对象")
    normalized_frames = current_frames or {}
    if normalized_frames and validated_view not in {"technical", "full"}:
        raise ValueError("current_frames 仅适用于 technical 或 full 视图")
    unexpected = set(normalized_frames) - set(validated_codes)
    if unexpected:
        raise ValueError("current_frames 只能包含本次请求的基金代码")
    normalized_frames = {
        code: _validate_quant_current_frame(frame)
        for code, frame in normalized_frames.items()
    }
    return await _post(
        "/api/fund/quant-metrics/batch",
        {
            "codes": validated_codes,
            "view": validated_view,
            "currentFrames": normalized_frames,
        },
    )


async def get_batch_fund_period_ranks(codes: list[str]) -> dict:
    """
    批量获取多个项目的近期业绩排名，code → 排名数据的映射位于 data 字段。
    一次请求处理最多 50 个项目，适合同时查看多个项目的表现对比。
    超过 50 个会直接报错，不会静默截断。

    Args:
        codes: 项目编号列表，如 ["000001", "161725"]，最多 50 个
    """
    _require_token()
    return await _get_batch_period_ranks(
        codes,
        validate_code=_validate_fund_code,
        post=_post,
    )
