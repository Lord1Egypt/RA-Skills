"""model-intel-check 的本地 Web UI（游戏化版）。

流程：主 agent 先与用户对话确定测评配置，写入 run_config.json（页面只读展示，不可更改），
再启动本服务。跑分在本进程后台线程执行（复用 intel_check.py，协议一致），
页面每 2 秒轮询 /api/state 实时刷新——agent 不需要在场。

用法:
    export KIMI_BASE_URL="..." KIMI_API_KEY="..."
    python serve.py --config run_config.json [--port 8899] [--no-browser]
    python serve.py --demo          # 假数据预览页面
"""
import argparse
import json
import os
import sys
import threading
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import intel_check as ic

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "web" / "index.html"

_lock = threading.Lock()
DEMO = False
CONFIG = None
STATE = {
    "status": "idle",          # idle | starting | running | done | failed
    "endpoint_echo": "",
    "total": 0, "done": 0, "ok": 0,
    "started_at": None,
    "items": {},               # "kind#id" -> {status, kind, extracted, finish_reason}
    "summary": {},             # kind -> [ok, n]
    "message": "",
}

DEMO_CONFIG = {
    "model": "kimi-k3",
    "concurrency": 8,
    "no_thinking": False,
    "suites": [
        {"kind": "aime", "name": "AIME 2026", "emoji": "", "count": 30,
         "stars": 5, "ref_pct": 80.0},
        {"kind": "gpqa", "name": "GPQA Diamond", "emoji": "", "count": 50,
         "stars": 4, "ref_pct": 85.7},
    ],
}


def set_state(**kw):
    with _lock:
        STATE.update(kw)


def load_config(path):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    if not cfg.get("suites"):
        sys.exit("run_config.json 里至少要有一个 suite")
    for s in cfg["suites"]:
        s.setdefault("emoji", "👾")
        s.setdefault("stars", 4)
        s.setdefault("ref_pct", None)
    cfg.setdefault("concurrency", 8)
    cfg.setdefault("no_thinking", False)
    if not cfg.get("model"):
        cfg["model"] = os.environ.get("MODEL_NAME", "kimi-k3")
    return cfg


def build_jobs(cfg):
    """按锁定配置构造任务清单: [(key, kind, item, correct_letter)]"""
    jobs = []
    for s in cfg["suites"]:
        if s["kind"] == "aime":
            aime = ic.load_jsonl(ic.DATA / s.get("file", "aime2025.jsonl"))
            for i in ic.parse_indices(s.get("indices", "0-4,20-29")):
                jobs.append((f"aime#{aime[i]['id']}", "aime", aime[i], None))
        elif s["kind"] == "gpqa":
            n = min(int(s.get("count", 50)), 50)
            for it in ic.gpqa_items(ic.load_jsonl(ic.DATA / "gpqa_diamond_50.jsonl"), n):
                jobs.append((f"gpqa#{it['id']}", "gpqa", it, it["correct_letter"]))
    return jobs


def run_benchmark(cfg):
    """后台线程：完整跑一轮，逐题更新 STATE，结果落盘 cwd/results/。"""
    try:
        client = ic.make_client()
        try:  # 预检 + 抓上游回声
            probe = client.chat.completions.create(
                model=cfg["model"], messages=[{"role": "user", "content": "hi"}], max_tokens=1)
            set_state(endpoint_echo=getattr(probe, "model", "") or "")
        except Exception as e:
            set_state(endpoint_echo=f"(预检失败: {e})")

        jobs = build_jobs(cfg)
        thinking = not cfg.get("no_thinking")
        with _lock:
            STATE["items"] = {k: {"status": "pending", "kind": k.split("#")[0]} for k, *_ in jobs}
            STATE.update(status="running", total=len(jobs), done=0, ok=0,
                         started_at=time.time(), summary={}, message="")
        results = []
        with ThreadPoolExecutor(max_workers=cfg["concurrency"]) as ex:
            futs = {ex.submit(ic.run_one, client, cfg["model"], it, kind, cl, thinking): (key, kind, it["id"])
                    for key, kind, it, cl in jobs}
            for fut in as_completed(futs):
                key, kind, iid = futs[fut]
                try:
                    r = fut.result()
                except Exception as e:
                    r = {"kind": kind, "id": iid, "target": None, "extracted": None,
                         "correct": False, "finish_reason": "error", "completion": f"ERROR: {e}"}
                results.append(r)
                with _lock:
                    st = "ok" if r["correct"] else ("error" if r["finish_reason"] != "stop" else "miss")
                    STATE["items"][key] = {"status": st, "kind": kind,
                                           "extracted": r.get("extracted"),
                                           "finish_reason": r.get("finish_reason")}
                    STATE["done"] += 1
                    STATE["ok"] += 1 if r["correct"] else 0

        outdir = Path.cwd() / "results"
        outdir.mkdir(exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        with open(outdir / f"results_{stamp}.jsonl", "w", encoding="utf-8") as f:
            for r in sorted(results, key=lambda x: (x["kind"], str(x["id"]))):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        summary = {}
        for kind in ("aime", "gpqa"):
            sub = [r for r in results if r["kind"] == kind]
            if sub:
                summary[kind] = [sum(r["correct"] for r in sub), len(sub)]
        n_err = sum(1 for r in results if r["finish_reason"] != "stop")
        set_state(status="done", summary=summary,
                  message=f"明细已落盘 results/results_{stamp}.jsonl"
                          + (f"；{n_err} 题传输失败，建议 rerun_failed.py 补跑后再判分" if n_err else ""))
    except Exception as e:
        set_state(status="failed", message=str(e))


def fake_run(cfg):
    """--demo：不发真实请求，模拟打怪过程，仅供预览页面。"""
    import random
    rng = random.Random(2026)
    items = []
    for s in cfg["suites"]:
        items.extend([(f"{s['kind']}#{i}", s["kind"]) for i in range(int(s["count"]))])
    with _lock:
        STATE["items"] = {k: {"status": "pending", "kind": k.split("#")[0]} for k, _ in items}
        STATE.update(status="running", total=len(items), done=0, ok=0,
                     started_at=time.time(), summary={}, message="",
                     endpoint_echo="accounts/fireworks/models/kimi-k3")
    summary = {}
    for key, kind in items:
        time.sleep(rng.uniform(0.4, 1.1))
        roll = rng.random()
        st = "ok" if roll < (0.87 if kind == "aime" else 0.92) else ("error" if roll > 0.985 else "miss")
        with _lock:
            STATE["items"][key] = {"status": st, "kind": kind,
                                   "extracted": "70" if st == "ok" else None,
                                   "finish_reason": "stop" if st != "error" else "error"}
            STATE["done"] += 1
            STATE["ok"] += 1 if st == "ok" else 0
        ok = sum(1 for v in STATE["items"].values() if v["kind"] == kind and v["status"] == "ok")
        n = sum(1 for v in STATE["items"].values() if v["kind"] == kind)
        summary[kind] = [ok, n]
    set_state(status="done", summary=summary, message="全部题目已完成")


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            body = INDEX.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/config":
            cfg = dict(CONFIG)
            self._json({"demo": DEMO, **cfg})
        elif path == "/api/state":
            with _lock:
                s = dict(STATE)
            if s.get("started_at") and s["status"] == "running":
                s["elapsed"] = round(time.time() - s["started_at"], 1)
            self._json(s)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/start":
            return self._json({"error": "not found"}, 404)
        with _lock:
            busy = STATE["status"] == "running"
        if busy:
            return self._json({"error": "已有运行中的测评"}, 409)
        set_state(status="starting", endpoint_echo="", message="",
                  items={}, total=0, done=0, ok=0, summary={}, started_at=None)
        runner = fake_run if DEMO else run_benchmark
        threading.Thread(target=runner, args=(CONFIG,), daemon=True).start()
        self._json({"ok": True})


def main():
    global DEMO, CONFIG
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", help="run_config.json 路径; 缺省读当前目录 ./run_config.json")
    ap.add_argument("--port", type=int, default=8899)
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--demo", action="store_true", help="假数据演示模式，不发真实请求")
    args = ap.parse_args()
    DEMO = args.demo

    cfg_path = args.config or "run_config.json"
    if Path(cfg_path).exists():
        CONFIG = load_config(cfg_path)
    elif DEMO:
        CONFIG = DEMO_CONFIG
    else:
        sys.exit(f"缺少 {cfg_path} —— 请先与用户对话确定测评配置并写入该文件（见 SKILL.md 4b 节）")

    if not DEMO and (not os.environ.get("KIMI_BASE_URL") or not os.environ.get("KIMI_API_KEY")):
        sys.exit("请先 export KIMI_BASE_URL / KIMI_API_KEY 再启动")
    url = f"http://127.0.0.1:{args.port}"
    total = sum(int(s["count"]) for s in CONFIG["suites"] if s.get("count"))
    print(f"配置锁定: {CONFIG['model']} | " +
          " + ".join(f"{s['name']}×{s.get('count','?')}" for s in CONFIG["suites"]) +
          f" | 页面: {url}" + ("  【演示模式】" if DEMO else ""))
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
