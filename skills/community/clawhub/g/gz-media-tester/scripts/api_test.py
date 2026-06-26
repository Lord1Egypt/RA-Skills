#!/usr/bin/env python3
"""
广州日报/融媒云接口测试工具
支持：GET/POST请求，自动鉴权，响应验证，报告输出
Usage: python3 api_test.py <url> <method> [--data JSON] [--token TOKEN] [--header KEY:VAL]
"""
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def print_header(url, method):
    print("=" * 60)
    print(f"  🧪 广州日报/融媒云 接口测试")
    print(f"  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"  URL    : {url}")
    print(f"  Method : {method}")
    print("-" * 60)


def run_test(url, method="GET", data=None, token=None, headers=None, timeout=10):
    """执行单次接口测试"""
    req_headers = {
        "Content-Type": "application/json",
        "User-Agent": "gz-media-tester/1.0",
        "Accept": "application/json",
    }
    if token:
        req_headers["Authorization"] = f"Bearer {token}"
    if headers:
        req_headers.update(headers)

    body_str = ""
    try:
        start = time.time()
        if method.upper() == "GET":
            resp = requests.get(url, headers=req_headers, timeout=timeout)
        elif method.upper() == "POST":
            body_str = json.dumps(data, ensure_ascii=False) if data else ""
            resp = requests.post(url, headers=req_headers, data=body_str, timeout=timeout)
        elif method.upper() == "PUT":
            body_str = json.dumps(data, ensure_ascii=False) if data else ""
            resp = requests.put(url, headers=req_headers, data=body_str, timeout=timeout)
        elif method.upper() == "DELETE":
            resp = requests.delete(url, headers=req_headers, timeout=timeout)
        else:
            return {"error": f"不支持的HTTP方法: {method}"}
        elapsed = (time.time() - start) * 1000

    except requests.exceptions.Timeout:
        return {"result": "FAIL", "error": f"请求超时（>{timeout}s）", "elapsed_ms": timeout * 1000}
    except requests.exceptions.ConnectionError as e:
        return {"result": "FAIL", "error": f"连接失败：{e}", "elapsed_ms": None}
    except Exception as e:
        return {"result": "FAIL", "error": str(e), "elapsed_ms": None}

    # 解析响应
    try:
        resp_json = resp.json()
    except Exception:
        resp_json = {"raw": resp.text[:500]}

    http_code = resp.status_code
    code = resp_json.get("code", http_code)
    message = resp_json.get("message", "")
    body_preview = json.dumps(resp_json, ensure_ascii=False)[:300]

    # 判断结果
    if http_code >= 500:
        result = "❌ FAIL"
        note = "服务端错误（5xx）"
    elif http_code == 401:
        result = "❌ FAIL"
        note = "未授权（401）"
    elif http_code == 403:
        result = "❌ FAIL"
        note = "禁止访问（403）"
    elif http_code >= 400:
        result = "❌ FAIL"
        note = f"客户端错误（{http_code}）"
    elif code != 200 and code not in (0, "0", "success"):
        result = "❌ FAIL"
        note = f"业务错误（code={code}）"
    else:
        elapsed_ms = round(elapsed)
        if elapsed_ms > 1000:
            result = "⚠️  WARN"
            note = f"响应慢（{elapsed_ms}ms > 1000ms）"
        else:
            result = "✅ PASS"
            note = f"响应正常（{elapsed_ms}ms）"

    return {
        "result": result,
        "http_code": http_code,
        "code": code,
        "message": message,
        "body": resp_json,
        "body_preview": body_preview,
        "elapsed_ms": round(elapsed),
        "note": note,
    }


def print_result(r):
    """打印测试结果"""
    print(f"\n📋 测试结果：{r['result']}")
    if "error" in r and "error" in r:
        print(f"   ⚠️  {r['error']}")
        return

    print(f"   HTTP状态码：{r['http_code']}")
    print(f"   业务code  ：{r['code']}")
    print(f"   响应时间  ：{r['elapsed_ms']} ms")
    print(f"   说明      ：{r['note']}")
    if r.get("message"):
        print(f"   消息      ：{r['message']}")
    print(f"\n📦 响应体预览：")
    print(f"   {r['body_preview']}")


def run_security_tests(url, token=None):
    """执行安全测试"""
    print("\n" + "=" * 60)
    print("  🔒 安全测试套件")
    print("=" * 60)

    tests = [
        ("SQL注入（OR 1=1）", {"username": "' OR 1=1 --", "password": "any"}),
        ("XSS攻击", {"content": "<script>alert(1)</script>"}),
        ("空Token访问", None),
        ("超长参数（1024字符）", {"content": "A" * 1024}),
    ]

    for name, payload in tests:
        print(f"\n--- {name} ---")
        if payload is None:
            # 空Token测试
            r = run_test(url, "POST", {}, token="invalid_token_abc123")
        else:
            r = run_test(url, "POST", payload, token=token)
        print_result(r)


def run_performance_test(url, method="GET", token=None, qps=10, duration=10):
    """简单性能测试"""
    print("\n" + "=" * 60)
    print(f"  ⚡ 性能测试（{qps} QPS，持续{duration}秒）")
    print("=" * 60)

    if not HAS_REQUESTS:
        print("⚠️ 需要安装 requests 库：pip3 install requests")
        return

    import threading
    results = {"success": 0, "fail": 0, "slow": 0, "times": []}
    lock = threading.Lock()
    interval = 1.0 / qps
    end_time = time.time() + duration

    def worker():
        while time.time() < end_time:
            r = run_test(url, method, token=token)
            with lock:
                results["times"].append(r.get("elapsed_ms", 0))
                if "FAIL" in r.get("result", ""):
                    results["fail"] += 1
                else:
                    results["success"] += 1
                    if r.get("elapsed_ms", 0) > 1000:
                        results["slow"] += 1
            time.sleep(interval)

    threads = [threading.Thread(target=worker) for _ in range(max(1, qps // 5))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    times = [t for t in results["times"] if t]
    times.sort()
    total = len(times)
    if not times:
        print("⚠️ 无有效请求")
        return

    p50 = times[int(total * 0.5)] if total > 0 else 0
    p95 = times[int(total * 0.95)] if total > 0 else 0
    p99 = times[int(total * 0.99)] if total > 0 else 0
    avg = sum(times) / total

    print(f"\n📊 性能报告：")
    print(f"   总请求数  ：{total}")
    print(f"   成功      ：{results['success']} | 失败：{results['fail']} | 慢（>1s）：{results['slow']}")
    print(f"   平均响应  ：{avg:.0f} ms")
    print(f"   P50       ：{p50} ms")
    print(f"   P95       ：{p95} ms")
    print(f"   P99       ：{p99} ms")


def check_install():
    """检查依赖"""
    if not HAS_REQUESTS:
        print("⚠️ 缺少 requests 库，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=True)
        global HAS_REQUESTS
        HAS_REQUESTS = True
        print("✅ requests 安装完成\n")


def main():
    parser = argparse.ArgumentParser(
        description="广州日报/融媒云接口测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 单次GET请求
  python3 api_test.py "https://api.example.com/news/list?page=1&size=10"

  # POST登录接口
  python3 api_test.py "https://api.example.com/user/login" POST \\
    --data '{"username":"test","password":"123456"}'

  # 带Token的请求
  python3 api_test.py "https://api.example.com/user/info" \\
    --token "eyJhbGciOiJIUzI1NiJ9..."

  # 安全测试
  python3 api_test.py "https://api.example.com/user/login" POST \\
    --data '{"username":"test","password":"123"}' \\
    --security

  # 性能测试
  python3 api_test.py "https://api.example.com/news/list" \\
    --perf --qps 20 --duration 10
"""
    )
    parser.add_argument("url", help="接口URL")
    parser.add_argument("method", nargs="?", default="GET", help="HTTP方法（GET/POST/PUT/DELETE）")
    parser.add_argument("--data", help="POST请求体（JSON字符串）")
    parser.add_argument("--token", help="Bearer Token")
    parser.add_argument("--header", action="append", help="额外请求头，格式 KEY:VAL")
    parser.add_argument("--timeout", type=int, default=10, help="请求超时（秒）")
    parser.add_argument("--security", action="store_true", help="执行安全测试套件")
    parser.add_argument("--perf", action="store_true", help="执行性能测试")
    parser.add_argument("--qps", type=int, default=10, help="性能测试QPS")
    parser.add_argument("--duration", type=int, default=10, help="性能测试持续时间（秒）")
    parser.add_argument("--report", help="输出报告文件路径（JSON）")

    args = parser.parse_args()

    check_install()

    # 解析额外headers
    extra_headers = {}
    if args.header:
        for h in args.header:
            if ":" in h:
                k, v = h.split(":", 1)
                extra_headers[k.strip()] = v.strip()

    # 解析data
    data = None
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
            print(f"❌ JSON解析错误：{args.data}")
            sys.exit(1)

    print_header(args.url, args.method)

    if args.security:
        run_security_tests(args.url, token=args.token)
        return

    if args.perf:
        run_performance_test(args.url, method=args.method, token=args.token,
                             qps=args.qps, duration=args.duration)
        return

    # 单次测试
    r = run_test(args.url, method=args.method, data=data, token=args.token,
                 headers=extra_headers, timeout=args.timeout)
    print_result(r)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告已保存：{args.report}")


if __name__ == "__main__":
    main()
