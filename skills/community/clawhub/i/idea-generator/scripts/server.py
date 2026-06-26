#!/usr/bin/env python3
"""冲击波营销创意生成系统 - API Server"""
import http.server, socketserver, os, json, time, urllib.request, subprocess, threading
from pathlib import Path

DIR = os.path.dirname(__file__) or "."
STATE_FILE = os.path.join(DIR, "state.json")
PORT_FILE = os.path.join(DIR, ".server_port")
TRIGGER_FILE = os.path.join(DIR, ".trigger_agent")

def _load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f: return json.load(f)
    return _default()

def _default():
    return {"status":"idle","topic":"","demand":"","rounds_count":3,"current_round":-1,"phase":"待机","progress":{"qualified":0,"pool":[]},"rounds":[],"logs":[],"latest":"—"}

def _save(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f: json.dump(state, f, ensure_ascii=False, indent=2)

def _notify():
    try:
        if os.path.exists(PORT_FILE):
            port = open(PORT_FILE).read().strip()
            urllib.request.urlopen(urllib.request.Request(f"http://localhost:{port}/notify", headers={"Cache-Control":"no-cache"}), timeout=1)
    except: pass

def api_reset(data=None):
    _save(_default())
    return _default()

def api_init(data):
    s=_default()
    s.update({"status":"running","topic":data.get("topic",""),"demand":data.get("demand",""),"rounds_count":int(data.get("rounds",3)),"phase":"就绪，待开始"})
    _save(s)
    return s

def api_start_round(data):
    s=_load()
    # 🔧 容错：人类习惯 round=1 表示第1轮，自动转换为数组索引 0
    rn_raw = int(data.get("round", 0))
    # 如果 round >= 1 且 rounds 数组为空或只有 null，说明是人类习惯编号，需要转换
    if rn_raw >= 1 and (len(s["rounds"]) == 0 or all(r is None for r in s["rounds"])):
        rn = rn_raw - 1  # 转换：round=1 → 索引0，round=2 → 索引1
    else:
        rn = rn_raw  # 已经是正确的索引
    rnd={"round":rn,"theme":data.get("theme",""),"demand":data.get("demand",""),"status":"in_progress","thinking":None,"searches":[],"insights":[],"ideas":[],"evaluation":None,"feedback":None,"timestamp":time.strftime("%H:%M:%S")}
    while len(s["rounds"])<=rn: s["rounds"].append(None)
    s["rounds"][rn]=rnd
    s["current_round"]=rn
    s["phase"]=f"第{rn+1}轮进行中"
    _save(s)
    return s

def api_log_thinking(data):
    s=_load()
    rn=int(data["round"])
    if rn<len(s["rounds"]) and s["rounds"][rn]:
        s["rounds"][rn]["thinking"]={"content":data.get("content",""),"time":time.strftime("%H:%M:%S")}
    _save(s)
    return s

def api_log_search(data):
    s=_load()
    rn=int(data["round"])
    if rn<len(s["rounds"]) and s["rounds"][rn]:
        search_record={
            "kw":data.get("kw",""),
            "findings":data.get("findings",""),
            "raw_content":data.get("raw_content",""),  # 原始搜索内容
            "source_url":data.get("source_url",""),    # 搜索来源URL
            "platform":data.get("platform",""),        # 搜索平台
            "time":time.strftime("%H:%M:%S")
        }
        s["rounds"][rn]["searches"].append(search_record)
    _save(s)
    return s

def api_log_insight(data):
    s=_load()
    rn=int(data["round"])
    if rn<len(s["rounds"]) and s["rounds"][rn]:
        s["rounds"][rn]["insights"].append({"title":data.get("title",""),"content":data.get("content",""),"time":time.strftime("%H:%M:%S")})
    _save(s)
    return s

def api_add_candidates(data):
    s=_load()
    rn=int(data["round"])
    ideas=data.get("ideas",[])
    if rn<len(s["rounds"]) and s["rounds"][rn]:
        for idea in ideas: idea["status"]="pending"
        s["rounds"][rn]["ideas"]=ideas
    _save(s)
    return s

def api_validate_search(data=None):
    """验证搜索结果是否真实"""
    import subprocess
    try:
        result = subprocess.run(
            ["python3", os.path.join(DIR, "search_validator.py"), "check"],
            capture_output=True, text=True, timeout=5
        )
        return {
            "valid": result.returncode == 0,
            "message": result.stdout.strip() or result.stderr.strip()
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def api_evaluate_round(data):
    s=_load()
    # 🔧 容错：自动修正 round 参数（同 api_start_round）
    rn_raw = int(data.get("round", 0))
    if rn_raw >= 1 and (len(s["rounds"]) == 0 or all(r is None for r in s["rounds"])):
        rn = rn_raw - 1
    else:
        rn = rn_raw
    evals=data.get("evaluations",[])
    if rn<len(s["rounds"]) and s["rounds"][rn]:
        rnd=s["rounds"][rn]
        
        # 🔴 强制搜索验证：如果搜索结果无效，拒绝评分
        # 但先检查是否有搜索记录，如果没有则跳过验证
        has_searches = len(rnd.get("searches", [])) > 0
        if has_searches:
            search_validation = api_validate_search()
            if not search_validation.get("valid"):
                return {"error": "搜索验证失败，请重新执行真实搜索", "details": search_validation}
        else:
            # 如果没有搜索记录，记录警告但允许继续
            print(f"⚠️ 第{rn}轮没有搜索记录，跳过搜索验证")
        
        passed,rejected=[],[]
        for i, ev in enumerate(evals):
            # 支持两种格式：idx(索引) 或 idea(名称)
            idx = int(ev.get("idx", i))  # 默认使用当前索引
            idea_name = ev.get("idea", "")
            
            # 如果提供了名称，尝试匹配
            if idea_name:
                for j, idea in enumerate(rnd["ideas"]):
                    if idea.get("创意") == idea_name:
                        idx = j
                        break
            
            if 0<=idx<len(rnd["ideas"]):
                idea=rnd["ideas"][idx]
                # 🔧 容错：支持多种评分字段名
                # total, score, 总分, 分数, score_total
                total = ev.get("total") or ev.get("score") or ev.get("总分") or ev.get("分数") or ev.get("score_total") or 0
                total = int(total) if total else 0
                qualified=total>=90  # 直接用分数判断
                # 🔧 容错：支持多种维度字段名
                dims = ev.get("dimensions") or ev.get("dims") or ev.get("维度") or ev.get("评分维度") or {}
                idea.update({"status":"qualified" if qualified else "rejected","total":total,"feedback":ev.get("feedback",""),"dims":dims})
                (passed if qualified else rejected).append(idea)
        rnd["evaluation"]={"passed":passed,"rejected":rejected,"avg_score":round(sum(int(ev.get("total") or ev.get("score") or ev.get("总分") or 0) for ev in evals)/len(evals),1) if evals else 0,"timestamp":time.strftime("%H:%M:%S")}
        rnd["status"]="done"
        for idea in passed:
            if not any(p.get("创意")==idea.get("创意") for p in s["progress"]["pool"]):
                s["progress"]["pool"].append(idea)
        s["progress"]["qualified"]=len(s["progress"]["pool"])
    _save(s)
    return s

def api_log_feedback(data):
    s=_load()
    rn=int(data["round"])
    if rn<len(s["rounds"]) and s["rounds"][rn]:
        s["rounds"][rn]["feedback"]={"content":data.get("content",""),"time":time.strftime("%H:%M:%S")}
    _save(s)
    return s

def api_update_phase(data):
    s=_load()
    s["phase"]=data.get("phase","")
    _save(s)
    return s

def api_done(data=None):
    s=_load()
    s.update({"status":"done","phase":"完成"})
    _save(s)
    return s

def api_stop(data=None):
    """停止当前任务 - 强制终止 isolated agent session"""
    s = _load()
    cron_job_id = s.get("cron_job_id", "")
    session_id = s.get("session_id", "")  # e.g. idea-gen-xxxxxxxxxxxx

    # 1. 更新状态文件（AI 每步检查此状态，立即门控）
    s.update({"status": "stopped", "phase": "已停止"})
    _save(s)

    # 2. 删除触发文件，防止未启动的 agent 误读旧任务
    trigger_file = os.path.join(DIR, ".trigger_agent")
    if os.path.exists(trigger_file):
        os.remove(trigger_file)

    # 3. 删除 cron 任务（防止任务还未启动就被触发）
    if cron_job_id:
        try:
            result = subprocess.run(
                ["openclaw", "cron", "rm", cron_job_id, "--json"],
                capture_output=True, text=True, timeout=5
            )
            print(f"[stop] cron rm {cron_job_id}: returncode={result.returncode}")
        except Exception as e:
            print(f"[stop] cron rm failed: {e}")

    # 4. 强制取消正在运行的 isolated agent 任务
    # openclaw tasks cancel 接受 session key 作为 lookup
    if session_id:
        try:
            result = subprocess.run(
                ["openclaw", "tasks", "cancel", session_id],
                capture_output=True, text=True, timeout=10
            )
            print(f"[stop] tasks cancel {session_id}: returncode={result.returncode} stdout={result.stdout.strip()} stderr={result.stderr.strip()}")
        except Exception as e:
            print(f"[stop] tasks cancel failed: {e}")

    print(f"[stop] 停止完成。session_id={session_id}, cron_job_id={cron_job_id}")
    return s

def api_clear_process(data=None):
    """清空创意过程"""
    s=_load()
    s["rounds"]=[]
    s["current_round"]=-1
    if s["status"]!="running":
        s["status"]="idle"
        s["phase"]="待机"
    _save(s)
    return s

def api_clear_pool(data=None):
    """清空创意池"""
    s=_load()
    s["progress"]={"qualified":0,"pool":[]}
    _save(s)
    return s

def api_remove_idea(data):
    """删除单个创意"""
    s=_load()
    idx=int(data.get("idx", -1))
    pool=s.get("progress",{}).get("pool",[])
    if 0<=idx<len(pool):
        pool.pop(idx)
        s["progress"]["pool"]=pool
        s["progress"]["qualified"]=len(pool)
        _save(s)
    return s

def api_run(data):
    """创建任务并立即启动创意生成"""
    import uuid as _uuid
    topic = data.get("topic", "").strip()
    rounds = int(data.get("rounds", 3))
    demand = data.get("demand", "").strip()

    if not topic:
        return {"error": "请输入创意需求"}

    # 检查是否已有任务在运行
    current = _load()
    if current.get("status") == "running":
        return {"error": "已有任务在执行中，请等待完成或先点停止", "current_topic": current.get("topic", "")}

    # 清除残留的触发文件（防止上次异常中断留下的旧文件）
    if os.path.exists(TRIGGER_FILE):
        os.remove(TRIGGER_FILE)

    # 生成本次任务唯一的 session key（用于在 openclaw 前端创建新对话）
    session_id = f"idea-gen-{_uuid.uuid4().hex[:12]}"
    session_key = f"agent:main:{session_id}"

    # 初始化任务状态（保留历史创意池！只重置运行状态）
    s = _load()
    existing_pool = s.get("progress", {}).get("pool", [])
    s.update({
        "status": "running",
        "topic": topic,
        "demand": demand,
        "rounds_count": rounds,
        "phase": "任务已创建，AI 即将响应...",
        "progress": {"qualified": len(existing_pool), "pool": existing_pool},
        "rounds": [],
        "logs": [{"type": "info", "title": "任务已创建", "content": f"主题：{topic} | {rounds}轮迭代", "time": time.strftime("%H:%M:%S")}],
        "latest": "任务已创建，AI 即将响应...",
        "session_id": session_id,
        "session_key": session_key,
        "cron_job_id": ""  # will be filled after cron add
    })
    _save(s)

    # 写入触发文件
    port_val = open(PORT_FILE).read().strip() if os.path.exists(PORT_FILE) else "50000"
    trigger_data = {
        "topic": topic,
        "rounds": rounds,
        "demand": demand,
        "port": port_val,
        "session_id": session_id,
        "session_key": session_key,
        "time": time.time()
    }
    with open(TRIGGER_FILE, "w", encoding="utf-8") as f:
        json.dump(trigger_data, f, ensure_ascii=False)

    # 🔔 通过 openclaw cron 创建一次性任务，在独立的 isolated session 中运行
    # 注意：--session-key 使用简短 ID（非 agent:main: 前缀）
    wake_ok = False
    try:
        from datetime import datetime, timezone, timedelta
        # 设定 10 秒后执行
        run_at = (datetime.now(timezone.utc) + timedelta(seconds=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        skill_dir = os.path.abspath(os.path.join(DIR, ".."))
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        msg = (
            f"[idea-generator] 创意任务已就绪：{topic}（{rounds}轮），"
            f"请立即读取 SKILL.md 并开始执行创意生成。"
        )
        cron_cmd = [
            "openclaw", "cron", "add",
            "--name", f"idea-gen-{session_id}",
            "--at", run_at,
            "--session", "isolated",
            "--session-key", session_id,
            "--message", msg,
            "--delete-after-run",
            "--json"
        ]
        result = subprocess.run(cron_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            cron_result = json.loads(result.stdout)
            wake_ok = True
            cron_job_id = cron_result.get("id", "")
            # 记录 cron_job_id 到 state，供 stop 时使用
            s2 = _load()
            s2["cron_job_id"] = cron_job_id
            _save(s2)
            print(f"[info] cron 任务创建成功: {cron_job_id}")
        else:
            print(f"[warn] cron add failed: {result.stderr.strip()}")
    except Exception as e:
        print(f"[warn] cron add exception: {e}")

    # 降级方案：如果 cron 失败，从环境变量读取 gateway 配置
    if not wake_ok:
        try:
            gateway_port = os.environ.get("OPENCLAW_GATEWAY_PORT", "18789")
            hook_token = os.environ.get("OPENCLAW_HOOK_TOKEN", "")
            if not hook_token:
                print("[warn] OPENCLAW_HOOK_TOKEN not set, skipping wake hook fallback")
            else:
                wake_payload = json.dumps({
                    "text": f"[idea-generator] 创意任务已就绪：{topic}（{rounds}轮），请立即读取 SKILL.md 并开始执行创意生成。",
                    "mode": "now"
                }).encode("utf-8")
                req = urllib.request.Request(
                    f"http://127.0.0.1:{gateway_port}/hooks/wake",
                    data=wake_payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {hook_token}"
                    },
                    method="POST"
                )
                resp = urllib.request.urlopen(req, timeout=3)
                wake_ok = resp.status == 200
                print(f"[info] wake hook fallback: ok={wake_ok}")
        except Exception as e2:
            print(f"[warn] wake hook also failed: {e2}")

    return {
        "ok": True,
        "topic": topic,
        "rounds": rounds,
        "wake": wake_ok,
        "session_id": session_id,
        "msg": "任务已创建！AI 正在新对话中响应..." if wake_ok else "任务已创建！等待 AI 响应。",
        "ready": True
    }

class Handler(http.server.BaseHTTPRequestHandler):
    def send_json(self, data, code=200):
        p = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(p))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(p)

    def read_json(self):
        clen = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(clen).decode("utf-8")) if clen else {}

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/state.json":
            try:
                data = open(STATE_FILE).read()
            except:
                data = "{}"
            p = data.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(p))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(p)
        elif path == "/notify":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            fp = os.path.join(DIR, path.lstrip("/") or "live-dashboard.html")
            if os.path.isfile(fp):
                with open(fp, "rb") as f:
                    d = f.read()
                ext = os.path.splitext(fp)[1].lower()
                ct = {".html": "text/html; charset=utf-8", ".js": "application/javascript", ".css": "text/css", ".json": "application/json", ".png": "image/png", ".ico": "image/x-icon"}.get(ext, "application/octet-stream")
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", len(d))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(d)
            else:
                self.send_error(404)

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            data = self.read_json()
        except:
            data = {}
        routes = {
            "/reset": (200, api_reset),
            "/init": (200, api_init),
            "/run": (200, api_run),
            "/stop": (200, api_stop),
            "/clear/process": (200, api_clear_process),
            "/clear/pool": (200, api_clear_pool),
            "/idea/remove": (200, api_remove_idea),
            "/round/start": (200, api_start_round),
            "/round/feedback": (200, api_log_feedback),
            "/log/thinking": (200, api_log_thinking),
            "/log/search": (200, api_log_search),
            "/log/insight": (200, api_log_insight),
            "/idea/add": (200, api_add_candidates),
            "/idea/evaluate": (200, api_evaluate_round),
            "/search/validate": (200, api_validate_search),
            "/phase": (200, api_update_phase),
            "/done": (200, api_done)
        }
        if path in routes:
            self.send_json(routes[path][1](data), routes[path][0])
        elif path == "/shutdown":
            self.send_json({"ok": True})
            self.wfile.flush()
            def _e():
                time.sleep(0.3)
                os._exit(0)
            threading.Thread(target=_e, daemon=True).start()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, *a): pass

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    port = int(open(PORT_FILE).read().strip()) if os.path.exists(PORT_FILE) else 50000
    # 启动时：如果上次状态是 running（意外重启/崩溃），自动重置为 stopped，避免前端卡住
    try:
        s = _load()
        if s.get("status") == "running":
            s["status"] = "stopped"
            s["phase"] = "服务重启，任务已中断"
            _save(s)
            print("[startup] 检测到上次任务未完成，已重置为 stopped 状态")
    except Exception as e:
        print(f"[startup] 状态检查失败: {e}")
    # 清除残留的触发文件
    if os.path.exists(TRIGGER_FILE):
        os.remove(TRIGGER_FILE)
        print("[startup] 清除残留 .trigger_agent 文件")
    with socketserver.ThreadingTCPServer(("", port), Handler) as httpd:
        if not os.path.exists(PORT_FILE):
            port = httpd.server_address[1]
            with open(PORT_FILE, "w") as f:
                f.write(str(port))
        print(f"Port: {port}")
        print(f"Dashboard: http://localhost:{port}/live-dashboard.html")
        httpd.serve_forever()
