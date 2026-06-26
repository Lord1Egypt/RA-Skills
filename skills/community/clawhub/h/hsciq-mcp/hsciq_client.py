#!/usr/bin/env python3
"""
HSCIQ MCP Python Client
海关编码查询服务 - Python 客户端

功能:
- 搜索海关编码
- 获取编码详情（税率、申报要素、监管条件）
- 搜索归类实例
- 统一搜索（CIQ/危化品/港口）
- 创建归类咨询单（支持产品信息与图片上传，提交人工复核）
- 获取归类咨询单详情
- 查看归类咨询单列表
- 归类单讨论（新建/回复）

使用示例:
    python hsciq_client.py search-code --keywords "塑料软管" --country CN
    python hsciq_client.py get-detail --code "3926909090"
    python hsciq_client.py search-instance --keywords "蓝牙耳机"
    python hsciq_client.py search-unified --keywords "食品" --type ciq
    python hsciq_client.py create-guilei-form --productNameCn "智能手机壳" --uses "手机保护" --images ./front.jpg
    python hsciq_client.py get-guilei-form --formId "abc123..."
    python hsciq_client.py list-my-guilei-forms --pageIndex 1
    python hsciq_client.py add-guilei-dialog-message --formId "abc..." --fieldKey "ProductNameCn" --content "追问"
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
    """HSCIQ MCP API 客户端"""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.getenv("HSCIQ_BASE_URL") or
                        self._load_config().get("baseUrl", DEFAULT_BASE_URL))
        self.api_key = (api_key or os.getenv("HSCIQ_API_KEY") or
                       self._load_config().get("apiKey", ""))
        self.auth_header = self._load_config().get("authHeader", "X-API-Key")

    def _load_config(self) -> Dict[str, str]:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _request(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/mcp/tools/call"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers[self.auth_header] = self.api_key

        payload = {"toolName": tool_name, "arguments": arguments}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            raise Exception(f"API request failed (HTTP {e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")
        except json.JSONDecodeError as e:
            raise Exception(f"Response parse error: {e}")

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
                       pageIndex: int = 1, pageSize: int = 10) -> Dict[str, Any]:
        return self._request("search_unified", {
            "keywords": keywords, "unifiedType": search_type,
            "pageIndex": pageIndex, "pageSize": pageSize
        })

    def create_guilei_form(self, productNameCn: str, productNameEn: Optional[str] = None,
                           uses: Optional[str] = None, ingredients: Optional[str] = None,
                           cas: Optional[str] = None, brand: Optional[str] = None,
                           model: Optional[str] = None, otherProductInfo: Optional[str] = None,
                           qq: Optional[str] = None, weixin: Optional[str] = None,
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
            isPaid: 是否付费咨询
            images: 图片文件路径列表（最多3张，每张≤1MB，支持jpg/png/gif/webp）

        Returns:
            {"formId": "...", "status": "已创建", "imageCount": N, "imageUrls": [...]}
        """
        if not productNameCn:
            raise ValueError("productNameCn is required")

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
                                  messageType: Optional[int] = None) -> Dict[str, Any]:
        """
        在归类咨询单字段上创建新对话或回复已有对话。

        Args:
            formId: 表单 GUID（必填）
            fieldKey: 字段名（必填，如 ProductNameCn、Uses 等）
            content: 消息内容（必填）
            dialogId: 对话 ID（不为空时回复已有对话，为空时新建对话）
            messageType: 可选的消息类型

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

        return self._request("add_guilei_dialog_message", arguments)

    def list_tools(self) -> Dict[str, Any]:
        url = f"{self.base_url}/mcp/tools/list"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers[self.auth_header] = self.api_key
        req = urllib.request.Request(url, data=b'{}', headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            raise Exception(f"API request failed (HTTP {e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")
        except json.JSONDecodeError as e:
            raise Exception(f"Response parse error: {e}")


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
    search_parser.add_argument('--country', default='CN', help='Country code (CN/JP/US)')

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
    guilei_parser.add_argument('--isPaid', action='store_true', help='Paid consultation')
    guilei_parser.add_argument('--images', nargs='+', help='Image file paths (max 3, ≤1MB each, jpg/png/gif/webp)')

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
            result = client.search_unified(args.keywords, args.type)
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
                messageType=args.messageType
            )
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
