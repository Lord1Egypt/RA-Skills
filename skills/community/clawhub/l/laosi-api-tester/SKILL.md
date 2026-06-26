---
badge: premium
name: api-tester
version: 2.0.0
description: API测试 - 构建/发送HTTP请求，验证响应状态码/�?体，性能基准(延迟/吞吐�?，支持REST和GraphQL
tags: [api, testing, http, rest, graphql, development]
author: laosi
source: original
---

# API Tester - API接口测试

> 激活词: 测试API / api test / 接口测试

## 功能

- 发�?GET/POST/PUT/DELETE 请求
- 自定义请求头、Body (JSON/Form/Text)
- 响应状态码、头、体验证
- GraphQL 查询支持
- 延迟测量和性能基准
- 测试结果持久�?
## Python 实现

```python
import json, time, urllib.request, urllib.error
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict

@dataclass
class APIRequest:
    method: str = "GET"
    url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    content_type: str = "application/json"
    timeout: int = 10
    
    def to_urllib_request(self) -> urllib.request.Request:
        """转换为urllib请求对象"""
        data = None
        if self.body and self.method in ("POST", "PUT", "PATCH"):
            data = self.body.encode("utf-8") if isinstance(self.body, str) else self.body
            if "Content-Type" not in self.headers:
                self.headers["Content-Type"] = self.content_type
        
        req = urllib.request.Request(
            self.url,
            data=data,
            headers=self.headers,
            method=self.method
        )
        return req

@dataclass
class APIResponse:
    status: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    body_json: Optional[Dict] = None
    latency_ms: float = 0.0
    error: Optional[str] = None

class APITester:
    def __init__(self):
        self.history: List[Dict] = []
        self.history_file = os.path.join(
            os.path.dirname(__file__), "api_tests.json"
        )
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
    
    def send(self, request: APIRequest) -> APIResponse:
        """发送单个API请求"""
        resp = APIResponse()
        start = time.time()
        
        try:
            req = request.to_urllib_request()
            with urllib.request.urlopen(req, timeout=request.timeout) as conn:
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
        entry = {
            "method": request.method,
            "url": request.url,
            "status": resp.status,
            "latency_ms": resp.latency_ms,
            "error": resp.error,
            "timestamp": datetime.now().isoformat(),
        }
        self._save_history(entry)
        
        return resp
    
    def batch(self, requests: List[APIRequest], concurrency: int = 1) -> List[APIResponse]:
        """批量发送请�?""
        results = []
        for req in requests:
            results.append(self.send(req))
        return results
    
    def benchmark(self, url: str, count: int = 5, method: str = "GET") -> dict:
        """性能基准测试"""
        latencies = []
        errors = 0
        for i in range(count):
            req = APIRequest(method=method, url=url)
            resp = self.send(req)
            if resp.error:
                errors += 1
            else:
                latencies.append(resp.latency_ms)
        
        return {
            "url": url,
            "requests": count,
            "errors": errors,
            "latency": {
                "min": min(latencies) if latencies else None,
                "max": max(latencies) if latencies else None,
                "avg": round(sum(latencies) / len(latencies), 1) if latencies else None,
                "p50": sorted(latencies)[len(latencies)//2] if latencies else None,
                "p99": sorted(latencies)[int(len(latencies)*0.99)] if len(latencies) > 1 else None,
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def graphql(self, endpoint: str, query: str, variables: dict = None) -> APIResponse:
        """发送GraphQL查询"""
        body = json.dumps({"query": query, "variables": variables or {}})
        req = APIRequest(
            method="POST",
            url=endpoint,
            body=body,
            content_type="application/json"
        )
        return self.send(req)
    
    def validate(self, resp: APIResponse, rules: Dict[str, Any]) -> List[str]:
        """验证响应是否符合规则"""
        failures = []
        
        if "status" in rules and resp.status != rules["status"]:
            failures.append(f"Status: expected {rules['status']}, got {resp.status}")
        
        if "header_contains" in rules:
            for key, val in rules["header_contains"].items():
                actual = resp.headers.get(key)
                if actual != val:
                    failures.append(f"Header {key}: expected '{val}', got '{actual}'")
        
        if "body_contains" in rules:
            for key in rules["body_contains"]:
                if resp.body_json and key not in resp.body_json:
                    failures.append(f"Body missing key: '{key}'")
        
        if "latency_max" in rules and resp.latency_ms > rules["latency_max"]:
            failures.append(f"Latency: {resp.latency_ms}ms > max {rules['latency_max']}ms")
        
        return failures
    
    def _save_history(self, entry: dict):
        entries = []
        if os.path.exists(self.history_file):
            with open(self.history_file, encoding="utf-8") as f:
                entries = json.load(f).get("tests", [])
        entries.append(entry)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump({"tests": entries}, f, ensure_ascii=False, indent=2)

# 使用示例
tester = APITester()

# 简单GET请求
req = APIRequest(method="GET", url="https://httpbin.org/get")
resp = tester.send(req)
print(f"GET {req.url} -> {resp.status} ({resp.latency_ms}ms)")
if resp.body_json:
    print(f"  Origin: {resp.body_json.get('origin', 'N/A')}")

# POST JSON
req2 = APIRequest(
    method="POST",
    url="https://httpbin.org/post",
    body=json.dumps({"name": "test", "value": 42}),
)
resp2 = tester.send(req2)
print(f"POST -> {resp2.status} ({resp2.latency_ms}ms)")

# GraphQL查询
gql_resp = tester.graphql(
    "https://api.github.com/graphql",
    "{ viewer { login } }"
)
print(f"GraphQL -> {gql_resp.status}")

# 性能基准
bench = tester.benchmark("https://httpbin.org/get", count=3)
print(f"基准: avg={bench['latency']['avg']}ms, errors={bench['errors']}")

# 验证
rules = {"status": 200, "latency_max": 3000}
failures = tester.validate(resp, rules)
print(f"验证: {'PASS' if not failures else 'FAIL: ' + str(failures)}")
```

## 常用验证规则

```python
VALIDATION_RULES = {
    "health_check": {"status": 200, "latency_max": 500},
    "api_ok": {"status": 200, "body_contains": ["data", "status"]},
    "created": {"status": 201, "header_contains": {"Content-Type": "application/json"}},
    "no_content": {"status": 204},
    "redirect": {"status": 302},
    "unauthorized": {"status": 401},
    "not_found": {"status": 404},
    "server_error": {"status": 500, "latency_max": 5000},
}
```

## 使用场景

1. **CI/CD管道**: 部署后自动测试API健康检�?2. **接口文档**: 自动生成API请求示例
3. **性能回归**: 每次部署后基准测试，发现性能退�?4. **集成测试**: 微服务间API契约验证

## 依赖

- Python 3.8+
- 标准库（urllib, json, time�?