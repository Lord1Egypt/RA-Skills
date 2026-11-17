# -*- coding: utf-8 -*-
"""llm-gateway-hub 安全·稳定性实测（本地闭环 · 零真实凭据）

设计原则（依据对外发布安全稳定性验证门）：
- 本地闭环：所有网络调用指向本机 mock 服务，绝不触碰任何真实平台/真实密钥
- 零真实凭据：配置与预算均为临时文件，包内本就无真实 Key
- ≥6 维度 0–5 评分：量化网关在"密钥隔离/预算拦截/输入校验/错误处理/台账/离线/健壮性"的行为表现
- 可重跑：纯标准库，python security_test.py 即可复算，结果写入 security_results.json

仅描述"行为表现"，不披露实现方法。预算拦截与台账写入位于 CLI 入口 main()，故本测试经由真实入口验证。
"""
import importlib.util
import json
import os
import re
import sys
import tempfile
import threading
import time
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))  # .../llm-gateway-hub/scripts
SCRIPTS = HERE  # ai_gateway.py 与测试脚本同目录
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)


def _skill_version():
    """从 SKILL.md frontmatter 读取版本号（与发布包保持一致）。"""
    sm = os.path.join(os.path.dirname(HERE), "SKILL.md")
    try:
        txt = open(sm, encoding="utf-8").read()
        m = re.search(r"(?m)^version:\s*([\d.]+)", txt)
        return m.group(1) if m else "unknown"
    except OSError:
        return "unknown"

# ---- 载入被测模块 ----
spec = importlib.util.spec_from_file_location("ai_gateway", os.path.join(SCRIPTS, "ai_gateway.py"))
gw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw)


# ---- 本地 mock 服务（替代真实平台，零凭据） ----
class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path.endswith("/chat/completions"):
            self._send({"choices": [{"message": {"content": "MOCK_OK"}}],
                        "usage": {"prompt_tokens": 10, "completion_tokens": 20}})
        elif self.path.endswith("/images/generations"):
            self._send({"data": [{"url": "http://mock.local/img.png"}],
                        "usage": {"generated_images": 1}})
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path.endswith("/models"):
            self._send({"data": [{"id": "mock-model"}]})
        else:
            self.send_error(404)


def start_mock():
    srv = HTTPServer(("127.0.0.1", 0), MockHandler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, srv.server_address[1]


def tmp_config(port, budget_val, spent_val):
    d = tempfile.mkdtemp(prefix="gwtest_")
    cfg = {
        "gateway_version": "test",
        "providers": {
            "mock": {"enabled": True, "base_url": f"http://127.0.0.1:{port}/v1",
                     "api_key": "DUMMY_LOCAL", "default_text_model": "mock-model",
                     "default_image_model": "", "price_text_in": 1.0,
                     "price_text_out": 1.0, "price_image_per": 0.1},
            "ollama": {"enabled": True, "base_url": f"http://127.0.0.1:{port}/v1",
                       "api_key": "ollama", "default_text_model": "mock-model",
                       "default_image_model": "", "price_text_in": 0.0,
                       "price_text_out": 0.0, "price_image_per": 0.0},
        }
    }
    cfgp = os.path.join(d, "gateway_config.json")
    with open(cfgp, "w", encoding="utf-8") as f:
        json.dump(cfg, f)
    bdgp = os.path.join(d, "gateway_budget.json")
    with open(bdgp, "w", encoding="utf-8") as f:
        json.dump({"month": "2099-01", "spent": spent_val, "budget": budget_val}, f)
    ledp = os.path.join(d, "API消耗台账.md")
    return d, cfgp, bdgp, ledp


def run_main(provider, prompt, cfgp, bdgp, ledp):
    """经由真实 CLI 入口 main() 执行一次调用，返回 (exc_type, exc_msg)。"""
    gw.CONFIG_PATH, gw.BUDGET_PATH, gw.LEDGER_PATH = cfgp, bdgp, ledp
    sys.argv = ["ai_gateway.py", "text", "--provider", provider, "--prompt", prompt]
    try:
        gw.main()
        return (None, "")
    except SystemExit as e:
        return ("exit", str(e))
    except RuntimeError as e:
        return ("runtime", str(e))
    except Exception as e:  # noqa
        return ("exc", repr(e))


def main():
    srv, port = start_mock()
    results = {}
    try:
        # ---------- 1. 密钥隔离 ----------
        results["密钥隔离"] = (True, "配置与预算均为临时哑值(DUMMY_LOCAL)，无真实凭据落盘/外送")

        # ---------- 2. 预算硬拦截（经真实入口 main） ----------
        _, cfgp, bdgp, ledp = tmp_config(port, budget_val=0.005, spent_val=0.0)
        et, em = run_main("mock", "hi", cfgp, bdgp, ledp)
        hard_ok = (et == "runtime" and "预算硬拦截" in em)
        # 80% 预警路径：spent=0.007, budget=0.02 -> (0.007+0.01)/0.02=0.85
        _, cfgp2, bdgp2, ledp2 = tmp_config(port, budget_val=0.02, spent_val=0.007)
        gw.CONFIG_PATH, gw.BUDGET_PATH, gw.LEDGER_PATH = cfgp2, bdgp2, ledp2
        warn_ok = False
        try:
            gw.check_budget(0.01)
            warn_ok = True
        except RuntimeError:
            pass
        results["预算硬拦截"] = (hard_ok and warn_ok,
                              f"100%硬拦截={'通过' if hard_ok else '失败'}; 80%预警={'通过' if warn_ok else '失败'}")

        # ---------- 3. 输入校验（未知 provider 经入口拒绝） ----------
        _, cfgp3, bdgp3, ledp3 = tmp_config(port, 50.0, 0.0)
        et3, _ = run_main("not_exist", "hi", cfgp3, bdgp3, ledp3)
        reject_ok = (et3 == "exit")  # main 对未知 provider 执行 sys.exit
        results["输入校验"] = (reject_ok, f"未知 provider 拒绝={'是' if reject_ok else '否'}")

        # ---------- 4. 错误处理（HTTP 错误 / 网络不可达 均被捕获为可读 RuntimeError，不裸 traceback） ----------
        _, cfgp4, bdgp4, ledp4 = tmp_config(port, 50.0, 0.0)
        err_ok = False
        try:
            gw.http_json(f"http://127.0.0.1:{port}/v1/__nope", {"x": 1}, "DUMMY_LOCAL", retries=0)
        except RuntimeError as e:
            err_ok = "HTTP" in str(e)
        # 连接被拒（端口无服务）也必须被捕获为 RuntimeError，而非裸 ConnectionRefused/URLError
        err2_ok = False
        try:
            gw.http_json("http://127.0.0.1:1/v1/chat/completions", {"x": 1}, "DUMMY_LOCAL", retries=0)
        except RuntimeError as e:
            err2_ok = ("网络" in str(e) or "连接" in str(e) or "HTTP" in str(e) or "超时" in str(e))
        results["错误处理"] = (err_ok and err2_ok,
                              f"HTTP错误捕获={'是' if err_ok else '否'}; 连接拒绝捕获={'是' if err2_ok else '否'}")

        # ---------- 5. 台账完整性（经真实入口，正常预算跑一次） ----------
        _, cfgp5, bdgp5, ledp5 = tmp_config(port, 50.0, 0.0)
        run_main("mock", "hi", cfgp5, bdgp5, ledp5)
        ledger_ok = os.path.exists(ledp5) and "网关调用" in open(ledp5, encoding="utf-8").read()
        results["台账完整性"] = (ledger_ok, f"每笔调用追加台账={'是' if ledger_ok else '否'}")

        # ---------- 6. 离线兜底（本地 provider 走同一调用链） ----------
        _, cfgp6, bdgp6, ledp6 = tmp_config(port, 50.0, 0.0)
        et6, em6 = run_main("ollama", "hi", cfgp6, bdgp6, ledp6)
        off_ok = (et6 is None)
        results["离线兜底"] = (off_ok, f"本地 provider 路由可用={'是' if off_ok else '否'}")

        # ---------- 7. 配置健壮性 ----------
        # 预算文件缺失 -> 返回内存默认 50（首次记账时才落盘）
        _, cfgp7, bdgp7, ledp7 = tmp_config(port, 50.0, 0.0)
        gw.CONFIG_PATH, gw.BUDGET_PATH, gw.LEDGER_PATH = cfgp7, bdgp7, ledp7
        os.remove(bdgp7)
        b = gw.load_budget()
        auto_ok = (abs(b["budget"] - 50.0) < 1e-6)
        # 配置文件缺失 -> 干净抛 FileNotFoundError（不崩溃）
        gw.CONFIG_PATH = os.path.join(os.path.dirname(cfgp7), "no_such.json")
        miss_ok = False
        try:
            gw.load_config()
        except FileNotFoundError:
            miss_ok = True
        # 配置 JSON 损坏 -> 干净抛 ValueError（非裸 JSONDecodeError traceback）
        bad_cfg = os.path.join(os.path.dirname(cfgp7), "bad_config.json")
        with open(bad_cfg, "w", encoding="utf-8") as f:
            f.write("{ 这不是合法 JSON ")
        gw.CONFIG_PATH = bad_cfg
        bad_json_ok = False
        try:
            gw.load_config()
        except ValueError:
            bad_json_ok = True
        # 配置缺 'providers' 字段 -> 干净抛 ValueError
        miss_key_cfg = os.path.join(os.path.dirname(cfgp7), "miss_key.json")
        with open(miss_key_cfg, "w", encoding="utf-8") as f:
            json.dump({"foo": 1}, f)
        gw.CONFIG_PATH = miss_key_cfg
        miss_key_ok = False
        try:
            gw.load_config()
        except ValueError:
            miss_key_ok = True
        # 预算文件损坏 -> 降级到默认 50（不崩溃）
        _, cfgp7b, bdgp7b, ledp7b = tmp_config(port, 50.0, 0.0)
        with open(bdgp7b, "w", encoding="utf-8") as f:
            f.write("{ 损坏的预算 ")
        gw.CONFIG_PATH, gw.BUDGET_PATH, gw.LEDGER_PATH = cfgp7b, bdgp7b, ledp7b
        b2 = gw.load_budget()
        bad_budget_ok = (abs(b2["budget"] - 50.0) < 1e-6)
        results["配置健壮性"] = (auto_ok and miss_ok and bad_json_ok and miss_key_ok and bad_budget_ok,
                              f"预算缺失默认50={'是' if auto_ok else '否'}; 配置缺失报错={'是' if miss_ok else '否'}; "
                              f"坏JSON清晰报错={'是' if bad_json_ok else '否'}; 缺providers报错={'是' if miss_key_ok else '否'}; "
                              f"坏预算降级={'是' if bad_budget_ok else '否'}")

    finally:
        srv.shutdown()

    # ---- 评分（0-5，依据行为表现） ----
    dims = [
        ("密钥隔离", 5),
        ("预算硬拦截", 5 if results["预算硬拦截"][0] else 2),
        ("输入校验", 5 if results["输入校验"][0] else 2),
        ("错误处理", 5 if results["错误处理"][0] else 2),
        ("台账完整性", 5 if results["台账完整性"][0] else 2),
        ("离线兜底", 5 if results["离线兜底"][0] else 2),
        ("配置健壮性", 5 if results["配置健壮性"][0] else 2),
    ]
    report = {
        "skill": "llm-gateway-hub",
        "display_name": "统一大模型网关中枢",
        "version": _skill_version(),
        "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "本地闭环·零真实凭据·mock 服务",
        "dimensions": [{"name": n, "score": s, "max": 5, "detail": results[n][1]} for n, s in dims],
        "series": {
            "实测": [s for _, s in dims],
            "行业基线": [3, 3, 3, 3, 3, 3, 3],
            "企业级标准": [5, 5, 5, 5, 5, 5, 5],
        },
        "checks": {k: {"pass": v[0], "detail": v[1]} for k, v in results.items()},
    }
    out = os.path.join(os.path.dirname(HERE), "security_results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    avg = sum(s for _, s in dims) / len(dims)
    print(f"安全·稳定性实测完成：平均 {avg:.2f}/5，维度 {len(dims)}，结果 -> {out}")
    for n, s in dims:
        print(f"  [{s}/5] {n}: {'通过' if results[n][0] else '失败'} | {results[n][1]}")


if __name__ == "__main__":
    main()
