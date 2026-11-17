"""Bounded recovery for action promises that stop before using a tool."""
from __future__ import annotations
import os, re
from typing import Iterable, Optional
_DEFAULT_MAX_ATTEMPTS=2
_ACTION_REQUEST=re.compile(r"(?:下载|安装|检查|查看|执行|运行|修复|创建|写入|删除|更新|升级|继续|等待完成|download|install|check|inspect|run|execute|fix|create|write|delete|update|upgrade|continue)",re.I)
_UNFINISHED_PROMISE=re.compile(r"(?:(?:让我|我来|马上|立刻|现在|继续).{0,24}(?:看看|检查|执行|下载|安装|处理|等待)|(?:let me|i(?:'ll| will)|starting|continuing).{0,48}(?:check|inspect|run|execute|download|install|wait|do))",re.I|re.S)
_COMPLETION_EVIDENCE=re.compile(r"(?:已完成|完成了|成功|失败|无法|被阻止|需要你|done|completed|succeeded|failed|blocked|cannot)",re.I)
def action_stop_nudge_enabled(platform: str="")->bool:
    env=os.environ.get("HERMES_ACTION_STOP_NUDGE")
    if env is not None and env.strip().lower() in {"0","false","no","off"}: return False
    return platform.strip().lower() not in {"","cli","api_server"}
def _last_user_text(messages: Iterable[dict]|None)->str:
    for msg in reversed(list(messages or [])):
        if isinstance(msg,dict) and msg.get("role")=="user" and not any(key for key in msg if str(key).endswith("_synthetic") and msg.get(key)):
            content=msg.get("content"); return content if isinstance(content,str) else ""
    return ""
def build_action_stop_nudge(*,messages: Iterable[dict]|None,response: str,platform: str="",attempts: int=0,max_attempts: int=_DEFAULT_MAX_ATTEMPTS)->Optional[str]:
    if not action_stop_nudge_enabled(platform) or attempts>=max_attempts: return None
    request=_last_user_text(messages); answer=(response or "").strip()
    if not _ACTION_REQUEST.search(request) or not _UNFINISHED_PROMISE.search(answer) or _COMPLETION_EVIDENCE.search(answer): return None
    return "[System: You promised an action but stopped without calling a tool. Do not narrate intent or repeat the promise. Call the appropriate tool now. Continue until there is concrete execution evidence, a verified result, or a specific blocker. Only then give the user a final answer.]"
__all__=["action_stop_nudge_enabled","build_action_stop_nudge"]
