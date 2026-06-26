#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conda 环境配置脚本
专门为 audioProject 虚拟环境配置会议纪要助手技能
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def detect_conda_environment():
    """检测 Conda 环境"""
    print("🔍 检测 Conda 环境")
    print("="*60)
    
    env_info = {}
    
    # 尝试检测 Conda
    try:
        # 方法1: 检查 CONDA_PREFIX 环境变量
        conda_prefix = os.environ.get('CONDA_PREFIX')
        if conda_prefix:
            env_info['conda_prefix'] = conda_prefix
            env_info['detected_by'] = 'CONDA_PREFIX'
        
        # 方法2: 运行 conda info 命令
        result = subprocess.run(
            ['conda', 'info', '--json'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            conda_info = json.loads(result.stdout)
            env_info.update({
                'conda_version': conda_info.get('conda_version'),
                'active_prefix': conda_info.get('active_prefix'),
                'envs': conda_info.get('envs', [])
            })
            env_info['detected_by'] = 'conda info'
    
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        pass
    
    # 检查 audioProject 环境
    project_env = None
    if env_info.get('envs'):
        for env_path in env_info['envs']:
            if 'audioProject' in str(env_path):
                project_env = str(env_path)
                break
    
    env_info['audioProject_path'] = project_env
    
    # 显示检测结果
    if env_info.get('conda_version'):
        print(f"✅ 检测到 Conda: 版本 {env_info['conda_version']}")
    else:
        print("❌ 未检测到 Conda")
    
    if env_info.get('active_prefix'):
        print(f"✅ 当前激活环境: {env_info['active_prefix']}")
    
    if project_env:
        print(f"✅ 找到 audioProject 环境: {project_env}")
    else:
        print("❌ 未找到 audioProject 环境")
    
    return env_info

def get_python_from_env(env_path):
    """获取指定环境的 Python 路径"""
    if not env_path:
        return None
    
    env_path = Path(env_path)
    
    # Windows 路径
    python_paths = [
        env_path / 'python.exe',
        env_path / 'Scripts' / 'python.exe',
    ]
    
    # Unix 路径
    python_paths.extend([
        env_path / 'bin' / 'python',
        env_path / 'bin' / 'python3',
    ])
    
    for path in python_paths:
        if path.exists():
            return str(path)
    
    return None

def test_environment_access():
    """测试环境访问"""
    print("\n🧪 测试环境访问")
    print("="*60)
    
    tests = []
    
    # 测试项目目录
    project_path = Path("D:/dev/python/voiceFunAsr")
    if project_path.exists():
        tests.append(("项目目录", "✅", str(project_path)))
    else:
        tests.append(("项目目录", "❌", "不存在"))
    
    # 测试虚拟环境中的 Python
    env_info = detect_conda_environment()
    python_path = get_python_from_env(env_info.get('audioProject_path'))
    
    if python_path:
        tests.append(("Python 路径", "✅", python_path))
        
        # 测试 Python 版本
        try:
            result = subprocess.run(
                [python_path, '--version'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                tests.append(("Python 版本", "✅", result.stdout.strip()))
            else:
                tests.append(("Python 版本", "❌", "无法获取"))
        except:
            tests.append(("Python 版本", "❌", "执行失败"))
    else:
        tests.append(("Python 路径", "❌", "未找到"))
    
    # 测试依赖包
    if python_path:
        dependencies = ['pyaudio', 'webrtcvad', 'funasr', 'torch']
        for dep in dependencies:
            try:
                result = subprocess.run(
                    [python_path, '-c', f'import {dep}; print(f"{dep} version: OK")'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                if result.returncode == 0:
                    tests.append((f"依赖 {dep}", "✅", "已安装"))
                else:
                    tests.append((f"依赖 {dep}", "❌", "未安装"))
            except:
                tests.append((f"依赖 {dep}", "❌", "检查失败"))
    
    # 显示测试结果
    for name, status, message in tests:
        print(f"{status} {name}: {message}")
    
    return all(status == "✅" for _, status, _ in tests)

def create_conda_config():
    """创建 Conda 环境配置文件"""
    print("\n⚙️ 创建 Conda 环境配置")
    print("="*60)
    
    env_info = detect_conda_environment()
    python_path = get_python_from_env(env_info.get('audioProject_path'))
    
    if not python_path:
        print("❌ 无法获取 Python 路径，配置失败")
        return None
    
    config = {
        "conda_environment": {
            "name": "audioProject",
            "python_path": python_path,
            "env_path": env_info.get('audioProject_path'),
            "conda_version": env_info.get('conda_version'),
            "detected_at": subprocess.run(
                'date /T && time /T',
                shell=True,
                capture_output=True,
                text=True
            ).stdout.strip()
        },
        "project": {
            "path": "D:/dev/python/voiceFunAsr",
            "main_script": "vocie_mic_fixed.py",
            "requirements": "requirements.txt",
            "records_dir": "meeting_records"
        },
        "skill": {
            "use_conda": True,
            "activate_command": f'conda activate audioProject',
            "python_command": python_path,
            "working_directory": "D:/dev/python/voiceFunAsr"
        }
    }
    
    # 保存配置
    config_dir = Path.home() / ".openclaw"
    config_file = config_dir / "meeting_minutes_conda_config.json"
    
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 配置文件已创建: {config_file}")
        return config
    
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return None

def update_skill_for_conda():
    """更新技能以支持 Conda 环境"""
    print("\n🔄 更新技能以支持 Conda 环境")
    print("="*60)
    
    # 1. 更新 SKILL.md 中的元数据
    skill_md_path = Path(__file__).parent / "SKILL.md"
    if skill_md_path.exists():
        content = skill_md_path.read_text(encoding='utf-8')
        
        # 更新 metadata 部分
        if 'metadata:' in content:
            # 添加 Conda 环境信息
            conda_section = '\n  conda_environment: "audioProject"'
            if 'conda_environment' not in content:
                # 在 metadata 部分添加
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('metadata:'):
                        # 在 metadata 块内添加
                        j = i + 1
                        while j < len(lines) and (lines[j].startswith('  ') or lines[j].startswith('}')):
                            j += 1
                        lines.insert(j, conda_section)
                        break
                content = '\n'.join(lines)
        
        skill_md_path.write_text(content, encoding='utf-8')
        print("✅ 更新了 SKILL.md 元数据")
    
    # 2. 创建 Conda 专用的启动脚本
    conda_script = Path(__file__).parent / "start_with_conda.bat"
    conda_content = """@echo off
REM 会议纪要助手 - Conda 环境启动脚本
REM 使用 audioProject 虚拟环境

echo 🎙️ 会议纪要助手 - Conda 版本
echo ========================================

REM 激活 Conda 环境
call conda activate audioProject
if errorlevel 1 (
    echo ❌ 无法激活 audioProject 环境
    pause
    exit /b 1
)

echo ✅ 已激活 audioProject 环境

REM 进入项目目录
cd /d D:\\dev\\python\\voiceFunAsr
if errorlevel 1 (
    echo ❌ 无法进入项目目录
    pause
    exit /b 1
)

echo ✅ 已进入项目目录

REM 运行转录脚本
echo 🚀 启动会议转录...
python vocie_mic_fixed.py

REM 如果脚本结束，暂停显示结果
pause
"""
    
    conda_script.write_text(conda_content, encoding='utf-8')
    print(f"✅ 创建了 Conda 启动脚本: {conda_script}")
    
    # 3. 更新主技能脚本以支持 Conda
    main_script = Path(__file__).parent / "meeting_minutes.py"
    if main_script.exists():
        content = main_script.read_text(encoding='utf-8')
        
        # 添加 Conda 环境检测
        conda_detection_code = '''
    def _get_conda_python(self):
        """获取 Conda 环境中的 Python 路径"""
        try:
            # 检查配置文件
            conda_config = self.config_dir / "meeting_minutes_conda_config.json"
            if conda_config.exists():
                with open(conda_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    python_path = config.get('skill', {}).get('python_command')
                    if python_path and Path(python_path).exists():
                        return python_path
            
            # 尝试自动检测
            env_paths = [
                Path.home() / "miniconda3" / "envs" / "audioProject",
                Path.home() / "anaconda3" / "envs" / "audioProject",
                Path("D:") / "miniconda3" / "envs" / "audioProject",
                Path("D:") / "anaconda3" / "envs" / "audioProject",
            ]
            
            for env_path in env_paths:
                python_exe = env_path / "python.exe"
                if python_exe.exists():
                    return str(python_exe)
                
                python_bin = env_path / "bin" / "python"
                if python_bin.exists():
                    return str(python_bin)
        
        except:
            pass
        
        return None
'''
        
        # 在 MeetingMinutesAssistant 类中添加方法
        if 'def _get_conda_python(self):' not in content:
            class_def_pos = content.find('class MeetingMinutesAssistant:')
            if class_def_pos != -1:
                # 找到第一个方法定义的位置
                method_start = content.find('def ', class_def_pos)
                if method_start != -1:
                    content = content[:method_start] + conda_detection_code + content[method_start:]
                    print("✅ 在主脚本中添加了 Conda 环境检测")
        
        main_script.write_text(content, encoding='utf-8')
    
    return True

def create_conda_requirements():
    """创建 Conda 环境要求文件"""
    print("\n📋 创建 Conda 环境要求")
    print("="*60)
    
    requirements = """# 会议纪要助手 - Conda 环境要求
# audioProject 虚拟环境应包含以下包

# 核心依赖
- python>=3.8
- pip

# 通过 pip 安装的包
- pyaudio
- webrtcvad
- sounddevice
- funasr>=1.0.27
- torch>=1.13.1
- torchaudio>=0.13.1

# 可选：用于增强功能
- openai-whisper
- pandas
- scikit-learn

# 环境配置说明
# 1. 创建环境: conda create -n audioProject python=3.8
# 2. 激活环境: conda activate audioProject
# 3. 安装依赖: pip install -r requirements.txt
# 4. 验证安装: python -c "import funasr; print('FunASR OK')"
"""
    
    req_file = Path(__file__).parent / "conda_requirements.txt"
    req_file.write_text(requirements, encoding='utf-8')
    print(f"✅ 创建了 Conda 环境要求文件: {req_file}")
    
    return True

def show_conda_usage():
    """显示 Conda 环境使用说明"""
    print("\n🚀 Conda 环境使用说明")
    print("="*60)
    
    print("1. 激活 Conda 环境:")
    print("   conda activate audioProject")
    print()
    
    print("2. 使用 Conda 启动脚本:")
    print("   start_with_conda.bat")
    print()
    
    print("3. 在 Conda 环境中测试技能:")
    print("   conda activate audioProject")
    print("   cd D:/dev/python/voiceFunAsr")
    print("   python vocie_mic_fixed.py")
    print()
    
    print("4. 在 OpenClaw 中使用（自动检测）:")
    print("   技能会自动检测并使用 Conda 环境")
    print("   无需手动激活环境")
    print()
    
    print("5. 手动指定 Python 路径:")
    print("   python meeting_minutes.py --python D:/miniconda3/envs/audioProject/python.exe")
    print()
    
    print("📁 重要路径:")
    print("   项目目录: D:/dev/python/voiceFunAsr")
    print("   Conda 环境: audioProject")
    print("   技能目录: C:/Users/pengjschina/.openclaw/workspace/skills/meeting-minutes-assistant")
    print("   配置文件: ~/.openclaw/meeting_minutes_conda_config.json")

def main():
    """主函数"""
    print("🎙️ 会议纪要助手 - Conda 环境配置")
    print("="*60)
    
    # 检测环境
    env_info = detect_conda_environment()
    
    if not env_info.get('audioProject_path'):
        print("\n⚠️  警告: 未找到 audioProject 环境")
        print("请确保:")
        print("1. Conda 已安装并配置")
        print("2. audioProject 环境已创建")
        print("3. 环境包含必要的依赖包")
        print("\n是否继续配置？(y/n): ", end='')
        if input().lower() != 'y':
            return
    
    # 测试环境访问
    if not test_environment_access():
        print("\n⚠️  环境测试有失败项")
        print("是否继续配置？(y/n): ", end='')
        if input().lower() != 'y':
            return
    
    # 创建配置
    config = create_conda_config()
    if not config:
        print("\n❌ 配置创建失败")
        return
    
    # 更新技能
    if not update_skill_for_conda():
        print("\n⚠️  技能更新有警告")
    
    # 创建要求文件
    create_conda_requirements()
    
    # 显示使用说明
    show_conda_usage()
    
    print("\n" + "="*60)
    print("✅ Conda 环境配置完成！")
    print("="*60)
    
    print("\n💡 下一步:")
    print("1. 测试环境: conda activate audioProject && python test_optimization.py")
    print("2. 使用 Conda 脚本: start_with_conda.bat")
    print("3. 在 OpenClaw 中测试: 说'开始会议转录'")

if __name__ == "__main__":
    main()