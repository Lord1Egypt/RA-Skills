#!/usr/bin/env python3
"""
通过端口终止进程

支持 macOS 和 Linux 系统。

用法:
    python kill_by_port.py <port>
    python kill_by_port.py 8080
    python kill_by_port.py 8080 --safe
    python kill_by_port.py 8080 --dry-run
    python kill_by_port.py 8080 --signal 15
"""

import argparse
import sys
import time
import signal
import os
from find_port import find_processes_by_port


def kill_process(pid, sig=signal.SIGKILL):
    """终止进程"""
    try:
        os.kill(pid, sig)
        return True, None
    except ProcessLookupError:
        return False, "进程不存在"
    except PermissionError:
        return False, "权限不足"
    except Exception as e:
        return False, str(e)


def wait_for_process(pid, timeout=5):
    """等待进程终止"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # 检测进程是否还存在
            os.kill(pid, 0)
            time.sleep(0.5)
        except ProcessLookupError:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="通过端口终止进程")
    parser.add_argument("port", type=int, help="要终止的端口号")
    parser.add_argument("--safe", action="store_true", 
                        help="安全模式：先发送 SIGTERM，等待后再发送 SIGKILL")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅显示要终止的进程，不实际执行")
    parser.add_argument("--signal", type=int, default=9,
                        help="要发送的信号（默认 9=SIGKILL，15=SIGTERM）")
    parser.add_argument("--timeout", type=int, default=5,
                        help="安全模式下的等待超时（秒）")
    
    args = parser.parse_args()
    
    # 查找进程
    processes = find_processes_by_port(args.port)
    
    if not processes:
        print(f"✅ 端口 {args.port} 没有被占用")
        return 0
    
    # 显示信息
    print(f"\n⚠️  找到 {len(processes)} 个进程占用端口 {args.port}:")
    print("-" * 80)
    for proc in processes:
        print(f"  PID:     {proc['pid']}")
        print(f"  用户:    {proc['user']}")
        print(f"  命令:    {proc['command'][:70]}{'...' if len(proc['command']) > 70 else ''}")
        print()
    
    if args.dry_run:
        print("🔍 --dry-run 模式：不实际终止进程")
        return 0
    
    # 确认
    print("-" * 80)
    try:
        if args.safe:
            print(f"⚠️  安全模式：将先发送 SIGTERM，等待 {args.timeout} 秒后再发送 SIGKILL")
        else:
            print(f"⚠️  将发送信号 {args.signal} 终止以上进程")
        
        response = input("\n确认继续？(y/N): ").strip().lower()
        if response not in ["y", "yes"]:
            print("❌ 已取消")
            return 1
    except KeyboardInterrupt:
        print("\n❌ 已取消")
        return 1
    
    # 执行终止
    success_count = 0
    fail_count = 0
    
    print(f"\n🚀 开始终止进程...")
    
    for proc in processes:
        pid = proc["pid"]
        print(f"\n处理 PID {pid}...")
        
        if args.safe:
            # 安全模式：先 SIGTERM
            print(f"  发送 SIGTERM (15)...")
            ok, err = kill_process(pid, signal.SIGTERM)
            
            if not ok:
                print(f"  ❌ 失败: {err}")
                fail_count += 1
                continue
            
            # 等待进程终止
            print(f"  等待进程终止...")
            terminated = wait_for_process(pid, args.timeout)
            
            if terminated:
                print(f"  ✅ 进程已优雅退出")
                success_count += 1
                continue
            
            # 如果还在运行，发送 SIGKILL
            print(f"  ⚠️  进程仍在运行，发送 SIGKILL (9)...")
            ok, err = kill_process(pid, signal.SIGKILL)
            
            if ok:
                print(f"  ✅ 进程已强制终止")
                success_count += 1
            else:
                print(f"  ❌ 失败: {err}")
                fail_count += 1
        else:
            # 直接发送指定信号
            sig = args.signal
            sig_name = signal.Signals(sig).name if sig in signal.Signals else str(sig)
            print(f"  发送信号 {sig} ({sig_name})...")
            ok, err = kill_process(pid, sig)
            
            if ok:
                print(f"  ✅ 成功")
                success_count += 1
            else:
                print(f"  ❌ 失败: {err}")
                fail_count += 1
    
    # 总结
    print("\n" + "=" * 80)
    print(f"📊 总结:")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")
    
    if fail_count == 0:
        print(f"\n✅ 端口 {args.port} 已释放")
        return 0
    else:
        print(f"\n⚠️  部分进程终止失败，可能需要 sudo 权限")
        return 1


if __name__ == "__main__":
    sys.exit(main())
