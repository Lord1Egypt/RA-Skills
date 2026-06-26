#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: LLM-Text-Correct
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 这段代码是一个 Python 脚本的环境初始化与自动化配置模块。
它主要用于确保程序在正确的 Python 版本和虚拟环境中运行，并能根据用户的硬件（特别是 NVIDIA GPU）自动安装适配的 PyTorch 及其相关音频处理依赖。
该脚本充当了程序的“引导加载程序”（Bootstrapper），主要完成以下四项任务：
1、路径与日志管理：整合项目路径配置并初始化日志系统。
2、环境强制检查：严格限制 Python 运行版本（3.10 ~ 3.12）。
3、智能硬件探测：通过解析 nvidia-smi 自动识别 GPU、驱动版本及 CUDA 版本。
4、自动化依赖部署：根据硬件情况，自动安装对应版本的 PyTorch（GPU/CPU 版）及音频处理库（audio-separator, librosa 等）。
"""

import os
import sys
import subprocess
import venv
import shutil
import re
from pathlib import Path
from logger_manager import LoggerManager
from config import ProjectPaths,SCRIPT_PATH, SKILL_ROOT,VENV_DIR,LOG_DIR,MODEL_DIR

# 方式 A：直接使用导出的常量
print(f"代码目录: {SCRIPT_PATH}")
print(f"根目录是: {SKILL_ROOT}")
print(f"虚拟环境路径: {VENV_DIR}")
print(f"日志路径: {LOG_DIR}")
print(f"模型路径: {MODEL_DIR}")

# 方式 B：使用辅助方法获取更深的路径
model_path = ProjectPaths.get_subpath("models", "v1", "model.pkl")
print(f"模型保存路径: {model_path}")

# --- 日志系统初始化 ---
# 将配置好的 LOG_DIR 传给 LoggerManager
logger = LoggerManager.setup_logger(logger_name="llm-text-correct")

def check_python_version():
    """严格检测 Python 版本，只支持 3.10 ~ 3.12"""
    major = sys.version_info.major
    minor = sys.version_info.minor
    if major != 3 or minor < 10 or minor > 12:
        logger.error(f"不支持的 Python 版本: {major}.{minor}。本技能仅支持 Python 3.10 ~ 3.12")
        print(f"\n❌ 错误：Python 版本必须是 3.10 ~ 3.12")
        print(f"当前版本: {major}.{minor}")
        print("请安装 Python 3.10、3.11 或 3.12 后再运行本技能。")
        sys.exit(1)
    logger.info(f"✅ Python 版本检测通过: {major}.{minor}")

def is_torch_gpu_installed(python_exe):
    """检测虚拟环境中是否安装了 GPU 版本 PyTorch"""
    try:
        result = subprocess.run(
            [str(python_exe), "-c",
             "import torch; print(torch.version.cuda or 'cpu')"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            cuda_version = result.stdout.strip()
            if cuda_version.lower() != "cpu" and cuda_version != "":
                return True
    except Exception:
        pass
    return False

def setup_venv():
    """自动创建虚拟环境 + 切换到 venv 执行主脚本（强化防递归 + 绝对路径版）"""
    # ==================== 防递归保护 ====================
    if os.getenv("RUNNING_IN_VENV") == "true":
        logger.info(f"✅ 已成功在虚拟环境中运行: {sys.executable}")
        return

    # 确定虚拟环境 python 路径
    if os.name == "nt":  # Windows
        venv_python = VENV_DIR / "Scripts" / "python.exe"
    else:
        venv_python = VENV_DIR / "bin" / "python"

    # 当前已经在虚拟环境中（大小写不敏感）
    if Path(sys.executable).resolve() == venv_python.resolve():
        logger.info(f"✅ 当前已在虚拟环境中运行")
        os.environ["RUNNING_IN_VENV"] = "true"
        return

    # ==================== 创建虚拟环境 + 安装依赖（保留你原来的全部逻辑） ====================
    if not VENV_DIR.exists():
        logger.info(f"正在创建虚拟环境: {VENV_DIR}")
        venv.create(VENV_DIR, with_pip=True)
        logger.info("虚拟环境创建成功")

        logger.info("正在升级 pip...")
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])

    # ==================== 检查 PyTorch GPU 是否已安装 ====================
    if Path(venv_python).exists() and is_torch_gpu_installed(venv_python):
        logger.info("✅ 虚拟环境中已有 GPU 版 PyTorch，无需重新安装")
    else:
        logger.info("ℹ️ 虚拟环境中 PyTorch 不是 GPU 版本，将重新安装 GPU 版")
        # ==================== 修复版 GPU 检测（解析完整 nvidia-smi） ====================
        logger.info("检测 GPU 和 CUDA 版本...")
        has_gpu = False
        cuda_ver = "unknown"
        driver = "unknown"

        nvidia_smi_path = shutil.which("nvidia-smi")
        if not nvidia_smi_path:
            possible_paths = [
                r"C:\Windows\System32\nvidia-smi.exe",  # 你的路径
                r"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe",
                "/usr/bin/nvidia-smi",  # Ubuntu
                "/usr/local/cuda/bin/nvidia-smi",
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    nvidia_smi_path = p
                    break

        if nvidia_smi_path:
            try:
                # 运行完整 nvidia-smi 并解析输出
                result = subprocess.run(
                    [nvidia_smi_path],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0 and result.stdout:
                    output = result.stdout
                    # 提取 Driver Version
                    driver_match = re.search(r"Driver Version:\s*([\d.]+)", output)
                    if driver_match:
                        driver = driver_match.group(1)
                    # 提取 CUDA Version
                    cuda_match = re.search(r"CUDA Version:\s*([\d.]+)", output)
                    if cuda_match:
                        cuda_ver = cuda_match.group(1)
                    # 提取 GPU Name（确认有 GPU）
                    if "NVIDIA" in output and cuda_ver != "unknown":
                        has_gpu = True
                        #has_gpu = False#FFmpeg使用CPU即可
                        logger.info(f"✅ 检测到 NVIDIA GPU！驱动: {driver}，CUDA: {cuda_ver}")
            except Exception as e:
                logger.warning(f"nvidia-smi 执行失败: {e}")

        # ==================== 根据 CUDA 版本选 wheel ====================
        index_url = "https://download.pytorch.org/whl/cpu"  # 默认 CPU
        use_gpu = False
        if has_gpu:
            major_minor = '.'.join(cuda_ver.split('.')[:2])
            cuda_map = {
                "12.6": "cu126",
                "12.7": "cu126",
                "12.8": "cu128",
                "12.9": "cu128",
                "13.0": "cu129",
                "13.1": "cu129",
            }
            wheel = cuda_map.get(major_minor, "cu121")  # 默认 cu121 for 13+
            index_url = f"https://download.pytorch.org/whl/{wheel}"
            use_gpu = True
            logger.info(f"🎯 CUDA {cuda_ver} → 使用 {wheel} GPU 加速版")

        else:
            logger.info("ℹ️ 未检测到 GPU，使用 CPU 版")

        # 安装 PyTorch
        logger.info("正在安装 PyTorch（~2-3GB，请耐心等待）...")
        subprocess.check_call([
            str(venv_python), "-m", "pip", "install", "torch", "torchvision", "torchaudio",
            "--index-url", index_url
        ])

        # 验证
        verify = subprocess.run([
            str(venv_python), "-c",
            "import torch; "
            "print('GPU可用' if torch.cuda.is_available() else '仅CPU'); "
            "print('设备:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
        ], capture_output=True, text=True, timeout=30)
        logger.info(f"PyTorch 验证结果: {verify.stdout.strip()}")

        # 安装 audio-separator + librosa（你提到的）
        if use_gpu:
            logger.info("安装 audio-separator GPU 版 + librosa...")
            subprocess.check_call([str(venv_python), "-m", "pip", "install", "audio-separator[gpu]", "librosa"])
        else:
            logger.info("安装 audio-separator CPU 版 + librosa...")
            subprocess.check_call([str(venv_python), "-m", "pip", "install", "audio-separator[cpu]", "librosa"])

        subprocess.check_call([str(venv_python), "-m", "pip", "install", "pydub"])
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "huggingface-hub[tqdm]"])
        
        logger.info("✅ 虚拟环境及所有依赖安装完成！")

    # ==================== 关键修复：重新启动主脚本 ====================
    logger.info("🔄 正在切换到虚拟环境重新执行脚本...")

    # 自动获取主脚本绝对路径（最稳健方式）
    main_script = Path(sys.argv[0]).resolve()
    
    # 如果上面没找到（极少数情况），尝试从 env_manager 所在目录向上找
    if not main_script.exists() or "env_manager" in main_script.name.lower():
        possible_paths = [
            Path.cwd() / "scripts" / "correct_text.py",
            Path.cwd() / "correct_text.py",
            Path(__file__).parent.parent / "scripts" / "correct_text.py",   # 项目根目录/scripts/correct_text.py
        ]
        for p in possible_paths:
            if p.exists():
                main_script = p
                break

    if not main_script.exists():
        logger.error(f"❌ 无法找到主脚本路径: {main_script}")
        logger.error(f"当前 sys.argv[0] = {sys.argv[0]}")
        logger.error(f"当前工作目录 = {Path.cwd()}")
        sys.exit(1)

    # 传递环境变量防止递归
    env = os.environ.copy()
    env["RUNNING_IN_VENV"] = "true"

    logger.info(f"   当前Python: {sys.executable}")
    logger.info(f"   目标Python: {venv_python}")
    logger.info(f"   主脚本路径: {main_script}")

    # 启动新进程（保持当前工作目录）
    result = subprocess.run(
        [str(venv_python), str(main_script)] + sys.argv[1:],
        env=env,
        cwd=Path.cwd(),      # ← 关键！保证相对路径正确
    )

    sys.exit(result.returncode)