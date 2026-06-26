#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenClaw专用转录包装器
解决OpenClaw环境下的输出缓冲和交互问题
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    print("=" * 60)
    print("OpenClaw会议转录包装器")
    print("=" * 60)
    print()
    print("此包装器专为解决OpenClaw环境下的转录问题：")
    print("  1. 输出缓冲问题 - 使用无缓冲输出")
    print("  2. 交互问题 - 启动独立窗口")
    print("  3. 编码问题 - 设置正确编码")
    print()
    
    print("请选择启动方式：")
    print("  1. 批处理文件（推荐，解决所有问题）")
    print("  2. 优化命令行（设置环境变量）")
    print("  3. 直接启动（可能有问题）")
    print()
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == "1":
        # 使用批处理文件
        batch_file = Path(__file__).parent / "openclaw_transcribe.bat"
        if batch_file.exists():
            print(f"\n使用批处理文件: {batch_file.name}")
            print("正在启动转录系统...")
            print()
            
            cmd = ["cmd", "/c", "start", "cmd", "/k", str(batch_file)]
            subprocess.Popen(cmd)
            
            print("转录系统已在新窗口中启动")
            print("请在新窗口中查看实时转录输出")
            print("按 Ctrl+C 停止转录")
            print()
            print("转录文件位置: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
            
        else:
            print(f"批处理文件未找到: {batch_file}")
            return 1
    
    elif choice == "2":
        # 优化命令行
        print("\n使用优化命令行启动...")
        print()
        
        cmd = ["cmd", "/c", "start", "cmd", "/k",
               "cd /d D:\\dev\\python\\voiceFunAsr && "
               "chcp 65001 && "
               "set PYTHONUNBUFFERED=1 && "
               "set PYTHONIOENCODING=utf-8 && "
               "conda run -n audioProject python -u vocie_mic_fixed_gbk.py"]
        
        print("执行命令:")
        print("  cd /d D:\\dev\\python\\voiceFunAsr")
        print("  chcp 65001")
        print("  set PYTHONUNBUFFERED=1")
        print("  set PYTHONIOENCODING=utf-8")
        print("  conda run -n audioProject python -u vocie_mic_fixed_gbk.py")
        print()
        
        subprocess.Popen(cmd)
        
        print("转录系统已在新窗口中启动")
        print("请在新窗口中查看实时转录输出")
        print("按 Ctrl+C 停止转录")
        print()
        print("转录文件位置: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
    
    elif choice == "3":
        # 直接启动（不推荐）
        print("\n直接启动（可能有问题）...")
        print("警告: 在OpenClaw中直接启动可能无法正常显示输出")
        print()
        
        cmd = ["conda", "run", "-n", "audioProject", "python", "-u", "vocie_mic_fixed_gbk.py"]
        
        print(f"执行命令: {' '.join(cmd)}")
        print(f"工作目录: D:\\dev\\python\\voiceFunAsr")
        print()
        print("正在启动转录系统...")
        print("-" * 50)
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                universal_newlines=True,
                cwd=r"D:\dev\python\voiceFunAsr",
                env={**os.environ, "PYTHONUNBUFFERED": "1"}
            )
            
            print(f"转录进程已启动，PID: {process.pid}")
            print("转录系统初始化中...")
            print()
            
            line_count = 0
            while True:
                line = process.stdout.readline()
                if line:
                    line = line.rstrip()
                    line_count += 1
                    print(f"[{line_count:03d}] {line}")
                    sys.stdout.flush()
                
                returncode = process.poll()
                if returncode is not None:
                    print(f"转录进程结束，退出码: {returncode}")
                    break
            
            print("-" * 50)
            print(f"总共输出 {line_count} 行")
            
        except KeyboardInterrupt:
            print("\n用户中断转录")
            if 'process' in locals():
                process.terminate()
        except Exception as e:
            print(f"转录启动错误: {e}")
            return 1
    
    else:
        print("无效选择")
        return 1
    
    print()
    print("=" * 60)
    print("启动完成")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())