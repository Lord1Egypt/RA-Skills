#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
会议纪要助手 - 环境检查工具
验证Conda环境和依赖包
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python():
    """检查Python可执行文件"""
    python_exe = Path(r"D:\ProgramData\Miniconda3\envs\audioProject\python.exe")
    
    print("\n[1] 检查Python环境...")
    if python_exe.exists():
        print(f"    ✅ 找到: {python_exe}")
        
        # 获取版本
        try:
            result = subprocess.run(
                [str(python_exe), "--version"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            print(f"    ✅ 版本: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"    ❌ 无法运行Python: {e}")
            return False
    else:
        print(f"    ❌ 未找到: {python_exe}")
        print("    请确保已创建 audioProject Conda环境")
        return False

def check_project():
    """检查项目目录"""
    project_dir = Path(r"D:\dev\python\voiceFunAsr")
    script_gbk = project_dir / "vocie_mic_fixed_gbk.py"  # 使用修复后的脚本
    script_original = project_dir / "vocie_mic_fixed.py"
    
    print("\n[2] 检查项目目录...")
    if project_dir.exists():
        print(f"    ✅ 项目目录: {project_dir}")
        
        # 检查脚本文件
        if script_gbk.exists():
            print(f"    ✅ 脚本文件 (GBK修复版): {script_gbk.name}")
        elif script_original.exists():
            print(f"    ⚠️  脚本文件 (原始版): {script_original.name}")
            print("    建议使用GBK修复版以避免编码问题")
        else:
            print(f"    ❌ 未找到脚本文件")
            return False
        
        # 检查转录目录
        records_dir = project_dir / "meeting_records"
        if records_dir.exists():
            print(f"    ✅ 转录目录: {records_dir.name}")
        else:
            print(f"    ⚠️  转录目录不存在，将自动创建")
        
        # 检查模型缓存
        modelscope_dir = Path(r"C:\Users\pengjschina\.cache\modelscope\hub\models\iic")
        if modelscope_dir.exists():
            print(f"    ✅ 模型缓存目录存在")
            # 检查具体模型
            model_dir = modelscope_dir / "speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
            if model_dir.exists():
                print(f"    ✅ ASR模型已下载")
            else:
                print(f"    ⚠️  ASR模型未下载，首次使用将自动下载")
        else:
            print(f"    ⚠️  模型缓存目录不存在，首次使用将自动下载模型")
        
        return True
    else:
        print(f"    ❌ 项目目录未找到: {project_dir}")
        return False

def check_dependencies():
    """检查Python依赖包"""
    python_exe = r"D:\ProgramData\Miniconda3\envs\audioProject\python.exe"
    deps = [
        ('funasr', '语音识别引擎'),
        ('torch', '深度学习框架'),
        ('torchaudio', '音频处理'),
        ('pyaudio', '音频输入输出'),
        ('webrtcvad', '语音活动检测'),
        ('numpy', '数值计算')
    ]
    
    print("\n[3] 检查依赖包...")
    
    all_ok = True
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
                print(f"    ✅ {dep} - {description}")
            else:
                print(f"    ❌ {dep} - 未安装")
                all_ok = False
        except subprocess.TimeoutExpired:
            print(f"    ⚠️  {dep} - 检查超时")
        except Exception as e:
            print(f"    ❌ {dep} - 检查失败: {e}")
            all_ok = False
    
    return all_ok

def check_audio_devices():
    """检查音频设备"""
    python_exe = r"D:\ProgramData\Miniconda3\envs\audioProject\python.exe"
    
    print("\n[4] 检查音频设备...")
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
            lines = result.stdout.strip().split('\n')
            if lines:
                print(f"    {lines[0]}")
                for line in lines[1:]:
                    print(f"    {line}")
            return True
        else:
            print(f"    ❌ 无法检查音频设备")
            return False
            
    except Exception as e:
        print(f"    ❌ 音频设备检查失败: {e}")
        return False

def main():
    print("=" * 60)
    print("会议纪要助手 - 环境检查")
    print("=" * 60)
    
    results = []
    
    # 运行检查
    results.append(check_python())
    results.append(check_project())
    deps_ok = check_dependencies()
    audio_ok = check_audio_devices()
    
    # 总结
    print("\n" + "=" * 60)
    
    all_passed = all(results) and deps_ok
    
    if all_passed:
        print("✅ 环境检查通过！")
        print("\n可以开始使用会议转录：")
        print("  1. 在OpenClaw中说'开始会议转录'")
        print("  2. 或运行: python run_in_conda.py")
        print("\n转录文件将保存到: D:\\dev\\python\\voiceFunAsr\\meeting_records\\")
    else:
        print("⚠️ 环境检查发现问题")
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
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())