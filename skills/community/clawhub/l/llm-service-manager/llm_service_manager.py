"""
llm_service_manager.py — 本地LLM服务管理器
管理 Ollama / vLLM / OpenAI 兼容服务，统一接口
"""
import sys, json, os, subprocess, time, platform
from datetime import datetime


# ── 服务状态检测 ──

def _check_ollama():
    """检测Ollama是否运行"""
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read())
            models = [m["name"] for m in data.get("models", [])]
            return {"running": True, "models": models, "url": "http://localhost:11434"}
    except Exception:
        return {"running": False, "models": [], "url": "http://localhost:11434"}


def _check_vllm():
    """检测vLLM是否运行"""
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:8000/v1/models")
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read())
            models = [m["id"] for m in data.get("data", [])]
            return {"running": True, "models": models, "url": "http://localhost:8000/v1"}
    except Exception:
        return {"running": False, "models": [], "url": "http://localhost:8000/v1"}


def _check_openai():
    """检测兼容的OpenAI API端点"""
    import os as _os
    url = _os.environ.get("OPENAI_BASE_URL", "")
    if not url:
        return {"running": False, "models": [], "url": ""}
    try:
        import urllib.request
        req = urllib.request.Request(f"{url}/models")
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read())
            models = [m["id"] for m in data.get("data", [])]
            return {"running": True, "models": models, "url": url}
    except Exception:
        return {"running": False, "models": [], "url": url}


# ── 模型查询 ──

def _query_ollama(model: str, prompt: str) -> str:
    """向Ollama发送查询"""
    try:
        import urllib.request
        body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}).encode()
        req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            return data.get("message", {}).get("content", str(data))
    except Exception as e:
        return f"[错误] {e}"


def _query_api(url: str, model: str, prompt: str, api_key: str = "") -> str:
    """向OpenAI兼容API发送查询"""
    try:
        import urllib.request
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        body = json.dumps({
            "model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512, "temperature": 0.3
        }).encode()
        req = urllib.request.Request(f"{url}/chat/completions", data=body, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[错误] {e}"


# ── 启动服务 (Windows) ──

def _start_ollama():
    """启动Ollama服务"""
    try:
        if platform.system() == "Windows":
            proc = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            time.sleep(3)
            status = _check_ollama()
            if status["running"]:
                return f"Ollama 已启动 (PID: {proc.pid})"
            return "Ollama 启动中，请稍候检查"
        return "仅Windows支持自动启动"
    except Exception as e:
        return f"启动失败: {e}"


# ── 主动能 ──

def run(cmd: str = "") -> str:
    """LLM服务管理器

    命令:
        status          - 查看所有服务状态
        ollama:query    - 向Ollama发请求
        api:query       - 向API端点发请求
        start           - 启动Ollama
        pull <model>    - 拉取模型
    """
    if not cmd:
        # 交互模式
        print("=" * 50)
        print("  LLM 服务管理器")
        print("=" * 50)
        while True:
            try:
                q = input("  > ").strip()
                if not q or q == "q":
                    break
                print(run(q))
            except (EOFError, KeyboardInterrupt):
                break
        return ""

    cmd = cmd.strip()

    # status
    if cmd == "status":
        lines = ["LLM 服务状态:", "-" * 40]

        o = _check_ollama()
        s_ollama = "RUNNING" if o["running"] else "STOPPED"
        lines.append(f"  Ollama  [{s_ollama}] {o['url']}")
        if o["models"]:
            lines.append(f"    模型: {', '.join(o['models'][:5])}")

        v = _check_vllm()
        s_vllm = "RUNNING" if v["running"] else "STOPPED"
        lines.append(f"  vLLM    [{s_vllm}] {v['url']}")

        openai_url = os.environ.get("OPENAI_BASE_URL", "")
        if openai_url:
            a = _check_openai()
            s_api = "RUNNING" if a["running"] else "STOPPED"
            lines.append(f"  API     [{s_api}] {a['url']}")
            if a["models"]:
                lines.append(f"    模型: {', '.join(a['models'][:3])}")
        else:
            lines.append("  API     [未配置] 设置 OPENAI_BASE_URL")

        return "\n".join(lines)

    # start
    if cmd == "start":
        return _start_ollama()

    # pull
    if cmd.startswith("pull "):
        model = cmd[5:].strip()
        if not model:
            return "请指定模型名，如: ollama pull gemma3:2b"
        try:
            proc = subprocess.Popen(
                ["ollama", "pull", model],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            out, _ = proc.communicate(timeout=120)
            return f"拉取 '{model}' 完成:\n{out[-500:]}"
        except subprocess.TimeoutExpired:
            return f"拉取 '{model}' 超时（后台进行中）"
        except Exception as e:
            return f"拉取失败: {e}"

    # ollama query
    if cmd.startswith("ollama:"):
        prompt = cmd[7:].strip()
        if not prompt:
            return "请输入查询内容"
        o = _check_ollama()
        if not o["running"]:
            return "Ollama 未运行，请先执行 'start'"
        model = o["models"][0] if o["models"] else "gemma3:latest"
        return _query_ollama(model, prompt)

    # api query
    if cmd.startswith("api:"):
        prompt = cmd[4:].strip()
        openai_url = os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1")
        api_key = os.environ.get("OPENAI_API_KEY", "")
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        if not prompt:
            return "请输入查询内容"
        return _query_api(openai_url, model, prompt, api_key)

    # direct query
    o = _check_ollama()
    if o["running"] and o["models"]:
        model = o["models"][0]
        return _query_ollama(model, cmd)

    return f"未知命令: {cmd}"


def main():
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    result = run(q)
    if result:
        print(result)


if __name__ == "__main__":
    main()
