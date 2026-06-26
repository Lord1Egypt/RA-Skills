# -*- coding: utf-8 -*-
import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 查找工作区根目录
def find_workspace_root():
    """查找工作区根目录"""
    current = Path(os.getcwd())

    # 查找包含 .learnings 或 skills 目录的根目录
    for parent in [current] + list(current.parents):
        if (parent / ".learnings").exists() or (parent / "skills").exists():
            return parent

    return current

WORKSPACE = find_workspace_root()

# 添加mempalace路径
mempalace_path = WORKSPACE / "skills" / "mempalace"
if mempalace_path.exists():
    sys.path.insert(0, str(mempalace_path))
    from mempalace.mcp_server import handle_request

# 配置文件路径
CONFIG_FILE = WORKSPACE / "skills" / "continuous-learning" / "config" / "dream_config.json"
DEFAULT_QUEUE = WORKSPACE / ".notification_queue.json"

# 加载配置
def load_config():
    """加载配置"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                notification_config = config.get('notification', {})
                return {
                    'queue_file': WORKSPACE / notification_config.get('queue_file', '.notification_queue.json'),
                    'to': notification_config.get('to', ''),
                    'account_id': notification_config.get('account_id', '')
                }
    except:
        pass

    return {
        'queue_file': DEFAULT_QUEUE,
        'to': '',
        'account_id': ''
    }

NOTIFICATION_CONFIG = load_config()

def queue_notification(message):
    """将通知存入队列"""
    try:
        notifications = []

        queue_file = NOTIFICATION_CONFIG['queue_file']
        to_user = NOTIFICATION_CONFIG.get('to', '')

        if queue_file.exists():
            with open(queue_file, 'r', encoding='utf-8') as f:
                notifications = json.load(f)

        notification_item = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'to': to_user
        }

        notifications.append(notification_item)

        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"[NOTIFY] 队列写入失败: {e}")
        return False

def send_weixin_notification(message):
    """发送微信通知"""
    try:
        to_user = NOTIFICATION_CONFIG.get('to', '')
        account_id = NOTIFICATION_CONFIG.get('account_id', '')

        if not to_user:
            print("[NOTIFY] 未配置通知目标，跳过发送")
            return False

        cmd = [
            'openclaw',
            'message', 'send',
            '--target', to_user,
            '--message', message,
            '--channel', 'openclaw-weixin'
        ]

        if account_id:
            cmd.extend(['--account', account_id])

        result = subprocess.run(cmd, timeout=30, cwd=str(WORKSPACE),
                                capture_output=True, text=True,
                                encoding='utf-8', errors='replace')

        if result.returncode == 0:
            print(f"[NOTIFY] 通知发送成功")
            return True
        else:
            print(f"[NOTIFY] 通知发送失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"[NOTIFY] 通知异常: {e}")
        return False

if __name__ == '__main__':
    print("[SYNC] 开始同步 -", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    try:
        # 调用MemPalace创建日记条目
        if 'handle_request' in globals():
            today = datetime.now().strftime('%Y%m%d')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            request = {
                "method": "mcp__call",
                "params": {
                    "name": "create_diary_entry",
                    "arguments": {
                        "title": f"对话记录_{today}",
                        "content": f"[SYNC] 自动同步于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
                        "drawer": "wing_xiaomai"
                    }
                }
            }

            result = handle_request(request)
            print(f"Diary entry: {result.get('result', {}).get('id', 'unknown')} → wing_xiaomai/diary/daily_summary")
        else:
            print("[SYNC] MemPalace未安装，跳过日记创建")

    print("[SYNC] 同步完成")

    # 发送通知
    message = (
        f"✅ MemPalace同步完成\n\n"
        f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"⚡ 耗时: 已创建日记条目"
    )

    # 尝试发送微信通知
    if send_weixin_notification(message):
        print("[SYNC] 微信通知已发送")
    else:
        print("[SYNC] 微信通知发送失败，已存入队列")
        queue_notification(message)

    except Exception as e:
        print(f"[SYNC] 同步失败: {e}")
        import traceback
        traceback.print_exc()
