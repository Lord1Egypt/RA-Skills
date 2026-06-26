#!/usr/bin/env python3
"""
记忆自动保存服务 - 守护进程模式

用法:
    # 启动服务（只需一次）
    python3 memory_daemon.py start --user-id ou_xxx
    
    # 查看状态
    python3 memory_daemon.py status
    
    # 停止服务
    python3 memory_daemon.py stop

原理:
- 启动后后台运行
- 监听 ~/.openclaw/memory_queue/
- AI 只需写入队列文件，自动保存
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

PID_FILE = os.path.expanduser("~/.openclaw/memory_daemon.pid")
QUEUE_DIR = os.path.expanduser("~/.openclaw/memory_queue")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def ensure_queue_dir():
    """确保队列目录存在"""
    Path(QUEUE_DIR).mkdir(parents=True, exist_ok=True)


def write_to_queue(user_id: str, query: str, response: str) -> bool:
    """
    AI 调用这个函数，将待保存的记忆写入队列
    立即返回，不阻塞
    """
    ensure_queue_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{user_id}_{timestamp}.json"
    filepath = os.path.join(QUEUE_DIR, filename)
    
    data = {
        "user_id": user_id,
        "query": query,
        "response": response,
        "timestamp": timestamp
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Queue Error] {e}")
        return False


def process_queue():
    """
    守护进程主循环：处理队列中的记忆保存
    """
    ensure_queue_dir()
    add_script = os.path.join(SCRIPT_DIR, 'memory_add.py')
    
    while True:
        try:
            # 获取所有待处理的文件
            files = sorted(Path(QUEUE_DIR).glob("*.json"))
            
            for filepath in files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 执行保存
                    result = subprocess.run(
                        ['python3', add_script,
                         '--user-id', data['user_id'],
                         '--query', data['query'],
                         '--response', data['response']],
                        capture_output=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        # 保存成功，删除队列文件
                        filepath.unlink()
                    else:
                        print(f"[Save Error] {result.stderr}")
                        
                except Exception as e:
                    print(f"[Process Error] {e}")
            
            # 每秒检查一次
            time.sleep(1)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[Daemon Error] {e}")
            time.sleep(5)


def start_daemon():
    """启动守护进程"""
    if os.path.exists(PID_FILE):
        print("[Error] 守护进程已在运行")
        return False
    
    # 使用 nohup 启动后台进程
    log_file = os.path.expanduser("~/.openclaw/memory_daemon.log")
    
    proc = subprocess.Popen(
        [sys.executable, __file__, 'run'],
        stdout=open(log_file, 'a'),
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    
    # 写入 PID 文件
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    print(f"[OK] 守护进程已启动 (PID: {proc.pid})")
    print(f"[Log] {log_file}")
    return True


def stop_daemon():
    """停止守护进程"""
    if not os.path.exists(PID_FILE):
        print("[Error] 守护进程未运行")
        return False
    
    with open(PID_FILE, 'r') as f:
        pid = int(f.read().strip())
    
    try:
        os.kill(pid, 15)  # SIGTERM
        os.remove(PID_FILE)
        print(f"[OK] 守护进程已停止 (PID: {pid})")
        return True
    except ProcessLookupError:
        os.remove(PID_FILE)
        print("[OK] 守护进程已停止（进程不存在）")
        return True
    except Exception as e:
        print(f"[Error] {e}")
        return False


def status_daemon():
    """查看守护进程状态"""
    if not os.path.exists(PID_FILE):
        print("[Status] 守护进程未运行")
        return False
    
    with open(PID_FILE, 'r') as f:
        pid = int(f.read().strip())
    
    # 检查进程是否存在
    result = subprocess.run(['ps', '-p', str(pid)], capture_output=True)
    
    if result.returncode == 0:
        queue_count = len(list(Path(QUEUE_DIR).glob("*.json")))
        print(f"[Status] 守护进程运行中 (PID: {pid})")
        print(f"[Queue] 待处理: {queue_count} 条")
        return True
    else:
        print(f"[Status] PID 文件存在但进程不存在，可能需要清理")
        os.remove(PID_FILE)
        return False


def main():
    parser = argparse.ArgumentParser(description='Memory Daemon')
    parser.add_argument('action', choices=['start', 'stop', 'status', 'run', 'queue'])
    parser.add_argument('--user-id', help='User ID (for queue action)')
    parser.add_argument('--query', help='Query (for queue action)')
    parser.add_argument('--response', help='Response (for queue action)')
    
    args = parser.parse_args()
    
    if args.action == 'start':
        start_daemon()
    elif args.action == 'stop':
        stop_daemon()
    elif args.action == 'status':
        status_daemon()
    elif args.action == 'run':
        # 内部使用，启动处理循环
        process_queue()
    elif args.action == 'queue':
        # AI 调用这个，将记忆加入队列
        if not all([args.user_id, args.query, args.response]):
            print("[Error] queue 需要 --user-id, --query, --response")
            sys.exit(1)
        
        if write_to_queue(args.user_id, args.query, args.response):
            print("[OK] 已加入保存队列")
        else:
            print("[Error] 加入队列失败")


if __name__ == "__main__":
    main()
