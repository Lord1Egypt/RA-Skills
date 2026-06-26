import os
import json
import time
from datetime import datetime, timedelta

# 模拟 OpenClaw 内部逻辑，实际运行时应通过 exec 调用 openclaw CLI
# 这里编写的是核心逻辑脚本，你可以将其放在 skill 目录下运行

def get_session_history(session_key):
    """
    模拟获取会话历史。
    在实际环境中，这里应该调用 sessions_api 获取消息内容。
    """
    return [
        {"role": "user", "content": f"Hello, this is history for {session_key}"},
        {"role": "assistant", "content": "Nice to meet you!"}
    ]

def summarize_session(session_key, history):
    """
    模拟对会话内容进行总结。
    在实际环境中，这里应该调用 LLM 接口进行总结。
    """
    summary_text = f"Summary of {session_key}: The conversation was brief and polite."
    return summary_text

def save_summary(session_key, summary_content):
    """将总结内容保存到本地 summaries 文件夹"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("/root/.openclaw/workspace/skills/lite-session-cleaner/summaries", exist_ok=True)
    filename = f"/root/.openclaw/workspace/skills/lite-session-cleaner/summaries/{session_key}_{timestamp}.json"
    data = {
        "sessionKey": session_key,
        "timestamp": datetime.now().isoformat(),
        "summary": summary_content
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"总结已保存至: {filename}")
    return filename

def get_sessions():
    """
    模拟执行 'openclaw sessions_list' 并获取会话列表。
    """
    return [
        {"sessionKey": "session_1", "last_activity": time.time() - 500, "target": "openclaw-weixin:user_a"},
        {"sessionKey": "session_2", "last_activity": time.time() - 4000, "target": "openclaw-weixin:user_b"},
        {"sessionKey": "session_3", "last_activity": time.time() - 100, "target": "openclaw-weixin:user_c"},
    ]

def kill_session(session_key):
    """模拟执行 'sessions_kill <session_key>'"""
    print(f"正在终止会话: {session_key}")
    return True

def send_notification(target, message):
    """模拟发送通知"""
    print(f"向 {target} 发送消息: {message}")

def clean_stale_sessions(timeout_seconds=3600):
    now = time.time()
    print(f"开始清理任务... 当前时间: {datetime.fromtimestamp(now)}")
    
    try:
        sessions = get_sessions() 
        cleaned_count = 0
        for session in sessions:
            last_act = session['last_activity']
            session_key = session['sessionKey']
            target = session['target']
            
            if now - last_act > timeout_seconds:
                print(f"发现过期会话: {session_key} (最后活动于 {datetime.fromtimestamp(last_act)})")
                
                # --- 新增：清理前总结并存储 ---
                history = get_session_history(session_key)
                summary = summarize_session(session_key, history)
                save_summary(session_key, summary)
                # ----------------------------

                send_notification(target, "当前会话已经结束")
                
                if kill_session(session_key):
                    cleaned_count += 1
                    
        print(f"清理完成。共清理了 {cleaned_count} 个会话。")
        
    except Exception as e:
        print(f"清理过程中出错: {e}")

if __name__ == "__main__":
    clean_stale_sessions(3600)
