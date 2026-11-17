#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QCM 反向工具处理器（V8.4 · 跨 skill 协同）

tool_qcm_query：Infoseek → QCM 反向调用
  探测 QCM 安装（~/.workbuddy/skills/QCM 或 QCM_ROOT env）→ stdio 调 QCM mcp_server.py
  的 qcm_attribution 工具 → 返回 QCM 4 形态输出；QCM 未安装/失败 → 优雅降级 degraded。
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict


def _probe_qcm_root() -> str:
    """探测 QCM 安装根目录（env 优先 · 用户级 skills 目录兜底）"""
    env = os.environ.get("QCM_ROOT", "").strip()
    if env and os.path.isdir(env):
        return env
    candidates = [
        str(Path.home() / ".workbuddy" / "skills" / "QCM"),
        str(Path(__file__).resolve().parent.parent.parent / "QCM"),
    ]
    for c in candidates:
        if os.path.isdir(c) and os.path.isfile(os.path.join(c, "SKILL.md")):
            return c
    return ""


def _qcm_call(qcm_root: str, query: str, form: str = "") -> dict:
    """stdio 调 QCM mcp_server 的 qcm_attribution"""
    server = os.path.join(qcm_root, "scripts", "mcp_server.py")
    if not os.path.isfile(server):
        return {"status": "degraded", "reason": "QCM mcp_server.py 缺失"}
    request = {
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {
            "name": "qcm_attribution",
            "arguments": {
                "unparsed_query": query,
                "qcm_failure_dimensions": ["", "ok", "", "", ""],  # QCM 契约：5 维占位
            },
        },
    }
    if form:
        request["params"]["arguments"]["form"] = form
    try:
        proc = subprocess.Popen(
            [sys.executable, server],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True,
            env={**os.environ, "QCM_ROOT": qcm_root},
        )
        proc.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
        proc.stdin.flush()
        proc.stdin.close()
        response = proc.stdout.readline().strip()
        proc.wait(timeout=30)
        parsed = json.loads(response) if response else {}
        result = parsed.get("result", parsed)
        if result.get("error"):
            return {"status": "error", "reason": str(result["error"])[:200]}
        # MCP 工具返回双层嵌套：result.content[0].text 是内层 JSON 字符串
        inner = result
        try:
            content = result.get("content") or []
            if content and isinstance(content[0], dict) and "text" in content[0]:
                inner = json.loads(content[0]["text"])
        except Exception:
            pass
        return {"status": "ok", "qcm_result": inner}
    except Exception as e:
        return {"status": "degraded", "reason": f"QCM 调用失败: {str(e)[:200]}"}


def tool_qcm_query(args: Dict) -> Dict:
    """qcm_query 工具实现：query → QCM 4 形态输出"""
    query = (args or {}).get("query", "").strip()
    form = (args or {}).get("form", "")
    if not query:
        return {"status": "failed", "reason": "query 不能为空", "degradation": "invalid_input"}

    qcm_root = _probe_qcm_root()
    if not qcm_root:
        return {
            "status": "degraded",
            "reason": "QCM 未安装（可选依赖 · 降级）",
            "degradation": "qcm_not_installed",
            "suggest": "安装 QCM skill 后重试（~/.workbuddy/skills/QCM）",
        }

    result = _qcm_call(qcm_root, query, form)
    if result.get("status") == "ok":
        qr = result.get("qcm_result", {})
        return {
            "status": "ok",
            "qcm_result": {
                "intent": qr.get("intent", ""),
                "form": qr.get("matched_qcm_form") or qr.get("form", ""),
                "confidence": qr.get("confidence_score", qr.get("confidence", 0)),
                "degradation_path": qr.get("degradation_path", ""),
                "anchors": (qr.get("anchors") or [])[:5],
                "version": qr.get("version", "QCM"),
            },
        }
    return result
