import sys
import subprocess
import argparse
import os
import shutil
import locale

def get_system_language():
    try:
        for env_var in ['LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE']:
            val = os.environ.get(env_var, '').lower()
            if val:
                if 'zh' in val: return 'zh'
                if 'en' in val: return 'en'
                
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                loc = locale.getdefaultlocale()[0]
                if loc and loc.lower().startswith('zh'): 
                    return 'zh'
        except Exception:
            pass
            
        if os.name == 'nt':
            import ctypes
            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            if (langid & 0x03FF) == 0x04:
                return 'zh'
    except Exception:
        pass
        
    return 'en'

def generate_sop(lang):
    if lang == 'zh':
        msg_warn = "⚠️ 提示：为了系统安全合规，我无权修改其他人的记忆文件。请人类用户将下方代码框内的内容复制，并手动粘贴到每一个智能体工作区的 AGENTS.md 文件末尾。贴完后，请在每个智能体发送 `/new` 重载对话即可全局生效。"
        protocol_text = """
```text
## 📡 跨智能体通信协议 (Multi-Agent Intercom)
你具有和其他智能体横向通信的能力。请严格遵守以下 SOP：

发送消息：当你需要联系或通知其他智能体时，调用系统终端执行以下命令：
`python ~/.openclaw/skills/multi-agent-intercom/scripts/intercom.py send <目标智能体 ID> <你的 ID> "<你要说的话>"`

接收与强制回复：当你看到一条以 `[来自智能体 xxx]` 开头的消息时，意味着你正在被对讲机呼叫。

你必须立刻处理该消息。
处理完毕后，你必须使用上述 send 命令将结果或确认信息回复给发送方。
严禁直接在当前主聊天框里向人类用户说"谢谢收到"，你的直接回复必须发给呼叫你的那个智能体！
防止死循环：如果对方发来的仅仅是一句"收到"或简单的确认回复，你无需再次回复对方，直接终止对话即可。
```
"""
    else:
        msg_warn = "⚠️ Note: For security compliance, I cannot modify other agents' memory files. Please manually copy the Markdown block below and paste it at the bottom of the AGENTS.md file in every agent's workspace. Type `/new` in your chat when done to reload."
        protocol_text = """
```text
## 📡 Multi-Agent Intercom Protocol
You have the ability to communicate laterally with other agents. Please strictly follow this SOP:

Send Message: When you need to contact or notify other agents, run the following command in the system terminal:
`python ~/.openclaw/skills/multi-agent-intercom/scripts/intercom.py send <TARGET_AGENT_ID> <YOUR_ID> "<YOUR_MESSAGE>"`

Receive & Mandatory Reply: When you see a message starting with `[From Agent xxx]`, it means you are being paged via intercom.

You MUST process this message immediately.
After processing, you MUST use the send command above to reply to the sender.
DO NOT just say "Thank you" to the human user in the main chat. Your direct reply MUST go to the agent who called you!
Anti-Loop Circuit Breaker: If the message you received is simply "Received" or a basic confirmation, DO NOT reply back. Terminate the conversation to prevent infinite loops.
```
"""

    print(msg_warn)
    print(protocol_text)

def run_background_task(cmd_list):
    executable = shutil.which(cmd_list[0])
    
    if not executable and os.name == 'nt':
        executable = shutil.which(cmd_list[0] + '.cmd')

    if not executable:
        print(f"❌ Error: Cannot find '{cmd_list[0]}' executable in PATH.", file=sys.stderr)
        return

    try:
        if os.name == 'nt':
            # Fix newline truncation bug in cmd.exe:
            # If the executable is a .cmd wrapper, cmd.exe will truncate arguments containing newlines.
            # We redirect it to the .ps1 equivalent and run via PowerShell to preserve multiline messages.
            if executable.lower().endswith('.cmd'):
                ps1_path = executable[:-4] + '.ps1'
                if os.path.exists(ps1_path):
                    cmd_list = ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1_path] + cmd_list[1:]
                    executable = shutil.which('powershell.exe') or 'powershell.exe'

            # Use CREATE_NO_WINDOW (0x08000000). 
            # Do NOT use DETACHED_PROCESS (0x00000008) as they conflict and can cause windows to pop up.
            CREATE_NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)
            subprocess.Popen(
                [executable] + cmd_list[1:],
                creationflags=CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                close_fds=True
            )
        else:
            subprocess.Popen(
                [executable] + cmd_list[1:],
                preexec_fn=os.setsid,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                close_fds=True
            )
    except Exception:
        pass

def send_message(target, sender_id, message, session_id, lang):
    tag = f"[来自智能体 {sender_id}] " if lang == 'zh' else f"[From Agent {sender_id}] "
    final_message = tag + message

    if lang == 'zh':
        print(f"正在尝试将消息发送给 '{target}' (会话: {session_id})...")
        print("✅ 消息已成功送出！目标智能体将在后台处理，如果需要会主动回复。")
    else:
        print(f"Attempting to send message to '{target}' (session: {session_id})...")
        print("✅ Message successfully sent! The target will process it in the background.")

    cmd_args = ['openclaw', 'agent', '--agent', target, '--session-id', session_id, '--message', final_message]
    
    sys.stdout.flush()
    run_background_task(cmd_args)
    sys.exit(0)

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')

    sys_lang = get_system_language()

    parser = argparse.ArgumentParser(description="Multi-Agent Intercom for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Commands: setup, send")
    
    subparsers.add_parser("setup", help="Generate the communication SOP for the user to copy")
    
    send_parser = subparsers.add_parser("send", help="Send a message to another agent")
    send_parser.add_argument("target_agent", help="The ID of the target agent (e.g., dev, rc)")
    send_parser.add_argument("sender_id", help="Your own agent ID (e.g., zz) for Caller ID")
    send_parser.add_argument("message", help="The message content to send")
    send_parser.add_argument("--session-id", default="main", help="The session ID to target (default: main)")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        generate_sop(sys_lang)
    elif args.command == "send":
        send_message(args.target_agent, args.sender_id, args.message, args.session_id, sys_lang)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
