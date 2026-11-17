#!/usr/bin/env python3
"""
HSCIQ MCP Python Client
海关编码查询服务 - Python 客户端

功能:
- 搜索海关编码（支持 10 国：CN/JP/US/EU/VN/MY/BR/MX/ID/CA）
- 获取编码详情（税率、申报要素、监管条件）
- 搜索归类实例
- 统一搜索（CIQ/危化品/港口）
- 创建归类咨询单（支持产品信息与图片上传，提交人工复核）
- 获取归类咨询单详情
- 查看归类咨询单列表
- 归类单讨论（新建/回复）
- 获取行业分类列表（用于创建归类咨询单时选择 categoryId）
- 海关公告（检索/详情/按编码反查，目前仅 CN）
- 船公司公告（船公司清单/检索/详情，仅最近 30 天）

使用示例:
    python hsciq_client.py search-code --keywords "塑料软管" --country CN
    python hsciq_client.py get-detail --code "3926909090"
    python hsciq_client.py search-instance --keywords "蓝牙耳机"
    python hsciq_client.py search-unified --keywords "食品" --type ciq
    python hsciq_client.py create-guilei-form --productNameCn "智能手机壳" --uses "手机保护" --images ./front.jpg
    python hsciq_client.py get-guilei-form --formId "abc123..."
    python hsciq_client.py list-my-guilei-forms --pageIndex 1
    python hsciq_client.py add-guilei-dialog-message --formId "abc..." --fieldKey "ProductNameCn" --content "追问"
    python hsciq_client.py list-guilei-categories
    python hsciq_client.py search-gonggao --keywords "关税"
    python hsciq_client.py get-gonggao-detail --gonggaoId 100
    python hsciq_client.py get-gonggao-by-code --code "8471300000"
    python hsciq_client.py list-ocean-carriers
    python hsciq_client.py search-ocean-carrier-notice --carrierCode MSC
    python hsciq_client.py get-ocean-carrier-notice-detail --noticeId "abc123..."
"""

import os
import sys
import json
import base64
import argparse
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

# 默认配置
DEFAULT_BASE_URL = "https://www.hsciq.com"
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/hsciq-mcp-config.json")


class HSCIQClient:
    """HSCIQ MCP API 客户端（标准 MCP 协议，JSON-RPC over Stateless Streamable HTTP，端点 /mcp/rpc）"""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.getenv("HSCIQ_BASE_URL") or
                        self._load_config().get("baseUrl", DEFAULT_BASE_URL))
        self.api_key = (api_key or os.getenv("HSCIQ_API_KEY") or
                       self._load_config().get("apiKey", ""))
        self.auth_header = self._load_config().get("authHeader", "X-API-Key")
        self._request_id = 0

    def _load_config(self) -> Dict[str, str]:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    @staticmethod
    def _parse_sse(body: str) -> Dict[str, Any]:
        """从 SSE (text/event-stream) 响应体中提取最后一条 message 事件的 JSON-RPC 数据；
        兼容非 SSE 的纯 JSON（如 401 错误）。"""
        data = None
        for line in body.split('\n'):
            t = line.strip()
            if t.startswith('data:'):
                data = t[5:].strip()
        return json.loads(data if data else body)

    def _rpc(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """标准 MCP JSON-RPC 调用。"""
        url = f"{self.base_url}/mcp/rpc"
        self._request_id += 1
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.api_key:
            headers[self.auth_header] = self.api_key

        payload = {"jsonrpc": "2.0", "id": self._request_id, "method": method, "params": params}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                body = response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            try:
                j = json.loads(error_body)
                error_body = j.get("message") or j.get("error") or error_body
            except Exception:
                pass
            raise Exception(f"API request failed (HTTP {e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")

        try:
            envelope = self._parse_sse(body)
        except json.JSONDecodeError as e:
            raise Exception(f"Response parse error: {e}")

        if envelope.get("error"):
            err = envelope["error"]
            raise Exception(f"{err.get('message', 'MCP error')} (code {err.get('code')})")
        return envelope.get("result") or {}

    def _request(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """tools/call：优先返回 structuredContent.result，兜底解析 content[].text。"""
        result = self._rpc("tools/call", {"name": tool_name, "arguments": arguments})

        if result.get("isError") is True:
            text = " ".join(c.get("text", "") for c in result.get("content", [])).strip()
            raise Exception(text or f"Tool {tool_name} failed")

        structured = result.get("structuredContent")
        if structured is not None:
            if isinstance(structured, dict) and "result" in structured:
                return structured["result"]
            return structured

        text = "".join(c.get("text", "") for c in result.get("content", [])).strip()
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"text": text}
        return result

    def search_code(self, keywords: str, country: str = "CN",
                    pageIndex: int = 1, pageSize: int = 10) -> Dict[str, Any]:
        return self._request("search_code", {
            "keywords": keywords, "country": country,
            "pageIndex": pageIndex, "pageSize": pageSize
        })

    def get_code_detail(self, code: str, country: str = "CN") -> Dict[str, Any]:
        return self._request("get_code_detail", {
            "code": code, "country": country
        })

    def search_instance(self, keywords: str, country: str = "CN",
                        pageIndex: int = 1, pageSize: int = 10) -> Dict[str, Any]:
        return self._request("search_instance", {
            "keywords": keywords, "country": country,
            "pageIndex": pageIndex, "pageSize": pageSize
        })

    def search_unified(self, keywords: str, search_type: str = "ciq",
                       pageIndex: int = 1, pageSize: int = 10,
                       searchType: int = 0) -> Dict[str, Any]:
        """
        统一搜索（CIQ/危化品/港口）。

        Args:
            keywords: 检索关键词
            search_type: 统一检索类型 ciq/hazardous/port（默认 ciq）
            searchType: 搜索方式，仅 hazardous 生效：0=名称（默认，与前台一致）1=CAS 号 2=海关编码
        """
        return self._request("search_unified", {
            "keywords": keywords, "unifiedType": search_type,
            "pageIndex": pageIndex, "pageSize": pageSize,
            "searchType": searchType
        })

    def create_guilei_form(self, productNameCn: str, productNameEn: Optional[str] = None,
                           uses: Optional[str] = None, ingredients: Optional[str] = None,
                           cas: Optional[str] = None, brand: Optional[str] = None,
                           model: Optional[str] = None, otherProductInfo: Optional[str] = None,
                           qq: Optional[str] = None, weixin: Optional[str] = None,
                           categoryId: Optional[int] = None,
                           isPaid: bool = False, images: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        创建 HS 归类咨询单，提交产品信息与图片给平台专业归类师人工审核。

        Args:
            productNameCn: 产品中文名称（必填）
            productNameEn: 产品英文名称
            uses: 产品用途
            ingredients: 产品成分/材质
            cas: CAS 号
            brand: 品牌
            model: 型号
            otherProductInfo: 其他产品信息
            qq: QQ 联系方式
            weixin: 微信联系方式
            categoryId: 行业分类 ID（可选，通过 list_guilei_categories 获取可用分类列表）
            isPaid: 是否付费咨询
            images: 图片文件路径列表（必填，至少1张，最多3张，每张≤1MB，支持jpg/png/gif/webp）

        Returns:
            {"formId": "...", "status": "已创建", "imageCount": N, "imageUrls": [...]}
        """
        if not productNameCn:
            raise ValueError("productNameCn is required")
        if not images:
            raise ValueError("images is required: at least 1 product image (1-3 images, ≤1MB each, jpg/png/gif/webp)")

        arguments: Dict[str, Any] = {"productNameCn": productNameCn}
        if productNameEn:
            arguments["productNameEn"] = productNameEn
        if uses:
            arguments["uses"] = uses
        if ingredients:
            arguments["ingredients"] = ingredients
        if cas:
            arguments["cas"] = cas
        if brand:
            arguments["brand"] = brand
        if model:
            arguments["model"] = model
        if otherProductInfo:
            arguments["otherProductInfo"] = otherProductInfo
        if qq:
            arguments["qq"] = qq
        if weixin:
            arguments["weixin"] = weixin
        if categoryId is not None:
            arguments["categoryId"] = categoryId
        if isPaid:
            arguments["isPaid"] = isPaid

        if images:
            image_entries = []
            valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
            for img_path in images[:3]:  # max 3 images
                ext = os.path.splitext(img_path)[1].lower()
                if ext not in valid_exts:
                    raise ValueError(f"Unsupported image format: {ext} (only jpg/png/gif/webp)")
                with open(img_path, "rb") as f:
                    data = f.read()
                if len(data) > 1024 * 1024:
                    raise ValueError(f"Image exceeds 1MB limit: {img_path}")
                image_entries.append({
                    "fileName": os.path.basename(img_path),
                    "data": base64.b64encode(data).decode("ascii")
                })
            arguments["images"] = image_entries

        return self._request("create_guilei_form", arguments)

    def get_guilei_form(self, formId: str) -> Dict[str, Any]:
        """
        获取归类咨询单详情，包含字段对话、归类结论等信息。

        Args:
            formId: 表单 GUID（必填）

        Returns:
            归类咨询单完整详情
        """
        if not formId:
            raise ValueError("formId is required")
        return self._request("get_guilei_form", {"formId": formId})

    def list_my_guilei_forms(self, pageIndex: int = 1, pageSize: int = 20) -> Dict[str, Any]:
        """
        获取当前用户的归类咨询单分页列表。

        Args:
            pageIndex: 页码（默认 1）
            pageSize: 每页条数（默认 20，最大 100）

        Returns:
            {"items": [...], "pageIndex": 1, "pageSize": 20, "totalItemCount": N, "totalPageCount": N}
        """
        return self._request("list_my_guilei_forms", {
            "pageIndex": pageIndex,
            "pageSize": pageSize
        })

    def add_guilei_dialog_message(self, formId: str, fieldKey: str, content: str,
                                  dialogId: Optional[str] = None,
                                  messageType: Optional[int] = None,
                                  parentMessageId: Optional[str] = None) -> Dict[str, Any]:
        """
        在归类咨询单字段上创建新对话或回复已有对话。

        Args:
            formId: 表单 GUID（必填）
            fieldKey: 字段名（必填，如 ProductNameCn、Uses 等）
            content: 消息内容（必填）
            dialogId: 对话 ID（不为空时回复已有对话，为空时新建对话）
            messageType: 可选的消息类型
            parentMessageId: 父消息 GUID（可选；仅回复已有对话时生效，表示回复该对话内的指定消息）

        Returns:
            {"dialogId": "...", "messageId": "...", "action": "created|reply"}
        """
        if not formId:
            raise ValueError("formId is required")
        if not fieldKey:
            raise ValueError("fieldKey is required")
        if not content:
            raise ValueError("content is required")

        arguments: Dict[str, Any] = {
            "formId": formId,
            "fieldKey": fieldKey,
            "content": content
        }
        if dialogId:
            arguments["dialogId"] = dialogId
        if messageType is not None:
            arguments["messageType"] = messageType
        if parentMessageId:
            arguments["parentMessageId"] = parentMessageId

        return self._request("add_guilei_dialog_message", arguments)

    def list_guilei_categories(self) -> Dict[str, Any]:
        """
        获取可用的行业分类列表，用于创建归类咨询单时选择 categoryId。

        Returns:
            [{"id": 1, "name": "分类名称"}, ...]
        """
        return self._request("list_guilei_categories", {})

    def search_gonggao(self, country: str = "CN", keywords: Optional[str] = None,
                       pageIndex: int = 1, pageSize: int = 10,
                       publishFrom: Optional[str] = None,
                       publishTo: Optional[str] = None) -> Dict[str, Any]:
        """
        检索海关公告（标题/文号/正文模糊匹配）。公告为公开数据，目前仅 CN。

        Args:
            country: 国家代码，仅 CN（US/JP 预留未接入）
            keywords: 检索关键词（可选；留空返回按发布时间倒序的最新公告）
            publishFrom: 发布日期起（yyyy-MM-dd，含当日）
            publishTo: 发布日期止（yyyy-MM-dd，含当日）
        """
        args: Dict[str, Any] = {"country": country, "pageIndex": pageIndex, "pageSize": pageSize}
        if keywords:
            args["keywords"] = keywords
        if publishFrom:
            args["publishFrom"] = publishFrom
        if publishTo:
            args["publishTo"] = publishTo
        return self._request("search_gonggao", args)

    def get_gonggao_detail(self, gonggaoId: int, country: str = "CN") -> Dict[str, Any]:
        """按 ID 查询海关公告详情，含正文及 3 组关联编码（created 新建/updated 修改/deleted 删除）。"""
        return self._request("get_gonggao_detail", {"gonggaoId": gonggaoId, "country": country})

    def get_gonggao_by_code(self, code: str, country: str = "CN",
                            pageIndex: int = 1, pageSize: int = 10) -> Dict[str, Any]:
        """按 HS 编码反查相关海关公告（CN 10 位纯数字，可带点分隔符），每项附 changeType（create/update/delete）。"""
        return self._request("get_gonggao_by_code", {
            "code": code, "country": country, "pageIndex": pageIndex, "pageSize": pageSize
        })

    def list_ocean_carriers(self) -> Dict[str, Any]:
        """查询启用中的船公司清单（SCAC 代码/名称），code 可作 search_ocean_carrier_notice 的 carrierCode。"""
        return self._request("list_ocean_carriers", {})

    def search_ocean_carrier_notice(self, keywords: Optional[str] = None,
                                    carrierCode: Optional[str] = None,
                                    pageIndex: int = 1, pageSize: int = 10) -> Dict[str, Any]:
        """
        检索船公司公告（仅匹配标题），仅返回最近 30 天内发布的公告，一律返回原文。

        Args:
            keywords: 检索关键词（可选；留空返回最新公告）
            carrierCode: 船公司 SCAC 代码（可选，如 MSC/MSK，不区分大小写）
        """
        args: Dict[str, Any] = {"pageIndex": pageIndex, "pageSize": pageSize}
        if keywords:
            args["keywords"] = keywords
        if carrierCode:
            args["carrierCode"] = carrierCode
        return self._request("search_ocean_carrier_notice", args)

    def get_ocean_carrier_notice_detail(self, noticeId: str) -> Dict[str, Any]:
        """按 ID 查询船公司公告详情（含正文原文）。仅支持最近 30 天内发布的公告。"""
        return self._request("get_ocean_carrier_notice_detail", {"noticeId": noticeId})

    def list_tools(self) -> Dict[str, Any]:
        """tools/list：返回服务器公布的工具列表（含 inputSchema/outputSchema）。"""
        result = self._rpc("tools/list", {})
        return result.get("tools", [])


def format_output(data: Dict[str, Any], indent: int = 2) -> str:
    return json.dumps(data, ensure_ascii=False, indent=indent)


def main():
    parser = argparse.ArgumentParser(
        description="HSCIQ MCP 海关编码查询服务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  %(prog)s search-code --keywords "塑料软管" --country CN
  %(prog)s get-detail --code "3926909090"
  %(prog)s search-instance --keywords "蓝牙耳机"
  %(prog)s search-unified --keywords "食品" --type ciq
  %(prog)s create-guilei-form --productNameCn "智能手机壳" --uses "手机保护" --images ./front.jpg
  %(prog)s get-guilei-form --formId "abc123..."
  %(prog)s list-my-guilei-forms --pageIndex 1
  %(prog)s add-guilei-dialog-message --formId "abc..." --fieldKey "ProductNameCn" --content "追问"
  %(prog)s list-guilei-categories
  %(prog)s search-gonggao --keywords "关税"
  %(prog)s get-gonggao-by-code --code "8471300000"
  %(prog)s list-ocean-carriers
  %(prog)s search-ocean-carrier-notice --carrierCode MSC
  %(prog)s list-tools
        """
    )

    parser.add_argument('--base-url', type=str, help='API base URL')
    parser.add_argument('--api-key', type=str, help='API key')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # search-code
    search_parser = subparsers.add_parser('search-code', help='Search HS codes')
    search_parser.add_argument('--keywords', required=True, help='Search keywords')
    search_parser.add_argument('--country', default='CN', help='Country code (CN/JP/US/EU/VN/MY/BR/MX/ID/CA)')

    # get-detail
    detail_parser = subparsers.add_parser('get-detail', help='Get code detail')
    detail_parser.add_argument('--code', required=True, help='HS code')
    detail_parser.add_argument('--country', default='CN', help='Country code')

    # search-instance
    instance_parser = subparsers.add_parser('search-instance', help='Search classification instances')
    instance_parser.add_argument('--keywords', required=True, help='Product name')
    instance_parser.add_argument('--country', default='CN', help='Country code')

    # search-unified
    unified_parser = subparsers.add_parser('search-unified', help='Unified search')
    unified_parser.add_argument('--keywords', required=True, help='Search keywords')
    unified_parser.add_argument('--type', default='ciq', help='Search type (ciq/hazardous/port)')
    unified_parser.add_argument('--searchType', type=int, default=0, help='Search mode for hazardous only: 0=name (default) 1=CAS 2=HS code')

    # create-guilei-form
    guilei_parser = subparsers.add_parser('create-guilei-form', help='Create HS classification consultation form')
    guilei_parser.add_argument('--productNameCn', required=True, help='Product name in Chinese (required)')
    guilei_parser.add_argument('--productNameEn', help='Product name in English')
    guilei_parser.add_argument('--uses', help='Product usage')
    guilei_parser.add_argument('--ingredients', help='Ingredients/materials')
    guilei_parser.add_argument('--cas', help='CAS number')
    guilei_parser.add_argument('--brand', help='Brand')
    guilei_parser.add_argument('--model', help='Model')
    guilei_parser.add_argument('--otherProductInfo', help='Other product info')
    guilei_parser.add_argument('--qq', help='QQ contact')
    guilei_parser.add_argument('--weixin', help='WeChat contact')
    guilei_parser.add_argument('--categoryId', type=int, help='Industry category ID (optional, get available list via list-guilei-categories)')
    guilei_parser.add_argument('--isPaid', action='store_true', help='Paid consultation')
    guilei_parser.add_argument('--images', nargs='+', required=True, help='Image file paths (required, 1-3 images, ≤1MB each, jpg/png/gif/webp)')

    # get-guilei-form
    get_form_parser = subparsers.add_parser('get-guilei-form', help='Get classification consultation form detail')
    get_form_parser.add_argument('--formId', required=True, help='Form GUID (required)')

    # list-my-guilei-forms
    list_forms_parser = subparsers.add_parser('list-my-guilei-forms', help='List my classification consultation forms')
    list_forms_parser.add_argument('--pageIndex', type=int, default=1, help='Page index (default: 1)')
    list_forms_parser.add_argument('--pageSize', type=int, default=20, help='Page size (default: 20, max: 100)')

    # add-guilei-dialog-message
    dialog_parser = subparsers.add_parser('add-guilei-dialog-message', help='Add dialog message on consultation form field')
    dialog_parser.add_argument('--formId', required=True, help='Form GUID (required)')
    dialog_parser.add_argument('--fieldKey', required=True, help='Field key (required, e.g. ProductNameCn)')
    dialog_parser.add_argument('--content', required=True, help='Message content (required)')
    dialog_parser.add_argument('--dialogId', help='Dialog ID (reply to existing if set, create new if empty)')
    dialog_parser.add_argument('--messageType', type=int, help='Optional message type')
    dialog_parser.add_argument('--parentMessageId', help='Parent message GUID (only when replying to an existing dialog)')

    # list-guilei-categories
    subparsers.add_parser('list-guilei-categories', help='List industry categories for create-guilei-form categoryId')

    # search-gonggao
    gonggao_search_parser = subparsers.add_parser('search-gonggao', help='Search China customs announcements (CN only)')
    gonggao_search_parser.add_argument('--country', default='CN', help='Country code (CN only)')
    gonggao_search_parser.add_argument('--keywords', help='Keywords matching title/document number/content (empty = latest)')
    gonggao_search_parser.add_argument('--pageIndex', type=int, default=1, help='Page index (default: 1)')
    gonggao_search_parser.add_argument('--pageSize', type=int, default=10, help='Page size (default: 10, max: 50)')
    gonggao_search_parser.add_argument('--publishFrom', help='Publish date from (yyyy-MM-dd, inclusive)')
    gonggao_search_parser.add_argument('--publishTo', help='Publish date to (yyyy-MM-dd, inclusive)')

    # get-gonggao-detail
    gonggao_detail_parser = subparsers.add_parser('get-gonggao-detail', help='Get customs announcement detail with 3 code groups')
    gonggao_detail_parser.add_argument('--gonggaoId', type=int, required=True, help='Announcement ID (required)')
    gonggao_detail_parser.add_argument('--country', default='CN', help='Country code (CN only)')

    # get-gonggao-by-code
    gonggao_code_parser = subparsers.add_parser('get-gonggao-by-code', help='Look up customs announcements by HS code')
    gonggao_code_parser.add_argument('--code', required=True, help='HS code (CN 10 digits, dots allowed)')
    gonggao_code_parser.add_argument('--country', default='CN', help='Country code (CN only)')
    gonggao_code_parser.add_argument('--pageIndex', type=int, default=1, help='Page index (default: 1)')
    gonggao_code_parser.add_argument('--pageSize', type=int, default=10, help='Page size (default: 10, max: 50)')

    # list-ocean-carriers
    subparsers.add_parser('list-ocean-carriers', help='List enabled ocean carriers (SCAC code/name)')

    # search-ocean-carrier-notice
    notice_search_parser = subparsers.add_parser('search-ocean-carrier-notice', help='Search ocean carrier notices (last 30 days only)')
    notice_search_parser.add_argument('--keywords', help='Keywords matching notice title (empty = latest)')
    notice_search_parser.add_argument('--carrierCode', help='Carrier SCAC code (e.g. MSC/MSK, case-insensitive)')
    notice_search_parser.add_argument('--pageIndex', type=int, default=1, help='Page index (default: 1)')
    notice_search_parser.add_argument('--pageSize', type=int, default=10, help='Page size (default: 10, max: 50)')

    # get-ocean-carrier-notice-detail
    notice_detail_parser = subparsers.add_parser('get-ocean-carrier-notice-detail', help='Get ocean carrier notice detail (last 30 days only)')
    notice_detail_parser.add_argument('--noticeId', required=True, help='Notice GUID (required)')

    # list-tools
    subparsers.add_parser('list-tools', help='List available tools')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = HSCIQClient(base_url=args.base_url, api_key=args.api_key)

    try:
        result = None

        if args.command == 'search-code':
            result = client.search_code(args.keywords, args.country)
        elif args.command == 'get-detail':
            result = client.get_code_detail(args.code, args.country)
        elif args.command == 'search-instance':
            result = client.search_instance(args.keywords, args.country)
        elif args.command == 'search-unified':
            result = client.search_unified(args.keywords, args.type, searchType=args.searchType)
        elif args.command == 'create-guilei-form':
            result = client.create_guilei_form(
                productNameCn=args.productNameCn,
                productNameEn=args.productNameEn,
                uses=args.uses,
                ingredients=args.ingredients,
                cas=args.cas,
                brand=args.brand,
                model=args.model,
                otherProductInfo=args.otherProductInfo,
                qq=args.qq,
                weixin=args.weixin,
                categoryId=args.categoryId,
                isPaid=args.isPaid,
                images=args.images
            )
        elif args.command == 'get-guilei-form':
            result = client.get_guilei_form(args.formId)
        elif args.command == 'list-my-guilei-forms':
            result = client.list_my_guilei_forms(args.pageIndex, args.pageSize)
        elif args.command == 'add-guilei-dialog-message':
            result = client.add_guilei_dialog_message(
                formId=args.formId,
                fieldKey=args.fieldKey,
                content=args.content,
                dialogId=args.dialogId,
                messageType=args.messageType,
                parentMessageId=args.parentMessageId
            )
        elif args.command == 'list-guilei-categories':
            result = client.list_guilei_categories()
        elif args.command == 'search-gonggao':
            result = client.search_gonggao(args.country, args.keywords, args.pageIndex, args.pageSize, args.publishFrom, args.publishTo)
        elif args.command == 'get-gonggao-detail':
            result = client.get_gonggao_detail(args.gonggaoId, args.country)
        elif args.command == 'get-gonggao-by-code':
            result = client.get_gonggao_by_code(args.code, args.country, args.pageIndex, args.pageSize)
        elif args.command == 'list-ocean-carriers':
            result = client.list_ocean_carriers()
        elif args.command == 'search-ocean-carrier-notice':
            result = client.search_ocean_carrier_notice(args.keywords, args.carrierCode, args.pageIndex, args.pageSize)
        elif args.command == 'get-ocean-carrier-notice-detail':
            result = client.get_ocean_carrier_notice_detail(args.noticeId)
        elif args.command == 'list-tools':
            result = client.list_tools()

        if args.json:
            print(format_output(result))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
