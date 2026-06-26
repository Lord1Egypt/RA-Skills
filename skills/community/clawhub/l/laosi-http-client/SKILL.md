---
name: http-client
version: 1.0.0
description: HTTP客户端 - 发送GET/POST/PUT/DELETE请求，自定义请求头/Body，响应验证，超时控制，重试机制
tags: [http, api, client, rest, web, development]
author: laosi
source: original
---

# HTTP Client - 通用HTTP客户端

> 激活词: 发请求 / HTTP / 请求API / curl

## 功能

- GET/POST/PUT/DELETE/PATCH 请求
- 自定义请求头和Body (JSON/Form/Text)
- 响应状态码/头/体验证
- 超时控制和自动重试
- 请求历史日志
- 认证支持 (Bearer/Basic/API Key)

## Python 实现

```python
import json, time, urllib.request, urllib.error
from datetime import datetime
from typing import Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from urllib.parse import urlencode

@dataclass
class HTTPRequest:
    method: str = "GET"
    url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    content_type: str = "application/json"
    timeout: int = 10
    auth: Optional[str] = None  # "Bearer xxx" or "Basic xxx"
    
    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "content_type": self.content_type,
            "timeout": self.timeout,
        }

@dataclass
class HTTPResponse:
    status: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    body_json: Optional[Dict] = None
    latency_ms: float = 0.0
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "latency_ms": self.latency_ms,
            "error": self.error,
            "body_preview": self.body[:200] if self.body else None,
        }

class HTTPClient:
    def __init__(self):
        self.history: list = []
    
    def request(self, req: HTTPRequest) -> HTTPResponse:
        """发送HTTP请求"""
        resp = HTTPResponse()
        headers = dict(req.headers)
        
        if req.auth:
            headers["Authorization"] = req.auth
        
        data = None
        if req.body and req.method in ("POST", "PUT", "PATCH"):
            if isinstance(req.body, dict):
                data = json.dumps(req.body).encode("utf-8")
                headers["Content-Type"] = "application/json"
            elif isinstance(req.body, str):
                data = req.body.encode("utf-8")
                if req.content_type:
                    headers["Content-Type"] = req.content_type
            elif isinstance(req.body, bytes):
                data = req.body
        
        urllib_req = urllib.request.Request(req.url, data=data, headers=headers, method=req.method)
        
        start = time.time()
        try:
            with urllib.request.urlopen(urllib_req, timeout=req.timeout) as conn:
                resp.status = conn.status
                resp.headers = dict(conn.headers)
                resp.body = conn.read().decode("utf-8", errors="replace")
                try:
                    resp.body_json = json.loads(resp.body)
                except json.JSONDecodeError:
                    pass
        except urllib.error.HTTPError as e:
            resp.status = e.code
            resp.headers = dict(e.headers)
            resp.body = e.read().decode("utf-8", errors="replace")
            resp.error = f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            resp.error = f"URL Error: {e.reason}"
        except Exception as e:
            resp.error = str(e)
        
        resp.latency_ms = round((time.time() - start) * 1000, 1)
        
        # 保存历史
        entry = {**req.to_dict(), **resp.to_dict(), "timestamp": datetime.now().isoformat()}
        self.history.append(entry)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        return resp
    
    def get(self, url: str, headers: dict = None) -> HTTPResponse:
        return self.request(HTTPRequest(method="GET", url=url, headers=headers or {}))
    
    def post(self, url: str, body: Any = None, headers: dict = None) -> HTTPResponse:
        return self.request(HTTPRequest(method="POST", url=url, body=body, headers=headers or {}))
    
    def put(self, url: str, body: Any = None) -> HTTPResponse:
        return self.request(HTTPRequest(method="PUT", url=url, body=body))
    
    def delete(self, url: str) -> HTTPResponse:
        return self.request(HTTPRequest(method="DELETE", url=url))
    
    def retry(self, req: HTTPRequest, max_retries: int = 3, delay: float = 1.0) -> HTTPResponse:
        """带重试的请求"""
        for attempt in range(max_retries):
            resp = self.request(req)
            if not resp.error or resp.status < 500:
                return resp
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
        return resp
    
    def graphql(self, endpoint: str, query: str, variables: dict = None) -> HTTPResponse:
        """发送GraphQL查询"""
        body = {"query": query}
        if variables:
            body["variables"] = variables
        return self.post(endpoint, body)

# 使用示例
client = HTTPClient()

# GET请求
resp = client.get("https://httpbin.org/get")
print(f"GET -> {resp.status} ({resp.latency_ms}ms)")
if resp.body_json:
    print(f"  Origin: {resp.body_json.get('origin')}")

# POST JSON
resp2 = client.post("https://httpbin.org/post", {"name": "test", "value": 42})
print(f"POST -> {resp2.status} ({resp2.latency_ms}ms)")

# 带认证的请求
auth_resp = client.request(HTTPRequest(
    method="GET",
    url="https://api.github.com/user",
    auth="Bearer ghp_xxxxxxxxxxxx"
))

# GraphQL
gql = client.graphql(
    "https://api.github.com/graphql",
    "{ viewer { login name } }"
)
print(f"GraphQL -> {gql.status}")

# 重试请求
retry_resp = client.retry(HTTPRequest(method="GET", url="https://httpbin.org/delay/1"))

# 请求历史
print(f"\n最近 {len(client.history)} 个请求:")
for h in client.history[-3:]:
    print(f"  {h['method']} {h['url'][:40]} -> {h['status']} ({h['latency_ms']}ms)")
```

## 常用配置

```python
# GitHub API
github = HTTPClient()
github.request(HTTPRequest(
    method="GET",
    url="https://api.github.com/repos/octocat/hello-world",
    headers={"Accept": "application/vnd.github.v3+json"}
))

# 带API Key
api = HTTPClient()
api.request(HTTPRequest(
    method="GET",
    url="https://api.openai.com/v1/models",
    auth="Bearer sk-xxxxxxxxxxxx"
))
```

## 使用场景

1. **API集成**: 快速调用REST/GraphQL API
2. **Webhook测试**: 发送测试请求验证webhook端点
3. **数据采集**: 批量抓取API数据
4. **自动化**: 脚本化调用外部服务

## 依赖

- Python 3.8+
- 标准库（urllib, json）
