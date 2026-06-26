#!/usr/bin/env python3
"""
Good-Memory 自动恢复脚本
在Agent收到第一条消息时自动执行，不需要修改Agent代码
用法：在AGENTS.md中添加启动时执行此脚本
"""

import os
import sys
import json
import subprocess
import re
import time
from datetime import datetime

# 配置
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAINTENANCE_SCRIPT = os.path.join(SKILL_DIR, "scripts", "maintenance.sh")
RECOVERY_SCRIPT = os.path.join(SKILL_DIR, "scripts", "recovery.sh")
LOG_FILE = os.path.join(SKILL_DIR, "autorecover.log")
SESSIONS_DIR = "/root/.openclaw/agents/main/sessions"
SESSIONS_JSON = "/root/.openclaw/agents/main/sessions/sessions.json"

def log(message):
    """写日志到文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_all_sessions_from_json():
    """从sessions.json读取所有会话，返回 {session_id: (agent, chat_id, session_key)}"""
    sessions = {}
    try:
        if os.path.exists(SESSIONS_JSON):
            with open(SESSIONS_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for session_key, info in data.items():
                parts = session_key.split(':')
                if len(parts) >= 5:
                    agent = parts[1]
                    chat_id = parts[-1]
                    session_id = info.get('sessionId', '')
                    if session_id:
                        sessions[session_id] = (agent, chat_id, session_key)
            log(f"从sessions.json读取到 {len(sessions)} 个会话")
    except Exception as e:
        log(f"读取sessions.json失败: {e}")
    return sessions

def get_current_session_file():
    """获取当前最新的session文件（当前正在处理的会话）"""
    try:
        # 获取最新的非reset jsonl文件
        files = [f for f in os.listdir(SESSIONS_DIR) 
                if f.endswith('.jsonl') 
                and not any(s in f for s in ('.reset.', '.deleted.', '.lock'))]
        if not files:
            return None
        # 按修改时间排序，取最新的
        files.sort(key=lambda x: os.path.getmtime(os.path.join(SESSIONS_DIR, x)), reverse=True)
        return os.path.join(SESSIONS_DIR, files[0])
    except Exception as e:
        log(f"获取最新session文件失败: {e}")
        return None

def extract_chat_id_from_session_file(filepath):
    """从session文件中提取chat_id（最多读前200行）"""
    session_key_pattern = re.compile(r'agent:([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+)')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 200:
                    break
                match = session_key_pattern.search(line)
                if match:
                    session_key = match.group(0)
                    parts = session_key.split(':')
                    if len(parts) >= 5:
                        agent = parts[1]
                        chat_id = parts[-1]
                        return agent, chat_id, session_key
    except Exception as e:
        log(f"从session文件提取失败: {e}")
        pass
    return None, None, None

def main():
    log("=== 开始执行自动恢复 ===")
    
    try:
        # 延迟3秒，确保session文件完全生成，避免race condition
        time.sleep(3)
        log("延迟3秒完成，开始处理")
        
        # 1. 首先尝试从环境变量获取
        agent_name = os.environ.get("INBOUND_AGENT") or os.environ.get("AGENT_NAME") or "main"
        chat_id = os.environ.get("INBOUND_CHAT_ID") or os.environ.get("CHAT_ID") or ""
        session_key = os.environ.get("SESSION_KEY") or ""
        
        log(f"从环境变量获取：agent={agent_name}, chat_id={chat_id}, session_key={session_key}")
        
        # 2. 读取所有会话映射
        sessions_map = get_all_sessions_from_json()
        
        # 3. 获取当前session文件
        current_session = get_current_session_file()
        log(f"当前最新session文件: {current_session}")
        
        if current_session and not chat_id:
            # 从文件名提取session_id
            session_id = os.path.basename(current_session).split('.')[0]
            log(f"当前session_id: {session_id}")
            
            # 优先从sessions_map查找
            if session_id in sessions_map:
                agent_name, chat_id, session_key = sessions_map[session_id]
                log(f"从sessions.json找到：agent={agent_name}, chat_id={chat_id}, session_key={session_key}")
            else:
                # 从文件内容提取
                agent_from_file, chat_id_from_file, session_key_from_file = extract_chat_id_from_session_file(current_session)
                if chat_id_from_file:
                    agent_name = agent_from_file or agent_name
                    chat_id = chat_id_from_file
                    session_key = session_key_from_file
                    log(f"从session文件提取：agent={agent_name}, chat_id={chat_id}, session_key={session_key}")
        
        if not chat_id:
            # 无法获取chat_id，跳过自动恢复
            log("❌ 无法获取chat_id，跳过恢复")
            print("", end="")
            return 0
        
        # 4. 强制执行detect检测是否重置（一定会更新tracker）
        log(f"执行detect命令：{MAINTENANCE_SCRIPT} detect {agent_name} {chat_id}")
        result = subprocess.run(
            [MAINTENANCE_SCRIPT, "detect", agent_name, chat_id],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = result.stdout + result.stderr
        log(f"detect输出：\n{output}")
        
        last_history = ""
        reset_detected = False
        
        # 5. 提取last_history路径和检测结果
        if "RESET_DETECTED" in output:
            reset_detected = True
            log("✅ 检测到重置")
            lines = output.strip().split('\n')
            for line in lines:
                if line.startswith("last_history:"):
                    last_history = line.split(":", 1)[1].strip()
                    log(f"找到last_history: {last_history}")
                    break
        else:
            # 额外检测：如果active_uuid变化但没有reset文件（隐式会话切换），尝试读取上一个会话
            log("⚠️ 没有检测到显式重置，检查是否有隐式会话切换")
            try:
                # 读取tracker获取上一个active_uuid
                with open("/root/.openclaw/workspace/session-tracker.json", 'r') as f:
                    tracker = json.load(f)
                if agent_name in tracker["agents"] and chat_id in tracker["agents"][agent_name]:
                    info = tracker["agents"][agent_name][chat_id]
                    prev_uuid = info.get("active_uuid", "")
                    if prev_uuid and current_uuid != prev_uuid:
                        log(f"⚠️ 检测到隐式会话切换：prev={prev_uuid}, current={current_uuid}")
                        # 尝试查找上一个会话文件是否还存在
                        prev_session = os.path.join(SESSIONS_DIR, f"{prev_uuid}.jsonl")
                        if os.path.exists(prev_session):
                            log(f"✅ 找到上一个会话文件：{prev_session}")
                            last_history = prev_session
                            reset_detected = True
            except Exception as e:
                log(f"隐式切换检测失败：{e}")
        
        # 6. 如果有last_history，读取历史记录
        if reset_detected and last_history and os.path.exists(last_history):
            log(f"读取历史记录：{RECOVERY_SCRIPT} read-file {last_history}")
            history_result = subprocess.run(
                [RECOVERY_SCRIPT, "read-file", last_history, "--lines", "50"],
                capture_output=True,
                text=True,
                timeout=5
            )
            history = history_result.stdout.strip()
            log(f"读取到历史记录：\n{history}")
            
            if history:
                # 输出恢复提示和历史记录，Agent会自动将这些内容作为系统上下文加入到对话开头
                recovery_msg = "已自动恢复 上次会话的对话记录 📜 如果想要回忆更早的请对我说\n\n"
                recovery_msg += "=== 历史对话 ===\n"
                recovery_msg += history + "\n"
                recovery_msg += "=== 当前对话 ===\n\n"
                
                log(f"输出恢复内容：\n{recovery_msg}")
                # 直接输出，OpenClaw会自动将脚本输出作为系统消息加入上下文
                print(recovery_msg, end="")
                log("✅ 恢复完成")
                return 0
        else:
            log("没有检测到重置或没有历史记录，跳过恢复")
    
    except Exception as e:
        # 任何错误都不影响正常对话，输出错误到日志
        log(f"❌ 执行错误：{str(e)}")
        print(f"[Good-Memory Error] {str(e)}", file=sys.stderr)
        pass
    
    # 没有重置或恢复失败，输出空
    log("=== 执行结束 ===")
    print("", end="")
    return 0

if __name__ == "__main__":
    sys.exit(main())
