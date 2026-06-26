#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Meeting Transcriber - 会议转录技能主文件
支持所有命令功能
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path
import webbrowser

def run_command(cmd, timeout=300, capture_output=False):
    """运行命令并处理输出"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=timeout
            )
            return result
        else:
            # 实时输出模式
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            while True:
                line = process.stdout.readline()
                if line:
                    line = line.rstrip()
                    output_lines.append(line)
                    print(line)
                    sys.stdout.flush()
                
                returncode = process.poll()
                if returncode is not None:
                    break
            
            return type('Result', (), {
                'returncode': returncode,
                'stdout': '\n'.join(output_lines),
                'stderr': ''
            })()
            
    except subprocess.TimeoutExpired:
        print(f"命令超时 ({timeout} 秒)")
        return type('Result', (), {'returncode': -1, 'stdout': '', 'stderr': 'Timeout'})()
    except Exception as e:
        print(f"执行错误: {e}")
        return type('Result', (), {'returncode': 1, 'stdout': '', 'stderr': str(e)})()

def start_transcription():
    """开始会议转录"""
    print("=" * 60)
    print("开始会议转录")
    print("=" * 60)
    print()
    
    # 检查环境
    env_result = check_environment(silent=True)
    if env_result != 0:
        print("环境检查失败，请先运行'检查转录环境'")
        return 1
    
    print("检测到OpenClaw环境，使用优化启动模式...")
    print()
    print("优化方案:")
    print("  1. 使用批处理文件解决输出缓冲问题")
    print("  2. 设置无缓冲输出环境变量")
    print("  3. 确保实时交互式输出")
    print()
    
    # 检查是否在OpenClaw环境中
    is_openclaw = "OPENCLAW" in os.environ or "OPENCLAW_SESSION" in os.environ
    
    if is_openclaw:
        print("检测到OpenClaw环境，推荐使用批处理文件:")
        print("  openclaw_transcribe.bat")
        print()
        print("或使用优化后的命令行:")
        print("  cd D:\\dev\\python\\voiceFunAsr")
        print("  set PYTHONUNBUFFERED=1")
        print("  conda run -n audioProject python -u vocie_mic_fixed_gbk.py")
        print()
        
        # 构建优化命令
        cmd = ["cmd", "/c", "start", "cmd", "/k", 
               "cd /d D:\\dev\\python\\voiceFunAsr && "
               "set PYTHONUNBUFFERED=1 && "
               "conda run -n audioProject python -u vocie_mic_fixed_gbk.py"]
    else:
        # 普通命令行环境
        cmd = ["conda", "run", "-n", "audioProject", "python", "-u", "vocie_mic_fixed_gbk.py"]
    
    print(f"执行命令: {' '.join(cmd[:3]) if is_openclaw else ' '.join(cmd)}")
    print(f"工作目录: D:\\dev\\python\\voiceFunAsr")
    print()
    print("正在启动转录系统...")
    print("注意: 首次启动可能需要几分钟加载模型")
    print("请耐心等待...")
    print("-" * 50)
    
    try:
        if is_openclaw:
            # OpenClaw环境：启动新窗口
            print("正在打开新的命令窗口运行转录系统...")
            print("请在弹出的窗口中查看实时转录输出")
            print()
            print("转录系统将在新窗口中运行，您可以:")
            print("  1. 在新窗口中查看实时转录")
            print("  2. 在新窗口中按 Ctrl+C 停止转录")
            print("  3. 转录文件将自动保存")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=r"D:\dev\python\voiceFunAsr"
            )
            
            print(f"转录进程已启动，PID: {process.pid}")
            print("转录系统正在新窗口中初始化...")
            print()
            print("转录文件将保存到: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
            
            # 等待一段时间让系统启动
            time.sleep(5)
            
            # 显示最新文件
            view_records(count=1)
            
            return 0
            
        else:
            # 普通命令行环境：实时输出模式
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                universal_newlines=True,
                cwd=r"D:\dev\python\voiceFunAsr"
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
                    
                    # 检测关键事件
                    if "检测到语音开始" in line:
                        print("语音检测正常")
                    elif "转录:" in line:
                        print("转录功能正常")
                    elif "保存:" in line:
                        print("文件保存正常")
                    elif "模型加载完成" in line:
                        print("模型加载完成")
                    elif "转录系统已启动" in line:
                        print("转录系统已就绪，请开始说话")
                
                returncode = process.poll()
                if returncode is not None:
                    print(f"转录进程结束，退出码: {returncode}")
                    break
            
            print("-" * 50)
            print(f"总共输出 {line_count} 行")
            
            # 显示最新文件
            view_records(count=1)
            
            return returncode if returncode is not None else 0
        
    except KeyboardInterrupt:
        print("\n用户中断转录")
        if 'process' in locals():
            process.terminate()
        return 0
    except Exception as e:
        print(f"转录启动错误: {e}")
        return 1

def stop_transcription():
    """停止转录"""
    print("停止会议转录")
    print("=" * 50)
    
    # 查找并终止转录进程
    try:
        import psutil
        killed = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any('vocie_mic' in str(arg) for arg in cmdline):
                    print(f"找到转录进程 PID: {proc.info['pid']}")
                    proc.terminate()
                    proc.wait(timeout=5)
                    killed += 1
                    print(f"已终止进程")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
        
        if killed > 0:
            print(f"已停止 {killed} 个转录进程")
        else:
            print("未找到正在运行的转录进程")
        
        # 显示最新文件
        view_records(count=1)
        
        return 0
        
    except ImportError:
        print("需要 psutil 模块来查找进程")
        print("请安装: pip install psutil")
        return 1
    except Exception as e:
        print(f"停止转录错误: {e}")
        return 1

def check_environment(silent=False):
    """检查转录环境"""
    if not silent:
        print("=" * 60)
        print("会议纪要助手 - 环境检查")
        print("=" * 60)
    
    results = []
    
    # 1. 检查Python环境
    python_exe = r"D:\ProgramData\Miniconda3\envs\audioProject\python.exe"
    if not silent:
        print("\n[1] 检查Python环境...")
    
    if os.path.exists(python_exe):
        if not silent:
            print(f"    找到: {python_exe}")
        
        # 获取版本
        try:
            result = subprocess.run(
                [python_exe, "--version"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if not silent:
                print(f"    版本: {result.stdout.strip()}")
            results.append(True)
        except Exception as e:
            if not silent:
                print(f"    无法运行Python: {e}")
            results.append(False)
    else:
        if not silent:
            print(f"    未找到: {python_exe}")
            print("    请确保已创建 audioProject Conda环境")
        results.append(False)
    
    # 2. 检查项目目录
    project_dir = r"D:\dev\python\voiceFunAsr"
    script_gbk = os.path.join(project_dir, "vocie_mic_fixed_gbk.py")
    script_original = os.path.join(project_dir, "vocie_mic_fixed.py")
    
    if not silent:
        print("\n[2] 检查项目目录...")
    
    if os.path.exists(project_dir):
        if not silent:
            print(f"    项目目录: {project_dir}")
        
        # 检查脚本文件
        if os.path.exists(script_gbk):
            if not silent:
                print(f"    脚本文件 (GBK修复版): {os.path.basename(script_gbk)}")
        elif os.path.exists(script_original):
            if not silent:
                print(f"    脚本文件 (原始版): {os.path.basename(script_original)}")
                print("    建议使用GBK修复版以避免编码问题")
        else:
            if not silent:
                print(f"    未找到脚本文件")
            results.append(False)
            return 1
        
        # 检查转录目录
        records_dir = os.path.join(project_dir, "meeting_records")
        if os.path.exists(records_dir):
            if not silent:
                print(f"    转录目录: {os.path.basename(records_dir)}")
        else:
            if not silent:
                print(f"    转录目录不存在，将自动创建")
        
        # 检查模型缓存
        modelscope_dir = r"C:\Users\pengjschina\.cache\modelscope\hub\models\iic"
        if os.path.exists(modelscope_dir):
            if not silent:
                print(f"    模型缓存目录存在")
            # 检查具体模型
            model_dir = os.path.join(modelscope_dir, "speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
            if os.path.exists(model_dir):
                if not silent:
                    print(f"    ASR模型已下载")
            else:
                if not silent:
                    print(f"    ASR模型未下载，首次使用将自动下载")
        else:
            if not silent:
                print(f"    模型缓存目录不存在，首次使用将自动下载模型")
        
        results.append(True)
    else:
        if not silent:
            print(f"    项目目录未找到: {project_dir}")
        results.append(False)
    
    # 3. 检查依赖包
    deps = [
        ('funasr', '语音识别引擎'),
        ('torch', '深度学习框架'),
        ('torchaudio', '音频处理'),
        ('pyaudio', '音频输入输出'),
        ('webrtcvad', '语音活动检测'),
        ('numpy', '数值计算')
    ]
    
    if not silent:
        print("\n[3] 检查依赖包...")
    
    deps_ok = True
    for dep, description in deps:
        try:
            result = subprocess.run(
                [python_exe, "-c", f"import {dep}; print('OK')"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=10
            )
            if result.returncode == 0:
                if not silent:
                    print(f"    {dep} - {description}")
            else:
                if not silent:
                    print(f"    {dep} - 未安装")
                deps_ok = False
        except subprocess.TimeoutExpired:
            if not silent:
                print(f"    {dep} - 检查超时")
        except Exception as e:
            if not silent:
                print(f"    {dep} - 检查失败: {e}")
            deps_ok = False
    
    # 4. 检查音频设备
    if not silent:
        print("\n[4] 检查音频设备...")
    
    audio_ok = True
    try:
        result = subprocess.run(
            [python_exe, "-c", """
import pyaudio
p = pyaudio.PyAudio()
input_devices = []
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if dev_info['maxInputChannels'] > 0:
        input_devices.append((i, dev_info['name']))
p.terminate()
print(f"Found {len(input_devices)} input devices")
for idx, name in input_devices[:3]:  # 显示前3个
    print(f"  [{idx}] {name}")
if len(input_devices) > 3:
    print(f"  ... and {len(input_devices)-3} more")
"""],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        
        if result.returncode == 0:
            if not silent:
                lines = result.stdout.strip().split('\n')
                if lines:
                    print(f"    {lines[0]}")
                    for line in lines[1:]:
                        print(f"    {line}")
        else:
            if not silent:
                print(f"    无法检查音频设备")
            audio_ok = False
            
    except Exception as e:
        if not silent:
            print(f"    音频设备检查失败: {e}")
        audio_ok = False
    
    if not silent:
        # 总结
        print("\n" + "=" * 60)
        
        all_passed = all(results) and deps_ok
        
        if all_passed:
            print("环境检查通过！")
            print("\n可以开始使用会议转录：")
            print("  1. 在OpenClaw中说'开始会议转录'")
            print("  2. 或运行: python run_in_conda.py")
            print("\n转录文件将保存到: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
        else:
            print("环境检查发现问题")
            print("\n需要解决的问题：")
            if not all(results):
                print("  - Python环境或项目目录问题")
            if not deps_ok:
                print("  - 依赖包缺失，请运行: python conda_setup.py")
            if not audio_ok:
                print("  - 音频设备问题，请检查麦克风连接")
            
            print("\n建议操作：")
            print("  1. 运行环境设置: python conda_setup.py")
            print("  2. 或运行PowerShell脚本: .\\setup_and_test.ps1")
        
        print("=" * 60)
    
    # 返回状态码
    all_passed = all(results) and deps_ok
    return 0 if all_passed else 1

def setup_environment():
    """设置转录环境"""
    print("设置转录环境")
    print("=" * 50)
    print()
    
    print("此功能需要手动设置，请按以下步骤操作：")
    print()
    print("1. 创建Conda环境（如果尚未创建）：")
    print("   conda create -n audioProject python=3.8")
    print()
    print("2. 激活环境并安装依赖：")
    print("   conda activate audioProject")
    print("   pip install funasr torch torchaudio pyaudio webrtcvad numpy")
    print()
    print("3. 验证安装：")
    print("   python -c \"import funasr; import pyaudio; print('安装成功')\"")
    print()
    print("4. 确保项目目录存在：")
    print("   D:\\dev\\python\\voiceFunAsr\\")
    print()
    print("5. 可选：运行PowerShell脚本进行完整设置：")
    print("   .\\setup_and_test.ps1")
    print()
    print("完成设置后，运行'检查转录环境'验证配置。")
    
    return 0

def view_records(count=10):
    """查看会议记录"""
    print("查看会议记录")
    print("=" * 50)
    
    records_dir = r"D:\dev\python\voiceFunAsr\meeting_records"
    
    if not os.path.exists(records_dir):
        print(f"转录目录不存在: {records_dir}")
        return 1
    
    # 获取所有转录文件
    files = []
    for f in os.listdir(records_dir):
        if f.startswith('meeting_') and f.endswith('.txt'):
            filepath = os.path.join(records_dir, f)
            mtime = os.path.getmtime(filepath)
            size = os.path.getsize(filepath)
            files.append((f, mtime, size))
    
    if not files:
        print("没有找到转录文件")
        return 0
    
    # 按修改时间排序
    files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"找到 {len(files)} 个转录文件:")
    print()
    
    for i, (filename, mtime, size) in enumerate(files[:count]):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print(f"{i+1}. {filename}")
        print(f"   修改时间: {timestamp}")
        print(f"   文件大小: {size} 字节")
        
        # 显示文件内容预览
        filepath = os.path.join(records_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                lines = content.split('\n')
                if len(lines) > 5:  # 有内容
                    # 找到第一个实际内容行
                    for line in lines:
                        if line.strip() and '=' not in line and '会议实时转写记录' not in line:
                            if len(line) > 50:
                                line = line[:50] + "..."
                            print(f"   内容预览: {line}")
                            break
        except:
            pass
        
        print()
    
    if len(files) > count:
        print(f"... 还有 {len(files) - count} 个文件未显示")
    
    return 0

def open_latest():
    """打开最新会议纪要"""
    print("打开最新会议纪要")
    print("=" * 50)
    
    records_dir = r"D:\dev\python\voiceFunAsr\meeting_records"
    
    if not os.path.exists(records_dir):
        print(f"转录目录不存在: {records_dir}")
        return 1
    
    # 查找最新文件
    latest_file = None
    latest_mtime = 0
    
    for f in os.listdir(records_dir):
        if f.startswith('meeting_') and f.endswith('.txt'):
            filepath = os.path.join(records_dir, f)
            mtime = os.path.getmtime(filepath)
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_file = filepath
    
    if not latest_file:
        print("没有找到转录文件")
        return 1
    
    print(f"最新文件: {os.path.basename(latest_file)}")
    print(f"修改时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest_mtime))}")
    print()
    
    # 显示文件内容
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print("文件内容:")
            print("-" * 50)
            print(content)
            print("-" * 50)
        
        # 询问是否用默认程序打开
        print()
        response = input("是否用默认程序打开此文件？(y/n): ").lower()
        if response == 'y':
            webbrowser.open(latest_file)
            print("已尝试用默认程序打开文件")
        
        return 0
        
    except Exception as e:
        print(f"打开文件错误: {e}")
        return 1

def show_help():
    """显示帮助信息"""
    print("Meeting Transcriber - 会议转录技能")
    print("=" * 60)
    print()
    print("可用命令:")
    print()
    print("  开始会议转录    - 启动实时语音转录")
    print("  停止转录        - 停止转录并保存文件")
    print("  检查转录环境    - 检查 Conda 环境和依赖包")
    print("  设置转录环境    - 配置 Conda 环境和安装依赖")
    print("  查看会议记录    - 列出所有会议转录文件")
    print("  打开最新会议纪要 - 打开最新的会议纪要文件")
    print("  OpenClaw专用转录 - 专为OpenClaw优化的转录")
    print()
    print("转录文件位置: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
    print()
    print("OpenClaw环境问题解决方案:")
    print("  1. 使用'OpenClaw专用转录'命令")
    print("  2. 或运行批处理文件: openclaw_transcribe.bat")
    print("  3. 或运行包装器: python openclaw_wrapper.py")
    print()
    print("基于 FunASR 的实时中文语音识别系统")
    print("专为 Conda audioProject 环境优化")

def openclaw_transcribe():
    """OpenClaw专用转录"""
    print("OpenClaw专用转录")
    print("=" * 60)
    print()
    print("此功能专为解决OpenClaw环境下的转录问题：")
    print("  1. 输出缓冲问题 - 使用无缓冲输出")
    print("  2. 交互问题 - 启动独立窗口")
    print("  3. 编码问题 - 设置正确编码")
    print()
    
    # 检查环境
    env_result = check_environment(silent=True)
    if env_result != 0:
        print("环境检查失败，请先运行'检查转录环境'")
        return 1
    
    print("推荐使用批处理文件启动转录系统...")
    print()
    
    batch_file = os.path.join(os.path.dirname(__file__), "openclaw_transcribe.bat")
    if os.path.exists(batch_file):
        print(f"使用批处理文件: {os.path.basename(batch_file)}")
        print("正在启动转录系统...")
        print()
        
        cmd = ["cmd", "/c", "start", "cmd", "/k", batch_file]
        subprocess.Popen(cmd)
        
        print("[OK] 转录系统已在新窗口中启动")
        print()
        print("请在新窗口中：")
        print("  1. 查看实时转录输出")
        print("  2. 按 Ctrl+C 停止转录")
        print("  3. 转录文件将自动保存")
        print()
        print("转录文件位置: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
        print()
        print("提示: 转录系统启动后，您可以开始说话进行转录")
        
        return 0
    else:
        print(f"批处理文件未找到: {batch_file}")
        print()
        print("备用方案: 使用优化命令行")
        print("  cd D:\\dev\\python\\voiceFunAsr")
        print("  set PYTHONUNBUFFERED=1")
        print("  conda run -n audioProject python -u vocie_mic_fixed_gbk.py")
        
        return 1

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    
    if command in ["开始会议转录", "start"]:
        return start_transcription()
    elif command in ["停止转录", "stop"]:
        return stop_transcription()
    elif command in ["检查转录环境", "check"]:
        return check_environment()
    elif command in ["设置转录环境", "setup"]:
        return setup_environment()
    elif command in ["查看会议记录", "view", "list"]:
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        return view_records(count)
    elif command in ["打开最新会议纪要", "open", "latest"]:
        return open_latest()
    elif command in ["OpenClaw专用转录", "openclaw"]:
        return openclaw_transcribe()
    elif command in ["帮助", "help", "--help", "-h"]:
        show_help()
        return 0
    else:
        print(f"未知命令: {command}")
        print("使用 '帮助' 查看可用命令")
        return 1

if __name__ == "__main__":
    sys.exit(main())