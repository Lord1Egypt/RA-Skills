#!/usr/bin/env python3
"""
专利交易 API 客户端 — 对接 trade `/api/skill`（token 鉴权，响应 `{success,data,total}`）

备用：设置 `TRADE_API_BASE_URL=https://trade.9235.net/nbapi` 可走官网同款 nbapi（无需 token）。
"""

import html
import importlib.util
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

_SKILL_DIR = Path(__file__).resolve().parent
_excel_mod: Any = None


def _load_excel_export() -> Any:
    global _excel_mod
    if _excel_mod is not None:
        return _excel_mod
    path = _SKILL_DIR / "excel_export.py"
    spec = importlib.util.spec_from_file_location(
        "skill_excel_export_patent_transaction", path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载 {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _excel_mod = mod
    return mod

DEFAULT_NBAPI_URL = "https://trade.9235.net/nbapi"
DEFAULT_SKILL_URL = "https://trade.9235.net/api/skill"

_PATENT_TYPE_LABEL = {1: "发明", 2: "实用新型", 3: "外观"}


def strip_highlight_markup(text: Any) -> str:
    """去掉 ES 高亮标签 <em> 等，避免聊天里出现乱码片段。"""
    if text is None:
        return ""
    s = str(text)
    s = re.sub(r"</?em>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def _sanitize_payload(obj: Any) -> Any:
    if isinstance(obj, str):
        return strip_highlight_markup(obj)
    if isinstance(obj, dict):
        return {k: _sanitize_payload(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_payload(x) for x in obj]
    return obj


def _table_cell(text: Any, max_len: int = 28) -> str:
    """Markdown 表格单元格：去高亮、转义竖线、截断。"""
    s = strip_highlight_markup(text) if text is not None else ""
    s = s.replace("|", "｜").replace("\n", " ").strip()
    if not s:
        return "—"
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def _format_price(price: Any) -> str:
    try:
        n = int(price)
        return f"¥{n:,}"
    except (TypeError, ValueError):
        return "—"


class TradeAPI:
    """专利交易 API 客户端"""

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        env_base = os.environ.get("TRADE_API_BASE_URL")
        self.base_url = (base_url or env_base or DEFAULT_SKILL_URL).rstrip("/")
        self._skill_mode = "/api/skill" in self.base_url

        self.token = token
        if not self.token:
            self.token = os.environ.get("TRADE_API_TOKEN")
        if not self.token:
            config_path = Path(__file__).parent / "config.json"
            if config_path.exists():
                with open(config_path, encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.token = cfg.get("token")
                    if not env_base and not base_url:
                        self.base_url = cfg.get("api_base_url", self.base_url).rstrip(
                            "/"
                        )
                        self._skill_mode = "/api/skill" in self.base_url

        if self._skill_mode and not self.token:
            raise ValueError(
                "未找到 API Token，/api/skill 需设置 TRADE_API_TOKEN 或 config.json"
            )

    def _normalize_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """将 nbapi 的 {code,data,total} 或 skill 的 {success,data} 转为统一结构。"""
        if self._skill_mode:
            if data.get("success"):
                out = dict(data)
                if out.get("data") is not None:
                    out["data"] = _sanitize_payload(out["data"])
                return out
            code = data.get("errorCode", data.get("code", 1))
            return {
                "success": False,
                "errorCode": code,
                "message": data.get("message") or data.get("msg") or "请求失败",
            }

        code = data.get("code", 1)
        if code == 0:
            out: Dict[str, Any] = {
                "success": True,
                "data": _sanitize_payload(data.get("data")),
                "total": data.get("total"),
            }
            if data.get("msg"):
                out["message"] = data["msg"]
            return out
        return {
            "success": False,
            "errorCode": code,
            "message": data.get("msg") or data.get("message") or "请求失败",
        }

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if params is None:
            params = {}
        if self._skill_mode and self.token:
            params["t"] = self.token
            params["v"] = 1
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            resp = requests.get(url, params=params, timeout=30)
            if resp.status_code != 200:
                return {
                    "success": False,
                    "errorCode": resp.status_code,
                    "message": resp.text[:200],
                }
            raw = resp.json()
            if not isinstance(raw, dict):
                return {"success": False, "errorCode": 203, "message": "响应格式错误"}
            return self._normalize_response(raw)
        except requests.exceptions.Timeout:
            return {"success": False, "errorCode": 408, "message": "请求超时"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "errorCode": 503, "message": "连接失败"}
        except Exception as e:
            return {"success": False, "errorCode": 500, "message": str(e)}

    def search_products(
        self,
        keyword: str = "",
        page: int = 1,
        page_size: int = 10,
        price_range: Optional[str] = None,
    ) -> Dict[str, Any]:
        """搜索在售专利"""
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }
        if keyword:
            params["q"] = keyword
        if price_range:
            params["priceRange"] = price_range
        return self._make_request("product/search", params)

    def get_product_detail(self, application_number: str) -> Dict[str, Any]:
        """专利交易详情"""
        return self._make_request(f"product/detail/{application_number}")

    def get_product_sellers(self, application_number: str) -> Dict[str, Any]:
        """挂牌卖家信息"""
        return self._make_request(f"product/sellers/{application_number}")

    def list_orders(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """成交记录列表"""
        return self._make_request(
            "orders", {"page": page, "pageSize": page_size}
        )

    def get_order_detail(self, application_number: str) -> Dict[str, Any]:
        """成交详情"""
        return self._make_request(f"order/detail/{application_number}")

    def search_open_patent(
        self, keyword: str = "", page: int = 1, page_size: int = 10
    ) -> Dict[str, Any]:
        """开放许可专利搜索"""
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        if keyword:
            params["q"] = keyword
        return self._make_request("openPatent/search", params)

    def get_open_patent(self, application_number: str) -> Dict[str, Any]:
        """开放许可详情"""
        return self._make_request(f"openPatent/{application_number}")

    def search_demand(
        self, keyword: str = "", page: int = 1, page_size: int = 10
    ) -> Dict[str, Any]:
        """采购需求搜索"""
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        if keyword:
            params["q"] = keyword
        return self._make_request("demand/search", params)

    def format_search_result(self, result: Dict[str, Any]) -> str:
        """格式化在售专利列表（Markdown 表格）"""
        if not result.get("success"):
            code = result.get("errorCode", "?")
            msg = strip_highlight_markup(result.get("message", "未知错误"))
            return f"❌ 查询失败 [{code}]: {msg}"

        items: List[Dict[str, Any]] = result.get("data") or []
        total = result.get("total", len(items))
        shown = items[:10]
        n_shown = len(shown)

        lines = [
            "### 🏪 在售专利检索结果",
            "",
            f"**共 {total:,} 条**（下表为本页 {n_shown} 条）",
            "",
            "| 序号 | 专利名称 | 类型 | 价格 | 申请号 | 权利人 |",
            "|:---:|:---|:---:|:---:|:---|:---|",
        ]
        for i, p in enumerate(shown, 1):
            title = _table_cell(p.get("title") or p.get("summary"), 30)
            ptype = _PATENT_TYPE_LABEL.get(p.get("patentType"), "—")
            price = _format_price(p.get("price"))
            an = _table_cell(p.get("applicationNumber"), 18)
            applicant = _table_cell(p.get("applicant"), 16)
            lines.append(
                f"| {i} | {title} | {ptype} | {price} | {an} | {applicant} |"
            )

        if total > n_shown:
            lines.append("")
            lines.append(
                f"> 提示：仅展示前 {n_shown} 条，共 **{total:,}** 条。"
                "可缩小关键词或指定 `page` 翻页查看。"
            )
        return "\n".join(lines)

    def _export_dict(
        self,
        filename: str,
        headers: List[str],
        rows: List[List[Any]],
        sheet_name: str,
        summary: str,
    ) -> Dict[str, Any]:
        if not rows:
            return {"success": False, "message": "无数据可导出"}
        try:
            xl = _load_excel_export()
            asset, fmt = xl.export_table(
                filename,
                headers,
                rows,
                sheet_name=sheet_name,
                subdir="trade-exports",
            )
        except Exception as e:
            return {
                "success": False,
                "message": f"导出失败: {e}",
                "hint": "在售搜索 search、详情 detail 等仍可用。",
            }
        return {
            "success": True,
            "message": f"✅ 已导出 **{len(rows)}** 条（{fmt}）：{asset['name']}",
            "content": summary,
            "outbound_assets": [asset],
        }

    def export_search_excel(
        self,
        keyword: str = "",
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        page_size = min(max(page_size, 1), 100)
        result = self.search_products(keyword, page, page_size)
        if not result.get("success"):
            return result
        items = result.get("data") or []
        total = result.get("total", len(items))
        headers = [
            "序号",
            "专利名称",
            "类型",
            "价格",
            "申请号",
            "权利人",
            "权利人类型",
            "IPC",
            "更新日期",
        ]
        rows: List[List[Any]] = []
        for i, p in enumerate(items, 1):
            rows.append(
                [
                    i,
                    strip_highlight_markup(p.get("title") or p.get("summary")),
                    _PATENT_TYPE_LABEL.get(p.get("patentType"), ""),
                    p.get("price", 0),
                    p.get("applicationNumber", ""),
                    strip_highlight_markup(p.get("applicant", "")),
                    p.get("applicantType", ""),
                    p.get("domain", ""),
                    p.get("updatedAt", ""),
                ]
            )
        safe = re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", keyword or "在售")[:24]
        summary = (
            f"关键词：{keyword or '（全部）'}\n"
            f"共 {total:,} 条，本页导出 {len(rows)} 条（第 {page} 页）。"
        )
        return self._export_dict(
            f"在售专利-{safe}-p{page}", headers, rows, "在售专利", summary
        )

    def export_orders_excel(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        page_size = min(max(page_size, 1), 100)
        result = self.list_orders(page, page_size)
        if not result.get("success"):
            return result
        items = result.get("data") or []
        if not isinstance(items, list):
            items = []
        headers = ["序号", "申请号", "标题", "成交价", "成交日期", "买方", "卖方"]
        rows: List[List[Any]] = []
        for i, o in enumerate(items, 1):
            if not isinstance(o, dict):
                continue
            rows.append(
                [
                    i,
                    o.get("applicationNumber", o.get("an", "")),
                    strip_highlight_markup(o.get("title", "")),
                    o.get("price", o.get("dealPrice", "")),
                    o.get("dealDate", o.get("updatedAt", "")),
                    strip_highlight_markup(o.get("buyer", "")),
                    strip_highlight_markup(o.get("seller", "")),
                ]
            )
        summary = f"成交记录，本页 {len(rows)} 条（第 {page} 页）。"
        return self._export_dict(
            f"专利成交记录-p{page}", headers, rows, "成交记录", summary
        )
