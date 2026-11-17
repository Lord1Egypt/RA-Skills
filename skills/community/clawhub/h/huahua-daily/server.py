"""HuahuaDaily MCP compatibility facade and console entry point."""

import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

_SERVER_DIR = str(Path(__file__).resolve().parent)
if _SERVER_DIR not in sys.path:
    sys.path.insert(0, _SERVER_DIR)

from huahua_mcp_runtime.client import (  # noqa: E402,F401 -- compatibility facade
    OFFICIAL_API as _OFFICIAL_API,
    PORTFOLIO_TTL as _PORTFOLIO_TTL,
    clear_session_caches as _clear_session_caches,
    delete as _delete,
    get as _get,
    get_client as _get_client,
    get_download_lock as _get_download_lock,
    get_optional as _get_optional,
    headers as _headers,
    portfolio_cache as _portfolio_cache,
    post as _post,
    post_files as _post_files,
    put as _put,
    request_generation as _request_generation,
    require_token as _require_token,
    session as _session,
    url as _url,
)
from huahua_mcp_runtime.portfolio_math import (  # noqa: E402,F401 -- compatibility facade
    beijing_date_string as _beijing_date_string,
    calc_change_profit as _calc_change_profit,
    calc_correction_delta_total as _calc_correction_delta_total,
    calc_fund_stats as _calc_fund_stats,
    is_valid_correction as _is_valid_correction_tx,
    js_round as _js_round,
    r2 as _r2,
    r4 as _r4,
    r6 as _r6,
    ratio_pct as _ratio_pct,
    parse_percent as _parse_percent,
    resolve_amount as _resolve_amount,
    resolve_buy_shares as _resolve_buy_shares,
    resolve_sell_shares as _resolve_sell_shares,
    sort_transactions as _sort_txs,
    to_float as _to_float,
    tx_effective_date as _tx_effective_date,
)
from huahua_mcp_runtime.portfolio_adapter import (  # noqa: E402,F401 -- compatibility facade
    is_empty_plain_object as _is_empty_plain_object,
    is_restorable_fund as _is_restorable_fund,
    is_valid_fund_code_value as _is_valid_fund_code_value,
    portfolio_payload_source as _portfolio_payload_source,
    summarize_sync_payload as _summarize_sync_payload,
    unwrap_sync_payload as _unwrap_sync_payload,
)
from huahua_mcp_runtime.validation import (  # noqa: E402,F401 -- compatibility facade
    detect_image_mime as _detect_image_mime,
    normalize_data_source_mode as _normalize_data_source_mode,
    normalize_upload_files as _normalize_upload_files,
    summarize_import_items as _summarize_import_items,
    validate_amount as _validate_amount,
    validate_data_cutoff as _validate_data_cutoff,
    validate_date as _validate_date,
    validate_fund_code as _validate_fund_code,
    validate_image_file as _validate_image_file,
)
from huahua_mcp_runtime.manifest import build_tool_manifest  # noqa: E402,F401 -- runtime binding
from huahua_mcp_runtime.update_check import mcp_lifespan  # noqa: E402
from huahua_mcp_runtime.version import __version__  # noqa: E402
from huahua_mcp_runtime.facade_helpers import (  # noqa: E402,F401 -- compatibility facade
    download_portfolio as _download_portfolio_impl,
    download_portfolio_raw as _download_portfolio_raw_impl,
    estimate_semaphore as _estimate_semaphore,
    fetch_estimates as _fetch_estimates_impl,
)
from huahua_mcp_runtime.tool_registry import TOOL_MODULES as _TOOL_MODULES  # noqa: E402,F401
from huahua_mcp_runtime.tool_registry import TOOL_NAMES as _TOOL_NAMES  # noqa: E402,F401
from huahua_mcp_runtime.tool_registry import register_tools  # noqa: E402

MCP_INSTRUCTIONS = (
    "仅在首次接入、配置变更或排障时调用 get_tool_manifest；普通会话无需重复。"
    "若 runtime.updateCheck.updateAvailable=true，先告知用户当前版本、最新版本和更新步骤；"
    "不要自行安装或覆盖用户环境。"
)
mcp = FastMCP(
    "huahua-daily",
    instructions=MCP_INSTRUCTIONS,
    lifespan=mcp_lifespan,
)
# FastMCP does not currently expose its protocol server version in the public
# constructor. Set it explicitly so initialize responses identify this runtime
# instead of the installed mcp library version.
mcp._mcp_server.version = __version__


async def _fetch_estimates(
    codes: list,
    default_data_source_mode: str = "source_a",
    data_source_mode_by_code: Optional[dict] = None,
) -> dict:
    return await _fetch_estimates_impl(
        globals(),
        codes,
        default_data_source_mode,
        data_source_mode_by_code,
    )


async def _download_portfolio() -> dict:
    return await _download_portfolio_impl(globals())


async def _download_portfolio_raw() -> tuple[dict, str]:
    return await _download_portfolio_raw_impl(globals())


register_tools(mcp, globals())


def main() -> None:
    """uvx / console_scripts 入口点。"""
    mcp.run()


if __name__ == "__main__":
    main()
