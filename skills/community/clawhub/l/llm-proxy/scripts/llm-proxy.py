#!/usr/bin/env python3
"""
- 协作者邮箱：394286006@qq.com
LLM Proxy with Content Filtering - v3.4
- ThreadingHTTPServer 并发处理
- 线程安全 stats
- 请求 ID 追踪
- 日志缓冲
- 请求体大小限制
- 优雅关闭（signal handler）
- 信号量限流
"""

import json
import re
import time
import os
import sys
import signal
import traceback
import uuid
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "llm-proxy-config.json")

def load_config():
    config_file = os.environ.get("LLM_PROXY_CONFIG", DEFAULT_CONFIG_FILE)
    default = {"proxy_port": 18979, "log_dir": "~/.openclaw/logs/llm-proxy",
               "rules_file": "content-filter-rules.json", "read_timeout": 60,
               "max_body_size_mb": 10, "max_threads": 50, "providers": {}}
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                print(f"[CONFIG] Loaded: {config_file}")
                for k in loaded:
                    if not k.startswith('_'): default[k] = loaded[k]
    except Exception as e: print(f"[CONFIG] Error: {e}")
    return default

CONFIG = load_config()
LISTEN_HOST = CONFIG.get("listen_host", "127.0.0.1")
PROXY_PORT = int(os.environ.get("LLM_PROXY_PORT", CONFIG.get("proxy_port", 18979)))
LOG_DIR = os.path.expanduser(CONFIG.get("log_dir", "~/.openclaw/logs/llm-proxy"))
RULES_FILE = os.environ.get("RULES_FILE", os.path.join(SCRIPT_DIR, CONFIG.get("rules_file", "content-filter-rules.json")))
READ_TIMEOUT = CONFIG.get("read_timeout", 60)
MAX_BODY_SIZE = CONFIG.get("max_body_size_mb", 10) * 1024 * 1024
MAX_THREADS = CONFIG.get("max_threads", 50)

PROVIDERS = {}
for pfx, info in CONFIG.get("providers", {}).items():
    if not pfx.startswith('_'):
        PROVIDERS[pfx] = info["url"] if isinstance(info, dict) else info

QUICK_CHECK_KEYWORDS = CONFIG.get("quick_check_keywords", [
    "关闭防火墙",
    "禁用防火墙",
    "停止防火墙",
    "socketfilterfw",
    "pfctl",
    "iptables -F",
    "关闭杀毒",
    "禁用杀毒",
    "关闭安全",
    "sudo su",
    "chmod 777",
    "rm -rf"
])
# 线程安全的统计
class ThreadSafeStats:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {
            "total_requests": 0,
            "total_responses": 0,
            "blocked": 0,
            "warnings": 0,
            "errors": 0,
            "start_time": time.time()
        }
    
    def increment(self, key):
        with self._lock:
            self._data[key] += 1
    
    def get(self, key=None):
        with self._lock:
            if key:
                return self._data[key]
            return dict(self._data)
    
    def to_dict(self):
        with self._lock:
            return dict(self._data)

stats = ThreadSafeStats()

# 线程安全的日志写入
class LogWriter:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self._lock = threading.Lock()
        os.makedirs(log_dir, exist_ok=True)
    
    def _get_log_file(self):
        return os.path.join(self.log_dir, f"proxy-{datetime.now().strftime('%Y-%m-%d')}.jsonl")
    
    def write(self, entry):
        with self._lock:
            try:
                with open(self._get_log_file(), 'a') as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            except Exception as e:
                print(f"[ERROR] 日志写入失败: {e}")

log_writer = LogWriter(LOG_DIR)

# 加载规则
def load_rules():
    try:
        with open(RULES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] 无法加载规则文件: {e}")
        return {"rules": [], "whitelist": []}

RULES = load_rules()

def check_content(content, rules):
    """分级审核：第一层恶意指令 + 第二层敏感内容"""
    alerts = []
    
    # 白名单检查
    for pattern in rules.get("whitelist", []):
        try:
            if re.search(pattern, content, re.IGNORECASE):
                return []
        except re.error:
            pass
    
    # 第一层：恶意指令检测
    layer1 = rules.get("layer1_malicious", {})
    if layer1.get("enabled", True):
        for rule in layer1.get("rules", []):
            for pattern in rule.get("patterns", []):
                try:
                    if re.search(pattern, content, re.IGNORECASE):
                        alerts.append({
                            "layer": "L1-恶意指令",
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"]
                        })
                        break
                except re.error:
                    pass
    
    # 第二层：敏感内容检测
    layer2 = rules.get("layer2_sensitive", {})
    if layer2.get("enabled", True):
        for rule in layer2.get("rules", []):
            for pattern in rule.get("patterns", []):
                try:
                    if re.search(pattern, content, re.IGNORECASE):
                        alerts.append({
                            "layer": "L2-敏感内容",
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"]
                        })
                        break
                except re.error:
                    pass
    
    return alerts

def inject_warning_chunk(warnings):
    warning_text = f"\n\n⚠️ [安全提醒] 检测到可能存在风险的操作建议：{', '.join(warnings)}"
    return f"data: {json.dumps({'choices': [{'delta': {'content': warning_text}}]})}"

def quick_check(text, keywords):
    """快速检测流式内容中的关键风险词"""
    found=[]
    for kw in keywords:
        if kw in text:
            found.append(kw)
    return found


def process_sse_stream(response_data, rules, request_id):
    """
    处理 SSE 流式响应，逐块检测内容
    
    Args:
        response_data: 原始响应数据 (bytes)
        rules: 内容检测规则
        request_id: 请求 ID
    
    Returns:
        processed_data: 处理后的响应数据 (bytes)
        blocked: 是否被阻断
    """
    accumulated_content = ""
    blocked = False
    processed_lines = []
    
    # 按行解析 SSE
    lines = response_data.decode('utf-8', errors='replace').split('\n')
    
    for line in lines:
        if line.startswith('data: '):
            data_str = line[6:]  # 去掉 "data: " 前缀
            
            if data_str == '[DONE]':
                processed_lines.append(line)
                continue
            
            try:
                data_json = json.loads(data_str)
                choices = data_json.get("choices", [])
                
                if choices:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content", "") or ""
                    reasoning_content = delta.get("reasoning_content", "") or ""
                    if content or reasoning_content:
                        # 累积内容（包含 reasoning_content）
                        accumulated_content += content + reasoning_content
                        if len(accumulated_content) >= 100:  # 每100字符检测一次
                           quick_alerts = quick_check(accumulated_content, QUICK_CHECK_KEYWORDS)
                           if quick_alerts:
                               # 注入警告 chunk
                               accumulated_content = ""  # 重置
                               warning_chunk = inject_warning_chunk(quick_alerts)
                               processed_lines.append(warning_chunk)
                              
                        # 检测累积内容
                        alerts = check_content(accumulated_content, rules)
                        critical = [a for a in alerts if a["severity"] == "critical"]
                        
                        if critical:
                            # 发现违规，阻断
                            print(f"[{request_id}] 🔴 流式响应阻断：发现 {len(critical)} 个严重告警")
                            blocked = True
                            stats.increment("blocked")
                            # 返回错误信息
                            error_response = {
                                "error": "内容安全审核未通过",
                                "alerts": [{k: v for k, v in a.items() if k != "patterns"} for a in critical],
                                "blocked": blocked,
                                "request_id": request_id
                            }
                            return json.dumps(error_response, ensure_ascii=False).encode('utf-8'), True
                    
                    processed_lines.append(line)
            except json.JSONDecodeError:
                processed_lines.append(line)
        else:
            processed_lines.append(line)
    
    # 重新组装 SSE 响应
    processed_data = '\n'.join(processed_lines).encode('utf-8')
    return processed_data, blocked


# 使用默认的 ThreadingMixIn，不自定义线程处理
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """多线程 HTTP 服务器"""
    daemon_threads = True
    allow_reuse_address = True
    block_on_close = False  # 防止关闭时死锁


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    timeout = 10  # 请求处理超时（防止连接挂起）
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")
    
    def _send_json_response(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)
    
    def _read_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > MAX_BODY_SIZE:
            raise ValueError(f"请求体过大: {content_length} > {MAX_BODY_SIZE}")
        
        if content_length == 0:
            return b''
        
        return self.rfile.read(content_length)
    
    def _forward_request(self, target_url, request_body, request_headers):
        headers = {
            'Content-Type': request_headers.get('Content-Type', 'application/json'),
            'User-Agent': 'OpenClaw-LLM-Proxy/3.1',
        }
        for header in ['Authorization', 'X-Api-Key', 'Api-Key', 'HTTP-Referer', 'X-Title']:
            if header in request_headers:
                headers[header] = request_headers[header]
        
        req = Request(target_url, data=request_body, headers=headers, method='POST')
        
        with urlopen(req, timeout=READ_TIMEOUT) as response:
            return response.read(), response.status
    
    def do_POST(self):
        request_id = str(uuid.uuid4())[:8]
        stats.increment("total_requests")
        start_time = time.time()
        
        # 解析 provider
        path = self.path
        provider = None
        target_base = None
        
        for prefix, base_url in PROVIDERS.items():
            if path.startswith(prefix):
                provider = prefix.lstrip("/")
                target_base = base_url
                path = path[len(prefix):] or "/"
                break
        
        if not target_base:
            self._send_json_response(404, {"error": f"Unknown provider: {self.path}"})
            return
        
        # 读取请求体
        try:
            request_body = self._read_request_body()
        except ValueError as e:
            self._send_json_response(413, {"error": str(e)})
            return
        except Exception as e:
            self._send_json_response(400, {"error": f"读取请求体失败: {e}"})
            return
        
        # 转发请求
        target_url = target_base.rstrip('/') + path
        alerts = []
        response_data = None
        status = 500
        # 检测是否是流式请求
        is_streaming = False
        try:
            req_json = json.loads(request_body)
            is_streaming = req_json.get("stream", False)
        except:
            pass  # 非 JSON 请求体，忽略

        try:
            response_data, status = self._forward_request(target_url, request_body, self.headers)
            
            # 流式请求：逐块检测内容
            if is_streaming:
                processed_data, blocked = process_sse_stream(response_data, RULES, request_id)
                if blocked:
                  stats.increment("blocked")
                  # self._send_json_response(403, json.loads(processed_data))
               

            # 检查响应内容（仅 JSON）- 阻断逻辑
            try:
                resp_json = json.loads(response_data)
                choices = resp_json.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    alerts = check_content(content, RULES)
                    if alerts:
                        critical = [a for a in alerts if a["severity"] == "critical"]
                        if critical:
                            stats.increment("blocked")
                            print(f"[{request_id}] 🔴 发现 {len(critical)} 个严重告警，阻断响应!")
                            # 阻断响应：返回安全错误而非原始内容
                            blocked_response = {
                                "error": "内容安全审核未通过",
                                "alerts": [{k: v for k, v in a.items() if k != "patterns"} for a in critical],
                                "blocked": True,
                                "request_id": request_id
                            }
                            response_data = json.dumps(blocked_response, ensure_ascii=False).encode("utf-8")
                            status = 403
                        else:
                            stats.increment("warnings")
                            print(f"[{request_id}] ⚠️ 发现 {len(alerts)} 个警告")
            except (json.JSONDecodeError, KeyError):
                pass
            
            stats.increment("total_responses")
            
            # 返回响应
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(response_data))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(response_data)
            
        except HTTPError as e:
            status = e.code
            stats.increment("errors")
            print(f"[{request_id}] ❌ HTTP {e.code}: {e.reason}")
            self._send_json_response(status, {"error": f"上游错误: {e.reason}", "status": status})
            
        except URLError as e:
            status = 502
            stats.increment("errors")
            print(f"[{request_id}] ❌ 连接失败: {e.reason}")
            self._send_json_response(502, {"error": f"连接失败: {e.reason}"})
            
        except socket.timeout:
            status = 504
            stats.increment("errors")
            print(f"[{request_id}] ❌ 请求超时 ({READ_TIMEOUT}s)")
            self._send_json_response(504, {"error": "请求超时"})
            
        except Exception as e:
            status = 500
            stats.increment("errors")
            print(f"[{request_id}] ❌ 内部错误: {e}")
            traceback.print_exc()
            try:
                self._send_json_response(500, {"error": "内部服务器错误"})
            except:
                pass
        
        # 记录日志 - 脱敏版本
        duration_ms = int((time.time() - start_time) * 1000)
        
        # 脱敏处理：不记录敏感头部和完整响应内容
        # 敏感头部列表
        sensitive_headers = ['Authorization', 'X-Api-Key', 'Api-Key', 'HTTP-Referer', 'X-Title']
        request_headers_safe = {k: ('***REDACTED***' if k in sensitive_headers else v) 
                                 for k, v in dict(self.headers).items()}
        
        # 响应预览脱敏：仅记录前100字符，且替换可能的敏感信息
        response_preview = None
        if response_data:
            try:
                resp_json = json.loads(response_data)
                choices = resp_json.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    # 脱敏：截取前100字符，替换可能的密钥/token
                    preview = content[:100]
                    # 正则替换可能的敏感信息
                    import re
                    preview = re.sub(r'(sk-[a-zA-Z0-9]{20,})', 'sk-***REDACTED***', preview)
                    preview = re.sub(r'(Bearer\s+[a-zA-Z0-9_-]{20,})', 'Bearer ***REDACTED***', preview)
                    preview = re.sub(r'([a-zA-Z0-9]{32,})', '***HASH***', preview)
                    response_preview = preview + ("..." if len(content) > 100 else "")
            except:
                response_preview = f"[{len(response_data)} bytes, content redacted]"
        
        log_writer.write({
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "provider": provider,
            "path": path,
            "status": status,
            "duration_ms": duration_ms,
            "alerts": alerts,
            "request_size": len(request_body),
            "response_size": len(response_data) if response_data else 0,
            "response_preview": response_preview,
            # 不记录敏感头部
            # "headers": request_headers_safe  # 可选：需要时取消注释
        })

    def do_GET(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DEBUG] do_GET called: {self.path}", flush=True)
        if self.path == "/health":
            self._send_json_response(200, {
                "status": "ok",
                "stats": stats.to_dict(),
                "uptime": int(time.time() - stats.get("start_time")),
                "rules_loaded": {
                    "layer1": len(RULES.get("layer1_malicious", {}).get("rules", [])),
                    "layer2": len(RULES.get("layer2_sensitive", {}).get("rules", [])),
                    "layer3": RULES.get("layer3_llm_review", {}).get("enabled", False),
                    "whitelist": len(RULES.get("whitelist", []))
                },
                "max_threads": MAX_THREADS,
                "active_threads": threading.active_count()
            })
        elif self.path == "/stats":
            self._send_json_response(200, stats.to_dict())
        else:
            self._send_json_response(404, {"error": "Not found"})


def print_banner():
    rules_count = len(RULES.get("layer1_malicious", {}).get("rules", [])) + \
                  len(RULES.get("layer2_sensitive", {}).get("rules", []))
    print(f"""
╔══════════════════════════════════════════════════════╗
║  🔒 LLM Proxy v3.4 (多线程 + 线程安全)               ║
║       协作者邮箱：39486006@qq.com
╠══════════════════════════════════════════════════════╣
║  Port: {PROXY_PORT:<42}║
║  Rules: {rules_count} rules loaded{' ' * (30 - len(str(rules_count)))}║
║  Timeout: {READ_TIMEOUT}s{' ' * 34}║
║  Max Body: {MAX_BODY_SIZE // 1024 // 1024}MB{' ' * 35}║
║  Max Threads: {MAX_THREADS}{' ' * 33}║
╠══════════════════════════════════════════════════════╣
║  Health: http://{LISTEN_HOST}:{PROXY_PORT}/health{' ' * 17}║
║  Stats:  http://{LISTEN_HOST}:{PROXY_PORT}/stats{' ' * 18}║
╚══════════════════════════════════════════════════════╝
""")


def signal_handler(signum, frame):
    """优雅关闭：处理 SIGINT/SIGTERM"""
    sig_name = signal.Signals(signum).name
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛑 收到 {sig_name} 信号，正在关闭...")
    
    if server_instance:
        # 停止接受新连接
        server_instance.shutdown()
    
    shutdown_event.set()


def debug_signal_handler(signum, frame):
    """SIGUSR1: 输出所有线程堆栈用于调试"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔍 调试信息 - 活跃线程: {threading.active_count()}", flush=True)
    for thread in threading.enumerate():
        print(f"  线程: {thread.name} (daemon={thread.daemon})", flush=True)
    import traceback
    print("\n主线程堆栈:", flush=True)
    traceback.print_stack(frame)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 调试信息结束\n", flush=True)


def wait_for_network(max_wait=10):
    """启动时检查本地端口是否可用（不探测外部网络）"""
    # 仅检测本地 socket 绑定能力，不连接外部站点
    # 避免泄露启动信息到第三方服务器
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ 检查本地端口可用性...")
    try:
        # 尝试绑定一个临时端口来验证网络栈可用
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2)
        test_socket.bind(('127.0.0.1', 0))  # 绑定随机端口
        test_socket.close()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 本地网络栈就绪")
        return True
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ 本地网络检查失败: {e}")
        return False


def main():
    global server_instance

    print_banner()

    # 启动前检查网络
    wait_for_network(30)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGUSR1, debug_signal_handler)  # 调试用
    
    try:
        server_instance = ThreadingHTTPServer((LISTEN_HOST, PROXY_PORT), ProxyHandler)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 代理服务启动 (PID: {os.getpid()})")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 多线程模式 | 最大线程: {MAX_THREADS} | 超时: {READ_TIMEOUT}s")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 按 Ctrl+C 停止\n")
        
        # serve_forever 会阻塞，直到 shutdown() 被调用
        server_instance.serve_forever()
        
    except OSError as e:
        if e.errno == 48:
            print(f"[ERROR] 端口 {PROXY_PORT} 已被占用")
            print("[TIP] 运行: lsof -i :{PROXY_PORT} 然后 kill <PID>")
        else:
            print(f"[ERROR] 启动失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 启动失败: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        s = stats.to_dict()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 代理服务已停止")
        print(f"[统计] 请求: {s['total_requests']}, 响应: {s['total_responses']}, 错误: {s['errors']}, 告警: {s['blocked'] + s['warnings']}")


if __name__ == "__main__":
    main()
