"""
基础客户端 - 对外提供普通 HTTP/CLI 接口，内部封装 MCP 通信细节
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional

DEFAULT_BASE_URL = 'https://mcp.jin10.com/mcp'
DEFAULT_PROTOCOL_VERSION = '2025-11-25'
DEFAULT_TIMEOUT = 30


class Jin10Error(Exception):
    """基础错误类"""

    def __init__(self, message: str, code: Optional[int] = None, data: Any = None):
        super().__init__(message)
        self.code = code
        self.data = data


@dataclass
class ClientState:
    """同一个 Jin10 会话的共享状态。"""

    base_url: str
    api_token: str
    request_id: int = 1
    initialized: bool = False
    session_id: Optional[str] = None


class BaseClient:
    """MCP 协议处理基础类。"""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_token: str = None,
        state: Optional[ClientState] = None,
    ):
        if state is None:
            state = ClientState(
                base_url=base_url,
                api_token=os.environ.get('JIN10_API_TOKEN', '') if api_token is None else api_token,
            )
        elif api_token is not None:
            state.api_token = api_token

        self._state = state

    @property
    def base_url(self) -> str:
        return self._state.base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._state.base_url = value

    @property
    def api_token(self) -> str:
        return self._state.api_token

    @api_token.setter
    def api_token(self, value: str) -> None:
        self._state.api_token = value

    @property
    def request_id(self) -> int:
        return self._state.request_id

    @request_id.setter
    def request_id(self, value: int) -> None:
        self._state.request_id = value

    @property
    def initialized(self) -> bool:
        return self._state.initialized

    @initialized.setter
    def initialized(self, value: bool) -> None:
        self._state.initialized = value

    @property
    def session_id(self) -> Optional[str]:
        return self._state.session_id

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        self._state.session_id = value

    def _require_api_token(self) -> None:
        if self.api_token:
            return
        raise Jin10Error('Missing API token. Set JIN10_API_TOKEN before calling Jin10.')

    def _next_request_id(self) -> int:
        request_id = self.request_id
        self.request_id += 1
        return request_id

    def _build_request(self, method: str, params: dict = None) -> dict:
        """构建带 id 的 JSON-RPC 请求。"""
        return {
            'jsonrpc': '2.0',
            'id': self._next_request_id(),
            'method': method,
            'params': params or {},
        }

    def _build_notify_request(self, method: str, params: dict = None) -> dict:
        """构建不带 id 的 JSON-RPC notification 请求。"""
        return {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
        }

    @staticmethod
    def _extract_sse_payload(raw_data: str) -> str:
        lines = []
        for line in raw_data.splitlines():
            if line.startswith('data:'):
                lines.append(line[5:].strip())

        if lines:
            return '\n'.join(lines)
        return raw_data.strip()

    @classmethod
    def _parse_json_body(cls, raw_data: str) -> Optional[dict]:
        raw_text = cls._extract_sse_payload(raw_data.strip())
        if not raw_text:
            return None

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return None

    @classmethod
    def _parse_sse_batch(cls, raw_data: str) -> list:
        """解析多个 SSE 事件，返回多个 JSON-RPC 响应。"""
        results = []
        for line in raw_data.splitlines():
            if line.startswith('data:'):
                text = line[5:].strip()
                try:
                    results.append(json.loads(text))
                except json.JSONDecodeError:
                    pass
        return results

    @staticmethod
    def _extract_rpc_error(error: dict) -> Jin10Error:
        code = error.get('code')
        message = error.get('message') or 'Unknown MCP error'
        return Jin10Error(f'MCP Error ({code}): {message}', code=code, data=error.get('data'))

    @staticmethod
    def _extract_tool_error(result: dict) -> str:
        structured = result.get('structuredContent')
        if isinstance(structured, dict):
            message = structured.get('message') or structured.get('error')
            if message:
                return str(message)

        content = result.get('content')
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get('text')
                    if text:
                        texts.append(str(text))
            if texts:
                return '\n'.join(texts)

        if isinstance(content, str) and content:
            return content

        return 'Tool execution error'

    @staticmethod
    def _extract_structured_result(result: dict) -> Any:
        if result.get('structuredContent') is not None:
            return result['structuredContent']

        content = result.get('content')
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('structuredContent') is not None:
                    return item['structuredContent']
            return content

        return result

    def _do_request(self, payload: dict) -> dict:
        """发送 HTTP 请求。"""
        self._require_api_token()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'Authorization': f'Bearer {self.api_token}',
        }
        if self.session_id:
            headers['Mcp-Session-Id'] = self.session_id

        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST',
        )

        try:
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
                self.session_id = response.headers.get('Mcp-Session-Id', self.session_id)
                raw_data = response.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='replace')
            parsed = self._parse_json_body(body)
            if parsed and 'error' in parsed:
                raise self._extract_rpc_error(parsed['error']) from None

            detail = body.strip()
            if detail:
                raise Jin10Error(f'HTTP Error: {exc.code} - {exc.reason}: {detail}') from None
            raise Jin10Error(f'HTTP Error: {exc.code} - {exc.reason}') from None
        except urllib.error.URLError as exc:
            raise Jin10Error(f'Network Error: {exc.reason}') from None

        if 'id' not in payload:
            return {}

        if not raw_data.strip():
            return {}

        result = self._parse_json_body(raw_data)
        if result is None:
            raise Jin10Error('Invalid JSON response returned from Jin10.')

        if 'error' in result:
            raise self._extract_rpc_error(result['error'])

        return result.get('result', {})

    def _do_batch_request(self, payloads: list) -> list:
        """发送批量 HTTP 请求（一次发送多个 JSON-RPC）。"""
        self._require_api_token()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'Authorization': f'Bearer {self.api_token}',
        }
        if self.session_id:
            headers['Mcp-Session-Id'] = self.session_id

        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(payloads).encode('utf-8'),
            headers=headers,
            method='POST',
        )

        try:
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
                self.session_id = response.headers.get('Mcp-Session-Id', self.session_id)
                raw_data = response.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='replace')
            raise Jin10Error(f'HTTP Error: {exc.code} - {exc.reason}: {body}') from None
        except urllib.error.URLError as exc:
            raise Jin10Error(f'Network Error: {exc.reason}') from None

        if not raw_data.strip():
            return []

        # SSE 批量响应：每个 JSON-RPC 响应是单独的 event: message\ndata:{...}
        results = self._parse_sse_batch(raw_data)
        if not results:
            raise Jin10Error('Invalid JSON response returned from Jin10.')

        # 检查是否有错误
        errors = [r.get('error') for r in results if 'error' in r]
        if errors:
            raise self._extract_rpc_error(errors[0])

        return [r.get('result') for r in results]

    def request(self, method: str, params: dict = None) -> Any:
        """发送请求（自动初始化）。"""
        if not self.initialized:
            self.initialize()
        return self._do_request(self._build_request(method, params))

    def notify(self, method: str, params: dict = None) -> None:
        """发送通知（无响应）。"""
        self._do_request(self._build_notify_request(method, params))

    def initialize(self) -> None:
        """初始化 MCP 连接。"""
        if self.initialized:
            return

        self._do_request(self._build_request('initialize', {
            'protocolVersion': DEFAULT_PROTOCOL_VERSION,
            'capabilities': {},
            'clientInfo': {
                'name': 'jin10-openclaw-skill',
                'version': '2.0.0',
            },
        }))
        self.notify('notifications/initialized')

        try:
            self._do_request(self._build_request('tools/list', {}))
            self._do_request(self._build_request('resources/list', {}))
        except Jin10Error:
            pass

        self.initialized = True

    def call_tool(self, name: str, arguments: dict = None) -> Any:
        """调用 MCP 工具。"""
        if not self.initialized:
            # 使用批量请求：initialize + tools/call 在同一次 HTTP 请求中
            init_payload = {
                'jsonrpc': '2.0',
                'id': self._next_request_id(),
                'method': 'initialize',
                'params': {
                    'protocolVersion': DEFAULT_PROTOCOL_VERSION,
                    'capabilities': {},
                    'clientInfo': {
                        'name': 'jin10-openclaw-skill',
                        'version': '2.0.0',
                    },
                },
            }
            tool_payload = {
                'jsonrpc': '2.0',
                'id': self._next_request_id(),
                'method': 'tools/call',
                'params': {
                    'name': name,
                    'arguments': arguments or {},
                },
            }
            results = self._do_batch_request([init_payload, tool_payload])
            # results[0] 是 initialize 结果，results[1] 是 tool call 结果
            if len(results) >= 2:
                result = results[1]
            else:
                result = results[-1] if results else {}
            self.initialized = True
        else:
            result = self._do_request(self._build_request('tools/call', {
                'name': name,
                'arguments': arguments or {},
            }))

        if not result:
            raise Jin10Error('No result returned from tool.')
        if result.get('isError'):
            raise Jin10Error(self._extract_tool_error(result))
        return self._extract_structured_result(result)

    def read_resource(self, uri: str) -> Any:
        """读取 MCP 资源。"""
        result = self.request('resources/read', {'uri': uri})
        if not result:
            return None

        contents = result.get('contents', [])
        for content in contents:
            if not isinstance(content, dict):
                continue
            if content.get('structuredContent') is not None:
                return content['structuredContent']
            if content.get('text'):
                return content['text']

        return result


class Jin10Client(BaseClient):
    """完整的 Jin10 客户端"""

    def __init__(self, api_token: str = None, base_url: str = DEFAULT_BASE_URL):
        super().__init__(base_url, api_token)
        self._quotes: Optional['QuotesClient'] = None
        self._flash: Optional['FlashClient'] = None
        self._news: Optional['NewsClient'] = None
        self._calendar: Optional['CalendarClient'] = None

    @property
    def quotes(self) -> 'QuotesClient':
        if self._quotes is None:
            self._quotes = QuotesClient(state=self._state)
        return self._quotes

    @property
    def flash(self) -> 'FlashClient':
        if self._flash is None:
            self._flash = FlashClient(state=self._state)
        return self._flash

    @property
    def news(self) -> 'NewsClient':
        if self._news is None:
            self._news = NewsClient(state=self._state)
        return self._news

    @property
    def calendar(self) -> 'CalendarClient':
        if self._calendar is None:
            self._calendar = CalendarClient(state=self._state)
        return self._calendar


# 延迟导入子模块避免循环引用
from .quotes import QuotesClient
from .flash import FlashClient
from .news import NewsClient
from .calendar import CalendarClient
