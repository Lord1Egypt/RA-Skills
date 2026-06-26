#!/usr/bin/env python3
"""
MaxKB Skill: 根据用户问题调用指定智能体

配合 list_agents 工具使用：
  1. 调用 list_agents() 获取已发布智能体列表（LLM 据此选择）
  2. LLM 根据用户问题和列表选出 agent_name
  3. 调用 chat_to_agent(question, agent_name) 发起对话，返回回答

入口函数: chat_to_agent(question: str, agent_name: str) -> str
"""

import os
import json
from urllib import request, parse
from urllib.error import HTTPError, URLError
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    # 如果没有 python-dotenv，提供简单的 .env 加载实现
    def load_dotenv(dotenv_path=None):
        if dotenv_path and os.path.exists(dotenv_path):
            with open(dotenv_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")


# ── 路径配置 ──────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ENV_FILE = SKILL_DIR / ".env"

# 加载环境变量
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

MAXKB_DOMAIN = os.environ.get("MAXKB_DOMAIN", "<maxkb_domain>")
# MaxKB API 路径前缀，默认为 /admin（标准 MaxKB 部署）
# 如果 MaxKB 部署在子路径下（如 http://example.com/mk），配置为 /mk
# 如果 MaxKB 部署在根路径且无 /admin 前缀，留空即可
MAXKB_API_PREFIX = os.environ.get("MAXKB_API_PREFIX", "/admin").rstrip("/")
MAXKB_TOKEN = os.environ.get("MAXKB_TOKEN", "")
MAXKB_WORKSPACE_ID = os.environ.get("MAXKB_WORKSPACE_ID", "default")
MAXKB_USERNAME = os.environ.get("MAXKB_USERNAME", "")
MAXKB_PASSWORD = os.environ.get("MAXKB_PASSWORD", "")

def _build_api_path(path: str) -> str:
    """Build full API path with optional prefix (e.g. /mk)
    
    注意：/chat/ 开头的路径是 MaxKB 前端路由，不需要添加 API 前缀
    - /api/... → /mk/api/...
    - /chat/... → /chat/... (不变)
    """
    if MAXKB_API_PREFIX and not path.startswith(MAXKB_API_PREFIX):
        # /chat/ 路径不需要前缀（MaxKB 特殊设计）
        if path.startswith("/chat/"):
            return path
        return f"{MAXKB_API_PREFIX}{path}"
    return path


# ── 内部 HTTP 工具 ────────────────────────────────────────────────────

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {MAXKB_TOKEN}",
        "Content-Type": "application/json",
    }


def _chat_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _get(path: str, token: str = None) -> dict:
    api_path = _build_api_path(path)
    url = f"{MAXKB_DOMAIN}{api_path}"
    headers = _headers() if token is None else _chat_headers(token)
    req = request.Request(url=url, headers=headers, method="GET")
    try:
        with request.urlopen(req) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return json.loads(resp.read().decode(charset, errors="replace"))
    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {path} 失败 HTTP {e.code}: {detail}") from e
    except URLError as e:
        raise RuntimeError(f"GET {path} 请求失败: {e}") from e


def _post_json(path: str, body: dict, token: str = None) -> dict:
    api_path = _build_api_path(path)
    url = f"{MAXKB_DOMAIN}{api_path}"
    data = json.dumps(body).encode("utf-8")
    headers = _headers() if token is None else _chat_headers(token)
    req = request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return json.loads(resp.read().decode(charset, errors="replace"))
    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"POST {path} 失败 HTTP {e.code}: {detail}") from e
    except URLError as e:
        raise RuntimeError(f"POST {path} 请求失败: {e}") from e


def _post_sse(path: str, body: dict, token: str) -> str:
    """
    发送 POST 请求并逐行解析 SSE（Server-Sent Events）流。
    收集所有 operate==true 的 content 片段，直到 is_end==true。
    """
    api_path = _build_api_path(path)
    url = f"{MAXKB_DOMAIN}{api_path}"
    data = json.dumps(body).encode("utf-8")
    req = request.Request(url=url, data=data, headers=_chat_headers(token), method="POST")
    chunks = []
    try:
        with request.urlopen(req) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if not payload or payload == "[DONE]":
                    continue
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if event.get("operate") is True:
                    chunks.append(event.get("content", ""))
                    if event.get("is_end"):
                        break
    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"SSE POST {path} 失败 HTTP {e.code}: {detail}") from e
    except URLError as e:
        raise RuntimeError(f"SSE POST {path} 请求失败: {e}") from e
    return "".join(chunks)

def _login() -> str:
    if MAXKB_USERNAME and  MAXKB_PASSWORD:
        resp = _post_json(
            "/api/user/login",
            {"username": MAXKB_USERNAME, "password": MAXKB_PASSWORD},
        )
        token = resp.get("data", {}).get("token", "")
        if not token:
            raise RuntimeError(f"登录失败，响应：{json.dumps(resp, ensure_ascii=False)}")
        return token
    else:
        return MAXKB_TOKEN


# ── 核心逻辑 ──────────────────────────────────────────────────────────

def get_published_agents() -> list:
    """返回所有已发布智能体，每条包含 id / name / desc。"""
    resp = _get(
        f"/api/workspace/{MAXKB_WORKSPACE_ID}/application/1/10000"
    )
    records = resp.get("data", {}).get("records", [])
    agents = [
        {
            "id": r["id"],
            "name": r.get("name", ""),
            "desc": r.get("desc", ""),
        }
        for r in records
        if r.get("is_publish") is True
    ]
    if not agents:
        raise RuntimeError("当前工作空间没有已发布的智能体")
    return agents


def list_agents() -> str:
    """返回已发布智能体的 name 和 desc 列表（JSON 字符串），供 LLM 选择。"""
    agents = get_published_agents()
    return json.dumps(
        [{"name": a["name"], "desc": a["desc"]} for a in agents],
        ensure_ascii=False,
    )


def find_agent_by_name(agents: list, agent_name: str) -> dict:
    """按名称精确匹配智能体，找不到则抛出异常。"""
    for a in agents:
        if a["name"] == agent_name:
            return a
    names = ", ".join(a["name"] for a in agents)
    raise RuntimeError(f"未找到名为 '{agent_name}' 的智能体，可用：{names}")


def chat_with_agent(agent_id: str, question: str) -> str:
    """
    对指定智能体发起一次对话并返回回答文本。
    """
    # 获取 access_token（匿名会话）
    token_resp = _get(f"/api/workspace/{MAXKB_WORKSPACE_ID}/application/{agent_id}/access_token")
    access_token = token_resp.get("data", {}).get("access_token", "")

    # 创建会话（注意：chat API 路径不以 /api 开头）
    chat_resp = _post_json(
        f"/chat/api/auth/anonymous",
        {"access_token": access_token},
    )
    token = chat_resp.get("data", '')
    if not token:
        raise RuntimeError(
            f"创建会话失败，响应：{json.dumps(chat_resp, ensure_ascii=False)}"
        )
    chat_id_resp = _get('/chat/api/open', token)
    chat_id = chat_id_resp.get("data", '')

    answer = _post_sse(
        f"/chat/api/chat_message/{chat_id}",
        {"message": question, 're_chat': False, 'stream': True},
        token
    )
    return answer


# ── 入口函数 ──────────────────────────────────────────────────────────

def chat_to_agent(question: str, agent_name: str) -> str:
    """
    调用指定智能体并返回回答。

    参数:
        question:   用户的问题文本
        agent_name: 由 LLM 根据 list_agents() 结果选定的智能体名称

    返回:
        JSON 字符串，包含：
          - agent_name: 实际调用的智能体名称
          - answer:     智能体的回答内容
    """
    agents = get_published_agents()
    selected = find_agent_by_name(agents, agent_name)
    answer = chat_with_agent(selected["id"], question)
    return json.dumps(
        {"agent_name": selected["name"], "answer": answer},
        ensure_ascii=False,
    )


if __name__ == "__main__":
    import sys

    MAXKB_TOKEN = _login()  # 预先登录获取 token，验证环境变量配置是否正确

    if len(sys.argv) >= 3:
        print(chat_to_agent(sys.argv[1], sys.argv[2]))
    else:
        # 仅列出已发布智能体，用于调试
        print(list_agents())
