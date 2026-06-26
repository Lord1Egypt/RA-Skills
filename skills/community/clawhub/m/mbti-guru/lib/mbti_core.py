#!/usr/bin/env python3
"""
MBTI Guru - 核心处理模块 (平台无关)
支持所有 OpenClaw 渠道: Telegram, Discord, 飞书, 微信等
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# 添加 lib 到路径
sys.path.insert(0, os.path.dirname(__file__))

from lib.session import save_session, load_session, get_incomplete_session, delete_session, list_user_sessions
from lib.history import save_test_result, get_test_history, get_test_detail
from lib.question_pool import sample_questions
from lib.scorer import calculate_type, calculate_clarity

# ==================== 常量 ====================
VERSIONS = {
    "1": {"name": "快速版", "name_en": "Quick", "questions": 70, "minutes": 10},
    "2": {"name": "标准版", "name_en": "Standard", "questions": 93, "minutes": 15},
    "3": {"name": "扩展版", "name_en": "Extended", "questions": 144, "minutes": 25},
    "4": {"name": "专业版", "name_en": "Professional", "questions": 200, "minutes": 35},
}

# ==================== 用户状态管理 ====================
class UserState:
    """用户测试状态"""
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.state = "idle"  # idle, selecting_version, testing, completed
        self.version: Optional[int] = None
        self.questions: List[Dict] = []
        self.current_index: int = 0
        self.answers: List[Tuple[str, str]] = []
        self.session_id: Optional[str] = None
        self.start_time: Optional[float] = None
        self.last_save_time: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "chat_id": self.chat_id,
            "state": self.state,
            "version": self.version,
            "current_index": self.current_index,
            "answers_count": len(self.answers),
            "session_id": self.session_id
        }

# 内存中的用户状态
_user_states: Dict[int, UserState] = {}

def get_user_state(chat_id: int) -> UserState:
    """获取或创建用户状态"""
    if chat_id not in _user_states:
        _user_states[chat_id] = UserState(chat_id)
    return _user_states[chat_id]

def clear_user_state(chat_id: int):
    """清除用户状态"""
    if chat_id in _user_states:
        del _user_states[chat_id]

# ==================== 进度保存 ====================
def save_progress(chat_id: int, state: UserState) -> str:
    """保存测试进度"""
    if state.version and state.questions:
        session_id = save_session(
            chat_id=chat_id,
            version=state.version,
            current_index=state.current_index,
            answers=state.answers,
            questions_total=len(state.questions)
        )
        state.session_id = session_id
        state.last_save_time = time.time()
        return session_id
    return ""

# ==================== 消息生成 ====================
def get_version_selection_text() -> str:
    """版本选择文本"""
    msg = "📊 **MBTI 人格测试**\n\n"
    msg += "请选择测试版本：\n\n"
    for key, info in VERSIONS.items():
        msg += f"`{key}`. {info['name']} ({info['questions']}题) ~{info['minutes']}分钟\n"
    msg += "\n发送数字 `1-4` 选择版本"
    return msg

def get_progress_bar(current: int, total: int, width: int = 10) -> str:
    """生成进度条"""
    filled = int(current * width / total)
    empty = width - filled
    pct = int(current * 100 / total)
    return f"[{'█' * filled}{'░' * empty}] {pct}% ({current}/{total})"

def get_question_text(state: UserState) -> Tuple[str, int]:
    """获取当前题目文本和题号"""
    q = state.questions[state.current_index]
    q_num = state.current_index + 1
    total = len(state.questions)
    
    progress = get_progress_bar(q_num, total)
    
    header = f"📝 **问题 {q_num}/{total}**\n{progress}\n\n"
    
    option_a = q.get("option_a", "")
    option_b = q.get("option_b", "")
    
    body = f"{q.get('question_cn', '')}\n\n"
    body += f"🅰️ {option_a}\n\n"
    body += f"🅱️ {option_b}"
    
    return header + body, q_num

def get_completion_text(type_code: str, scores: Dict, clarity: Dict) -> str:
    """完成消息文本"""
    type_names = {
        "ISTJ": "物流师", "ISFJ": "守卫者", "INFJ": "提倡者", "INTJ": "建筑师",
        "ISTP": "鉴赏家", "ISFP": "探险家", "INFP": "调停者", "INTP": "逻辑学家",
        "ESTP": "企业家", "ESFP": "表演者", "ENFP": "竞选者", "ENTP": "辩论家",
        "ESTJ": "经理", "ESFJ": "执政官", "ENFJ": "主人公", "ENTJ": "指挥官",
    }
    
    name_en = type_names.get(type_code, type_code)
    
    msg = f"🎉 **测试完成！**\n\n"
    msg += f"你的MBTI类型：**{type_code}** ({name_en})\n\n"
    msg += "**维度得分：**\n"
    
    dim_names = {"EI": "能量倾向", "SN": "信息获取", "TF": "决策方式", "JP": "生活态度"}
    for dim, (score, pref) in clarity.items():
        dim_name = dim_names.get(dim, dim)
        bar = "▓" * int(score // 10) + "░" * (10 - int(score // 10))
        msg += f"{dim} {dim_name}: {bar} {score}%\n"
    
    msg += "\n正在生成PDF报告..."
    return msg

def get_history_text(history: List[Dict]) -> str:
    """历史记录文本"""
    if not history:
        return "📭 暂无测试历史\n\n开始新测试：/start"
    
    msg = "📜 **测试历史**\n\n"
    for i, test in enumerate(history[:5], 1):
        date = test.get("date", "")[:10]
        mtype = test.get("type_code", "")
        version = test.get("version", "")
        clarity_val = test.get("clarity", {})
        
        if clarity_val:
            vals = [v.get("value", 0) for v in clarity_val.values() if isinstance(v, dict)]
            avg = sum(vals) / len(vals) if vals else 0
            clarity_str = f"{avg:.0f}%"
        else:
            clarity_str = "N/A"
        
        msg += f"`{i}`. **{mtype}** | 清晰度: {clarity_str} | {date} | v{version}题\n"
    
    if len(history) > 5:
        msg += f"\n_显示最近5条，共{len(history)}条历史_"
    
    return msg

def get_status_text(chat_id: int, state: UserState) -> str:
    """状态查询文本"""
    incomplete = get_incomplete_session(chat_id)
    
    if state.state == "testing" and state.questions:
        progress = get_progress_bar(state.current_index, len(state.questions))
        msg = f"📍 **测试进行中**\n\n"
        msg += f"版本：{state.version}题\n"
        msg += f"进度：{progress}\n"
        msg += f"已答：{len(state.answers)}题"
        return msg
    
    if incomplete:
        progress = get_progress_bar(incomplete["current_index"], incomplete["questions_total"])
        msg = f"📍 **有未完成的测试**\n\n"
        msg += f"版本：{incomplete['version']}题\n"
        msg += f"进度：{progress}\n"
        msg += f"发送 /resume 继续"
        return msg
    
    return "📍 **当前状态：** 空闲\n\n发送 /start 开始新测试"

# ==================== 核心处理 ====================
def process_start(chat_id: int) -> Dict:
    """处理开始命令"""
    state = get_user_state(chat_id)
    state.state = "idle"
    return {
        "action": "send",
        "message": get_version_selection_text(),
        "state": "selecting_version"
    }

def process_version_select(chat_id: int, version_key: str) -> Dict:
    """处理版本选择"""
    if version_key not in VERSIONS:
        return {"action": "send", "message": "请发送数字 1-4 选择版本"}
    
    version_info = VERSIONS[version_key]
    version_num = version_info["questions"]
    
    state = get_user_state(chat_id)
    state.state = "testing"
    state.version = version_num
    state.questions = sample_questions(version_num)
    state.current_index = 0
    state.answers = []
    state.start_time = time.time()
    
    question_text, _ = get_question_text(state)
    
    return {
        "action": "send",
        "message": question_text,
        "state": "testing"
    }

def process_answer(chat_id: int, answer: str) -> Dict:
    """处理回答"""
    state = get_user_state(chat_id)
    
    # 如果状态不是testing，尝试恢复session
    if state.state != "testing":
        incomplete = get_incomplete_session(chat_id)
        if incomplete:
            state.state = "testing"
            state.version = incomplete["version"]
            state.questions = sample_questions(incomplete["questions_total"])
            state.current_index = incomplete["current_index"]
            state.answers = incomplete["answers"]
            state.session_id = incomplete["session_id"]
        else:
            return {"action": "send", "message": "请先开始测试：/start"}
    
    if answer.upper() not in ["A", "B"]:
        return {"action": "send", "message": "请回复 A 或 B"}
    
    # 保存答案
    q = state.questions[state.current_index]
    state.answers.append((q["id"], answer.upper()))
    
    # 下一题
    state.current_index += 1
    
    # 每次都保存进度
    save_progress(chat_id, state)
    
    # 检查是否完成
    if state.current_index >= len(state.questions):
        type_code, scores = calculate_type(state.answers)
        clarity = {dim: calculate_clarity(score) for dim, score in scores.items()}
        
        # 保存结果到历史
        save_test_result(chat_id, type_code, scores, clarity, state.version, len(state.answers))
        
        # 清理
        if state.session_id:
            delete_session(state.session_id)
        clear_user_state(chat_id)
        
        return {
            "action": "complete",
            "message": get_completion_text(type_code, scores, clarity),
            "type_code": type_code,
            "scores": scores,
            "clarity": clarity
        }
    
    # 返回下一题
    question_text, q_num = get_question_text(state)
    
    return {
        "action": "send",
        "message": question_text,
        "q_num": q_num,
        "state": "testing"
    }

def process_resume(chat_id: int) -> Dict:
    """处理恢复"""
    incomplete = get_incomplete_session(chat_id)
    
    if not incomplete:
        return process_start(chat_id)
    
    state = get_user_state(chat_id)
    state.state = "testing"
    state.version = incomplete["version"]
    state.questions = sample_questions(incomplete["questions_total"])
    state.current_index = incomplete["current_index"]
    state.answers = incomplete["answers"]
    state.session_id = incomplete["session_id"]
    
    question_text, _ = get_question_text(state)
    
    return {
        "action": "send",
        "message": f"✅ 已恢复进度\n\n{question_text}",
        "state": "testing"
    }

def process_history(chat_id: int) -> Dict:
    """处理历史"""
    history = get_test_history(chat_id)
    return {
        "action": "send",
        "message": get_history_text(history)
    }

def process_status(chat_id: int) -> Dict:
    """处理状态"""
    state = get_user_state(chat_id)
    return {
        "action": "send",
        "message": get_status_text(chat_id, state)
    }

def process_cancel(chat_id: int) -> Dict:
    """处理取消"""
    state = get_user_state(chat_id)
    
    if state.session_id:
        delete_session(state.session_id)
    
    clear_user_state(chat_id)
    
    return {
        "action": "send",
        "message": "❌ 测试已取消\n\n发送 /start 开始新测试"
    }

# ==================== 统一入口 ====================
def process_message(chat_id: int, text: str) -> Dict:
    """
    统一消息处理入口
    适用于所有平台: Telegram, Discord, 飞书, 微信等
    """
    text = text.strip()
    
    # 命令处理
    if text == "/start":
        return process_start(chat_id)
    elif text == "/help":
        msg = "📖 **MBTI Guru 使用指南**\n\n"
        msg += "`/start` - 开始新测试\n"
        msg += "`/resume` - 继续未完成的测试\n"
        msg += "`/history` - 查看测试历史\n"
        msg += "`/status` - 查看当前状态\n"
        msg += "`/cancel` - 取消当前测试\n"
        msg += "\n直接回复 A 或 B 回答问题"
        return {"action": "send", "message": msg}
    elif text == "/resume":
        return process_resume(chat_id)
    elif text == "/history":
        return process_history(chat_id)
    elif text == "/status":
        return process_status(chat_id)
    elif text == "/cancel":
        return process_cancel(chat_id)
    
    # 版本选择
    if text in ["1", "2", "3", "4"]:
        return process_version_select(chat_id, text)
    
    # 答题
    state = get_user_state(chat_id)
    if state.state == "testing" and text.upper() in ["A", "B"]:
        return process_answer(chat_id, text.upper())
    
    # 如果收到A/B但状态不是testing，尝试恢复session
    if text.upper() in ["A", "B"]:
        incomplete = get_incomplete_session(chat_id)
        if incomplete:
            state.state = "testing"
            state.version = incomplete["version"]
            state.questions = sample_questions(incomplete["questions_total"])
            state.current_index = incomplete["current_index"]
            state.answers = incomplete["answers"]
            state.session_id = incomplete["session_id"]
            return process_answer(chat_id, text.upper())
    
    # 默认：显示版本选择
    if state.state in ["idle", "completed"]:
        return process_start(chat_id)
    
    return {"action": "send", "message": "请回复 A 或 B 回答问题"}
