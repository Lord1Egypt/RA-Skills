#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skill Name: LLM-Text-Correct
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: OpenClaw 中文文本纠错脚本
支持：直接文本 / 单个文件 / 文件夹（自动创建新文件/新文件夹）
"""

import sys
import gc
from pathlib import Path
from huggingface_hub import snapshot_download
from logger_manager import LoggerManager
import env_manager
import ensure_package
from config import SKILL_ROOT
from macbert_gpu_refiner import gpu_refiner, MacBertGPURefiner   # ← 新增这行
import argparse
ensure_package.pip("pycorrector", "pycorrector","Corrector")
ensure_package.pip("kenlm")
from pycorrector import Corrector

# 全局模型（只加载一次）
#用people2014corpus_chars.klm + my_custom_confusion.txt 快速初纠（发挥领域专长、速度极快）
model = None #D:/shibing624-chinese-kenlm-klm/people2014corpus_chars.klm #KenLM 是经典的 n-gram 统计语言模型（C++ 实现），天生不支持 GPU
gpu_refiner = None   # 显式声明本模块全局
MODEL_PATH = None   # 将由 argparse 设置
KLM_OVERRIDE = None   # --model-path 参数传入的值
CUSTOM_CONFUSION = str(SKILL_ROOT / 'my_custom_confusion.txt')# 自定义混淆词典（必须存在）,相对路径（放在 scripts/ 同级）或改成绝对路径
MODELS_DIR = SKILL_ROOT / "models"

logger = LoggerManager.setup_logger(logger_name="llm-text-correct")

# ==================== 模型映射（支持别名 + 完整 repo） ====================
MODEL_MAPPING = {
    "shibing624-chinese-kenlm-klm": "shibing624/chinese-kenlm-klm",
}

def download_model(model_name: str, models_dir: Path) -> str:
    """自动下载模型（完全复制自 macbert_gpu_refiner.py，美观错误提示）"""
    if model_name in MODEL_MAPPING:
        repo_id = MODEL_MAPPING[model_name]
        local_dir = models_dir / model_name.replace("/", "_")
    elif "/" in model_name:
        repo_id = model_name
        local_dir = models_dir / model_name.split("/")[-1].replace(":", "_")
    else:
        repo_id = model_name
        local_dir = models_dir / model_name.replace("/", "_")

    if local_dir.exists() and any(local_dir.iterdir()):
        print(f"✅ 模型已存在: {local_dir}", file=sys.stderr)
        return str(local_dir)

    print(f"🔽 正在从 Hugging Face 下载模型: {model_name} → {repo_id}", file=sys.stderr)
    print(f" 保存路径: {local_dir}（当前models目录）", file=sys.stderr)
    local_dir.mkdir(parents=True, exist_ok=True)

    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_dir),
            allow_patterns=["*"]
        )
        print(f"✅ 下载完成！模型路径: {local_dir}", file=sys.stderr)
        return str(local_dir)
    except Exception as e:
        download_url = f"https://huggingface.co/{repo_id}/tree/main"
        
        print("\n" + "="*60, file=sys.stderr)
        print("❌ 模型下载失败", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(f"错误原因: {str(e)}", file=sys.stderr)
        print("\n💡 手动下载方案（推荐，3步搞定）：", file=sys.stderr)
        print(" 1. 打开下面链接（直接复制到浏览器）：", file=sys.stderr)
        print(f" 👉 {download_url}", file=sys.stderr)
        print(" 2. 点击页面右上角 **Download** 按钮（或逐个文件下载）", file=sys.stderr)
        print(" 需要下载全部文件（尤其是 people2014corpus_chars.klm）", file=sys.stderr)
        print(f" 3. 把所有文件放到以下目录：", file=sys.stderr)
        print(f" 📁 {local_dir}", file=sys.stderr)
        print(" 4. 重新运行命令即可（自动识别已存在模型）", file=sys.stderr)
        print("\n📋 你的专属模型下载地址（已为你生成）：", file=sys.stderr)
        print(f" {download_url}", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        
        sys.exit(1)

def init_model():
    """初始化模型（关键逻辑：如果传了 --model-path 则跳过下载）"""
    global model
    if model is not None:
        logger.info(f"🌌 model已加载（复用）")
        return

    if KLM_OVERRIDE:
        klm_path = Path(KLM_OVERRIDE).resolve()
        if not klm_path.exists():
            print(f"❌ 指定模型文件不存在: {klm_path}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ 使用手动指定模型（跳过下载）: {klm_path}", file=sys.stderr)
    else:
        print("🚀 正在检查/下载 KenLM 模型（people2014corpus_chars.klm）...", file=sys.stderr)
        downloaded_dir = download_model("shibing624/chinese-kenlm-klm", MODELS_DIR)
        klm_path = Path(downloaded_dir) / "people2014corpus_chars.klm"
        
        if not klm_path.exists():
            print(f"❌ 未找到 klm 文件: {klm_path}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ 使用自动下载模型: {klm_path}", file=sys.stderr)

    model = Corrector(
        language_model_path=str(klm_path),
        custom_confusion_path_or_dict=CUSTOM_CONFUSION
    )
    print("✅ 模型加载完成！", file=sys.stderr)

def correct_text(text: str, use_refine: bool = False) -> str:
    global model
    init_model()
    results = model.correct_batch([text])
    kenlm_corrected = results[0]['target'] if results else text
    # ────────────────────────────── 日志 ──────────────────────────────
    print("\n" + "═" * 60, file=sys.stderr)
    print("🛠️ KenLM 初纠：", kenlm_corrected[:20] + ("......" if len(kenlm_corrected) > 20 else ""), file=sys.stderr)
    # ──────────────────────────────────────────────────────────────────
    corrected = kenlm_corrected
    
    if use_refine:
        print("🚀 【GPU精修已开启】KenLM初纠 → MacBERT GPU精修", file=sys.stderr)
        global gpu_refiner
        if gpu_refiner is None:
            gpu_refiner = MacBertGPURefiner(CUSTOM_CONFUSION)
        macbert_corrected = gpu_refiner.correct(kenlm_corrected)
        # ────────────────────────────── 日志 ──────────────────────────────
        print("✨ MacBERT 精修：",  macbert_corrected[:20] + ("......" if len(macbert_corrected) > 20 else ""), file=sys.stderr)
        # ──────────────────────────────────────────────────────────────────
        corrected = macbert_corrected
    else:
        print("最终输出  ：", corrected[:20] + ("......" if len(corrected) > 20 else ""), file=sys.stderr)
    print("═" * 60 + "\n", file=sys.stderr)
    return corrected


def process_file(file_path: Path, output_path: Path, use_refine: bool = False):
    """处理单个文件（支持 GPU 精修参数）"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
       
        corrected = correct_text(content, use_refine=use_refine)   # ← 关键修改：传递参数
       
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(corrected)
       
        logger.info(f"✅ 已纠错: {file_path} → {output_path}")
    except Exception as e:
        logger.info(f"❌ 跳过文件 {file_path}: {e}")

def get_text_files(folder: Path):
    """递归获取所有文本文件"""
    extensions = {".txt", ".md", ".py", ".json", ".html", ".csv", ".js", ".css"}
    return [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in extensions]


def main():
    global KLM_OVERRIDE

    parser = argparse.ArgumentParser(description="中文文本纠错工具（KenLM + 可选GPU精修）")
    parser.add_argument('input', nargs='?', default=None,help='需要纠错的文本、文件路径或文件夹路径')
    parser.add_argument('--refine', '-r', action='store_true',help='是否使用 MacBERT GPU 精修（默认不使用）')
    parser.add_argument('--model-path', '-m', type=str, default=None,help='本地 .klm 文件完整路径（传入后跳过自动下载）')
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    KLM_OVERRIDE = args.model_path
    input_path = Path(args.input).resolve()
    use_refine = args.refine   # ← 关键：在这里定义 use_refine

    # 1. 直接文本模式
    if not input_path.exists():
        corrected = correct_text(args.input, use_refine=use_refine)  # ← 修复：传递参数
        logger.info(corrected)
        cleanup()
        return

    # 2. 单个文件模式
    if input_path.is_file():
        output_path = input_path.with_name(f"{input_path.stem}_corrected{input_path.suffix}")
        process_file(input_path, output_path, use_refine=use_refine)  # ← 已修复
        cleanup()
        return

    # 3. 文件夹模式（递归）
    if input_path.is_dir():
        output_dir = input_path.parent / f"{input_path.name}_corrected"
        output_dir.mkdir(exist_ok=True)
       
        files = get_text_files(input_path)
        if not files:
            logger.info("⚠️ 文件夹中没有找到可处理的文本文件")
            return
       
        logger.info(f"🚀 开始处理文件夹，共 {len(files)} 个文件... {'（已开启GPU精修）' if use_refine else ''}")
       
        for file_path in files:
            relative = file_path.relative_to(input_path)
            output_path = output_dir / relative
            process_file(file_path, output_path, use_refine=use_refine)  # ← 已修复
       
        logger.info(f"\n🎉 全部完成！新文件夹已创建：{output_dir}")
        cleanup()
        return

    logger.info("❌ 输入路径无效")


def cleanup():
    """统一清理 KenLM + GPU 精修模型"""
    global model, gpu_refiner
    cleaned = False
   
    if model is not None:
        del model
        model = None
        cleaned = True
   
    if gpu_refiner is not None:
        gpu_refiner.cleanup()
        gpu_refiner = None
        cleaned = True
   
    if cleaned:
        gc.collect()
        print("✅ 全部显存已释放", file=sys.stderr)

if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()
    main()

    