#!/usr/bin/env python3
"""
voice_trainer.py — 声音模型一键训练工具（Phase 2）

自动完成 GPT-SoVITS 的完整训练流程：
  预训练模型下载 → 文本特征提取 → HuBERT 特征提取 → 语义特征提取 → SoVITS 微调 → GPT 微调

用户只需提供预处理后的 WAV 文件和标注文件，一条命令完成全部训练。

前置条件：
  1. GPT-SoVITS 已 clone 到项目目录下（或设置 GPT_SOVITS_DIR 环境变量）
  2. 已通过 voice_preprocessor.py 生成干净 WAV 文件
  3. 已通过 --action prepare 生成 Whisper 标注
  4. RTX 4080S / 3060 12GB 或更高显卡

用法：
  # 一键完成：准备数据 + 训练（最简单）
  python voice_trainer.py --action full --slug grandpa --audio-dir ./processed/

  # 分步执行
  python voice_trainer.py --action prepare --slug grandpa --audio-dir ./processed/
  python voice_trainer.py --action train   --slug grandpa
  python voice_trainer.py --action status  --slug grandpa
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEMORIALS_DIR = os.path.join(PROJECT_ROOT, "memorials")
DEFAULT_SOVITS_DIR = os.path.join(PROJECT_ROOT, "GPT-SoVITS")

# 训练版本（v2 是当前平衡最好的版本）
TRAIN_VERSION = "v2"


def get_sovits_dir() -> str:
    env_dir = os.environ.get("GPT_SOVITS_DIR")
    if env_dir and os.path.isdir(env_dir):
        return env_dir
    if os.path.isdir(DEFAULT_SOVITS_DIR):
        return DEFAULT_SOVITS_DIR
    return ""


def voice_dir(slug: str) -> str:
    return os.path.join(MEMORIALS_DIR, slug, "voice")


def training_dir(slug: str) -> str:
    return os.path.join(voice_dir(slug), "training_data")


def python_exec() -> str:
    return sys.executable


# ── 预训练模型下载 ───────────────────────────��────────────────────────────────

def ensure_pretrained_models():
    """确保预训练模型已下载。"""
    sovits_dir = get_sovits_dir()
    if not sovits_dir:
        print("[x] GPT-SoVITS 未安装")
        return False

    pretrained_dir = os.path.join(sovits_dir, "GPT_SoVITS", "pretrained_models")

    # v2 需要的文件
    required = {
        "chinese-roberta-wwm-ext-large": "BERT 模型",
        "chinese-hubert-base": "HuBERT 模型",
        "gsv-v2final-pretrained": "GPT-SoVITS v2 预训练权重",
    }

    missing = []
    for name, desc in required.items():
        path = os.path.join(pretrained_dir, name)
        if not os.path.isdir(path):
            missing.append((name, desc))

    if not missing:
        print("[ok] 预训练模型已就绪")
        return True

    print(f"[!] 缺少 {len(missing)} 个预训练模型，正在下载...")

    # 使用 modelscope 下载（国内速度快）
    try:
        from modelscope import snapshot_download
        model_map = {
            "chinese-roberta-wwm-ext-large": "AI-ModelScope/chinese-roberta-wwm-ext-large",
            "chinese-hubert-base": "AI-ModelScope/chinese-hubert-base",
            "gsv-v2final-pretrained": "lj1995/GPT-SoVITS",
        }
        for name, desc in missing:
            model_id = model_map.get(name)
            if model_id:
                print(f"  下载 {desc} ({model_id})...")
                dst = os.path.join(pretrained_dir, name)
                snapshot_download(model_id, local_dir=dst)
                print(f"  [ok] {name}")
        return True
    except ImportError:
        pass

    # 如果 modelscope 不可用，尝试 huggingface
    try:
        from huggingface_hub import snapshot_download
        hf_map = {
            "chinese-roberta-wwm-ext-large": "hfl/chinese-roberta-wwm-ext-large",
            "chinese-hubert-base": "TencentGameMate/chinese-hubert-base",
            "gsv-v2final-pretrained": "lj1995/GPT-SoVITS",
        }
        for name, desc in missing:
            model_id = hf_map.get(name)
            if model_id:
                print(f"  下载 {desc} ({model_id})...")
                dst = os.path.join(pretrained_dir, name)
                snapshot_download(model_id, local_dir=dst)
                print(f"  [ok] {name}")
        return True
    except ImportError:
        pass

    print("[x] 无法自动下载预训练模型")
    print("  请手动下载或安装 modelscope: pip install modelscope")
    for name, desc in missing:
        print(f"  缺少: {pretrained_dir}/{name} ({desc})")
    return False


# ── Prepare ────────────────────────────────────────────────────────────────��──

def action_prepare(slug: str, audio_dir: str):
    """准备训练数据：收集 WAV → 训练目录 + Whisper 标注。"""
    tdir = training_dir(slug)
    wavs_dir = os.path.join(tdir, "wavs")
    os.makedirs(wavs_dir, exist_ok=True)

    wavs = sorted([f for f in os.listdir(audio_dir) if f.lower().endswith(".wav")])
    if not wavs:
        print(f"[x] {audio_dir} 中没有 WAV 文件")
        return False

    print(f"[1/2] 收集 {len(wavs)} 个 WAV 文件...")
    total_dur = 0
    manifest = []

    for wav in wavs:
        src = os.path.join(audio_dir, wav)
        dst = os.path.join(wavs_dir, wav)
        shutil.copy2(src, dst)
        try:
            import soundfile as sf
            dur = sf.info(src).duration
        except Exception:
            dur = 0
        total_dur += dur
        manifest.append({"file": wav, "duration": round(dur, 2)})

    with open(os.path.join(tdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"slug": slug, "total_files": len(wavs),
                    "total_duration_seconds": round(total_dur, 1), "files": manifest},
                   f, ensure_ascii=False, indent=2)

    # Whisper 标注
    annotation_path = os.path.join(tdir, "annotations.list")
    print(f"[2/2] Whisper 标注 {len(wavs)} 条音频...")
    try:
        import whisper
        model = whisper.load_model("small")
        annotations = []
        for i, wav in enumerate(wavs, 1):
            wav_path = os.path.join(wavs_dir, wav)
            result = model.transcribe(wav_path, language="zh", verbose=False)
            text = result["text"].strip()
            lang = result.get("language", "zh")
            annotations.append(f"{wav_path}|{slug}|{lang}|{text}")
            if i % 50 == 0 or i == len(wavs):
                print(f"  [{i}/{len(wavs)}] 已标注")

        with open(annotation_path, "w", encoding="utf-8") as f:
            f.write("\n".join(annotations))
        print(f"  标注完成: {len(annotations)} 条")
    except ImportError:
        print("[x] 未安装 whisper: pip install openai-whisper")
        return False

    print(f"\n[ok] 训练数据准备完毕: {len(wavs)} 条, {total_dur:.0f}秒 ({total_dur/60:.1f}分钟)")
    return True


# ── Train (一键) ──────────────────────────────────────────────────────────────

def _check_transcription_quality(annotation_path: str) -> float:
    """
    检测 Whisper 转录质量（0-1 分）。
    用于判断是否应该微调 GPT（方言/低质量转录时跳过）。
    """
    try:
        with open(annotation_path, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception:
        return 0.0

    if not lines:
        return 0.0

    good = 0
    for line in lines:
        parts = line.split("|")
        if len(parts) < 4:
            continue
        text = parts[3]
        # 判断标准：纯中文字符占比高、没有乱码、长度合理
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(text.replace(" ", ""))
        if total_chars > 0 and chinese_chars / total_chars > 0.7 and 2 <= len(text) <= 200:
            good += 1

    score = good / len(lines) if lines else 0.0
    return score


def action_train(slug: str, batch_size_s2: int = 16, epochs_s2: int = 10,
                 batch_size_s1: int = 8, epochs_s1: int = 15,
                 skip_gpt: bool = False, force_gpt: bool = False):
    """
    一键执行完整 GPT-SoVITS 训练流程。

    步骤：
    1. 检查预训练模型
    2. 1-get-text: 提取文本/BERT 特征
    3. 2-get-hubert-wav32k: 提取 HuBERT 音频特征
    4. 3-get-semantic: 提取语义 token
    5. SoVITS 微调 (s2_train.py) — 必须
    6. GPT 微调 (s1_train.py) — 可选（转录质量差时自动跳过）
    """
    sovits_dir = get_sovits_dir()
    if not sovits_dir:
        print("[x] GPT-SoVITS 未安装")
        return False

    tdir = training_dir(slug)
    annotation_path = os.path.join(tdir, "annotations.list")
    wavs_dir = os.path.join(tdir, "wavs")

    if not os.path.exists(annotation_path):
        print(f"[x] 标注文件不存在，请先运行 --action prepare")
        return False

    exp_name = slug
    exp_root = os.path.join(sovits_dir, "logs")
    exp_dir = os.path.join(exp_root, exp_name)
    os.makedirs(exp_dir, exist_ok=True)

    py = python_exec()
    version = TRAIN_VERSION

    # 预训练模型路径
    pretrained = os.path.join(sovits_dir, "GPT_SoVITS", "pretrained_models")
    bert_dir = os.path.join(pretrained, "chinese-roberta-wwm-ext-large")
    hubert_dir = os.path.join(pretrained, "chinese-hubert-base")
    s2G_path = os.path.join(pretrained, "gsv-v2final-pretrained", "s2G2333k.pth")
    s2D_path = os.path.join(pretrained, "gsv-v2final-pretrained", "s2D2333k.pth")
    s1_ckpt = os.path.join(pretrained, "gsv-v2final-pretrained",
                           "s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt")

    # Step 0: 检查预训练模型
    print("=" * 60)
    print(f"  GPT-SoVITS 一键训练 - {slug}")
    print("=" * 60)

    if not ensure_pretrained_models():
        return False

    # 公共环境：确保 GPT-SoVITS 内部模块可 import
    sovits_pythonpath = os.path.join(sovits_dir, "GPT_SoVITS")
    base_env = os.environ.copy()
    existing_pp = base_env.get("PYTHONPATH", "")
    base_env["PYTHONPATH"] = f"{sovits_dir}{os.pathsep}{sovits_pythonpath}{os.pathsep}{existing_pp}"
    base_env["PYTHONIOENCODING"] = "utf-8"

    # Step 1: 1-get-text (BERT 特征提取)
    print(f"\n[Step 1/6] 提取文本/BERT 特征...")
    env1 = base_env.copy()
    env1.update({
        "inp_text": annotation_path,
        "inp_wav_dir": wavs_dir,
        "exp_name": exp_name,
        "opt_dir": exp_dir,
        "bert_pretrained_dir": bert_dir,
        "i_part": "0",
        "all_parts": "1",
        "_CUDA_VISIBLE_DEVICES": "0",
        "is_half": "True",
        "version": version,
    })
    r = subprocess.run(
        [py, "-s", "GPT_SoVITS/prepare_datasets/1-get-text.py"],
        cwd=sovits_dir, env=env1, timeout=600
    )
    if r.returncode != 0:
        print(f"  [x] Step 1 failed (returncode={r.returncode})")
        return False
    # 合并输出
    txt_parts = os.path.join(exp_dir, "2-name2text-0.txt")
    txt_final = os.path.join(exp_dir, "2-name2text.txt")
    if os.path.exists(txt_parts):
        shutil.move(txt_parts, txt_final)
    print(f"  [ok] 文本特征提取完成")

    # Step 2: 2-get-hubert-wav32k (HuBERT 特征)
    print(f"\n[Step 2/6] 提取 HuBERT 音频特征...")
    ssl_dir = os.path.join(hubert_dir)
    env2 = base_env.copy()
    env2.update({
        "inp_text": annotation_path,
        "inp_wav_dir": wavs_dir,
        "exp_name": exp_name,
        "opt_dir": exp_dir,
        "cnhubert_base_dir": ssl_dir,
        "i_part": "0",
        "all_parts": "1",
        "_CUDA_VISIBLE_DEVICES": "0",
        "is_half": "True",
        "version": version,
    })
    r = subprocess.run(
        [py, "-s", "GPT_SoVITS/prepare_datasets/2-get-hubert-wav32k.py"],
        cwd=sovits_dir, env=env2, timeout=1200
    )
    if r.returncode != 0:
        print(f"  [x] Step 2 failed (returncode={r.returncode})")
        return False
    print(f"  [ok] HuBERT 特征提取完成")

    # Step 3: 3-get-semantic (语义 token)
    print(f"\n[Step 3/6] 提取语义 token...")
    env3 = base_env.copy()
    env3.update({
        "inp_text": annotation_path,
        "inp_wav_dir": wavs_dir,
        "exp_name": exp_name,
        "opt_dir": exp_dir,
        "pretrained_s2G": s2G_path,
        "s2config_path": os.path.join(sovits_dir, "GPT_SoVITS", "configs", "s2.json"),
        "i_part": "0",
        "all_parts": "1",
        "_CUDA_VISIBLE_DEVICES": "0",
        "is_half": "True",
        "version": version,
    })
    r = subprocess.run(
        [py, "-s", "GPT_SoVITS/prepare_datasets/3-get-semantic.py"],
        cwd=sovits_dir, env=env3, timeout=1200
    )
    if r.returncode != 0:
        print(f"  [x] Step 3 failed (returncode={r.returncode})")
        return False
    print(f"  [ok] 语义 token 提取完成")

    # Step 4: SoVITS 微调
    print(f"\n[Step 4/6] SoVITS 微调 (batch={batch_size_s2}, epochs={epochs_s2})...")
    s2_config_template = os.path.join(sovits_dir, "GPT_SoVITS", "configs", "s2.json")
    with open(s2_config_template) as f:
        s2_config = json.load(f)

    s2_config["train"]["batch_size"] = batch_size_s2
    s2_config["train"]["epochs"] = epochs_s2
    s2_config["train"]["pretrained_s2G"] = s2G_path
    s2_config["train"]["pretrained_s2D"] = s2D_path
    s2_config["train"]["gpu_numbers"] = "0"
    s2_config["train"]["if_save_latest"] = True
    s2_config["train"]["if_save_every_weights"] = True
    s2_config["train"]["save_every_epoch"] = epochs_s2
    s2_config["data"]["exp_dir"] = exp_dir
    s2_config["s2_ckpt_dir"] = exp_dir
    s2_config["save_weight_dir"] = os.path.join(sovits_dir, "SoVITS_weights_v2")
    s2_config["name"] = exp_name
    s2_config["version"] = version
    s2_config["model"]["version"] = version

    s2_tmp = os.path.join(exp_dir, "tmp_s2.json")
    with open(s2_tmp, "w") as f:
        json.dump(s2_config, f)

    r = subprocess.run(
        [py, "-s", "GPT_SoVITS/s2_train.py", "--config", s2_tmp],
        cwd=sovits_dir, timeout=3600
    )
    if r.returncode != 0:
        print(f"  [x] SoVITS 训练失败")
        return False
    print(f"  [ok] SoVITS 微调完成")

    # Step 5: GPT 微调（根据转录质量决定是否执行）
    do_gpt_train = True
    if skip_gpt:
        do_gpt_train = False
        print(f"\n[Step 5/6] GPT 微调 -- 跳过（--skip-gpt）")
    elif not force_gpt:
        quality = _check_transcription_quality(annotation_path)
        print(f"\n[Step 5/6] 转录质量检测: {quality:.0%}")
        if quality < 0.5:
            do_gpt_train = False
            print(f"  转录质量较低（{quality:.0%} < 50%），可能是方言数据")
            print(f"  自动跳过 GPT 微调，推理时将使用预训练底模")
            print(f"  （如需强制训练，添加 --force-gpt 参数）")
        else:
            print(f"  转录质量良好（{quality:.0%}），执行 GPT 微调")

    if not do_gpt_train:
        print(f"  [ok] GPT 微调已跳过 — 推理时使用预训练底模 + 微调 SoVITS")
    else:
        print(f"  GPT 微调开始 (batch={batch_size_s1}, epochs={epochs_s1})...")
        s1_config_template = os.path.join(sovits_dir, "GPT_SoVITS", "configs", "s1longer.yaml")
        s1_dir = exp_dir
        semantic_path = os.path.join(s1_dir, "6-name2semantic.tsv")
        phoneme_path = os.path.join(s1_dir, "2-name2text.txt")
        s1_tmp = os.path.join(exp_dir, "tmp_s1.yaml")

        import yaml
        if os.path.exists(s1_config_template):
            with open(s1_config_template) as f:
                s1_config = yaml.safe_load(f)
        else:
            s1_config = {}

        s1_config["train_semantic_path"] = semantic_path
        s1_config["train_phoneme_path"] = phoneme_path
        s1_config["output_dir"] = os.path.join(s1_dir, "logs_s1")
        s1_config["pretrained_s1"] = s1_ckpt
        s1_config["batch_size"] = batch_size_s1
        s1_config["epochs"] = epochs_s1
        s1_config["save_every_epoch"] = epochs_s1
        s1_config["if_save_latest"] = True
        s1_config["if_save_every_weights"] = True
        s1_config["gpu_numbers"] = "0"
        s1_config["save_weight_dir"] = os.path.join(sovits_dir, "GPT_weights_v2")
        s1_config["name"] = exp_name
        s1_config["version"] = version

        with open(s1_tmp, "w") as f:
            yaml.dump(s1_config, f)

        r = subprocess.run(
            [py, "-s", "GPT_SoVITS/s1_train.py", "--config_file", s1_tmp],
            cwd=sovits_dir, timeout=3600
        )
        if r.returncode != 0:
            print(f"  [x] GPT 训练失败")
            return False
        print(f"  [ok] GPT 微调完成")

    # Step 6: 复制模型到档案目录
    print(f"\n[Step 6/6] 复制模型文件...")
    model_dir = os.path.join(voice_dir(slug), "gpt_sovits")
    os.makedirs(model_dir, exist_ok=True)

    # 查找生成的模型文件
    sovits_weight_dir = os.path.join(sovits_dir, "SoVITS_weights_v2")
    gpt_weight_dir = os.path.join(sovits_dir, "GPT_weights_v2")

    copied = []
    for d in [sovits_weight_dir, gpt_weight_dir]:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if exp_name in f and f.endswith(".pth") or f.endswith(".ckpt"):
                    src = os.path.join(d, f)
                    dst = os.path.join(model_dir, f)
                    shutil.copy2(src, dst)
                    copied.append(f)

    if copied:
        print(f"  [ok] 模型已保存到 {model_dir}")
        for f in copied:
            size = os.path.getsize(os.path.join(model_dir, f)) / 1024 / 1024
            print(f"    {f} ({size:.1f}MB)")
    else:
        print(f"  [!] 未找到输出的模型文件，请检查训练日志")

    # 保存训练配置
    train_meta = {
        "slug": slug, "version": version,
        "batch_size_s2": batch_size_s2, "epochs_s2": epochs_s2,
        "batch_size_s1": batch_size_s1, "epochs_s1": epochs_s1,
        "model_files": copied,
        "sovits_dir": sovits_dir,
    }
    with open(os.path.join(model_dir, "train_config.json"), "w", encoding="utf-8") as f:
        json.dump(train_meta, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"  训练完成!")
    print(f"  模型目录: {model_dir}")
    print(f"  下一步: python voice_synthesizer.py --slug {slug} --text \"测试文本\"")
    print(f"{'=' * 60}")
    return True


# ── Status ────────────────────────────────────────────────────────────────────

def action_status(slug: str):
    """查看训练数据和模型状态。"""
    vdir = voice_dir(slug)
    tdir = training_dir(slug)
    model_dir = os.path.join(vdir, "gpt_sovits")

    print(f"=== {slug} voice model status ===\n")

    if os.path.isdir(tdir):
        manifest_path = os.path.join(tdir, "manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            print(f"Training data: [ok]")
            print(f"  Files: {manifest['total_files']}")
            print(f"  Duration: {manifest['total_duration_seconds']}s")
        annotation_path = os.path.join(tdir, "annotations.list")
        if os.path.exists(annotation_path):
            with open(annotation_path, encoding="utf-8") as f:
                n = len(f.readlines())
            print(f"  Annotations: [ok] {n}")
        else:
            print(f"  Annotations: [x]")
    else:
        print(f"Training data: [x]")

    print()
    if os.path.isdir(model_dir):
        pth_files = [f for f in os.listdir(model_dir) if f.endswith((".pth", ".ckpt"))]
        if pth_files:
            print(f"Model: [ok]")
            for f in pth_files:
                size = os.path.getsize(os.path.join(model_dir, f)) / 1024 / 1024
                print(f"  {f} ({size:.1f}MB)")
        else:
            print(f"Model: [..] directory exists, no weights yet")
    else:
        print(f"Model: [x]")

    print()
    sovits_dir = get_sovits_dir()
    print(f"GPT-SoVITS: {'[ok] ' + sovits_dir if sovits_dir else '[x]'}")


# ── Full (一键全流程) ────────────────────────────────────────────────────────

def action_full(slug: str, audio_dir: str):
    """一键完成：prepare + train。"""
    print("=" * 60)
    print(f"  Memorial Voice - One-Click Training")
    print(f"  Target: {slug}")
    print("=" * 60)

    ok = action_prepare(slug, audio_dir)
    if not ok:
        return False

    ok = action_train(slug)
    return ok


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Voice model trainer (GPT-SoVITS)")
    parser.add_argument("--action", required=True,
                        choices=["prepare", "train", "full", "status"],
                        help="Action: prepare/train/full/status")
    parser.add_argument("--slug", help="Memorial slug")
    parser.add_argument("--audio-dir", help="Preprocessed WAV directory (for prepare/full)")
    parser.add_argument("--batch-size-s2", type=int, default=16, help="SoVITS batch size")
    parser.add_argument("--epochs-s2", type=int, default=10, help="SoVITS epochs")
    parser.add_argument("--batch-size-s1", type=int, default=8, help="GPT batch size")
    parser.add_argument("--epochs-s1", type=int, default=15, help="GPT epochs")
    parser.add_argument("--skip-gpt", action="store_true",
                        help="Skip GPT fine-tuning (use pretrained, recommended for dialect)")
    parser.add_argument("--force-gpt", action="store_true",
                        help="Force GPT fine-tuning even if transcription quality is low")
    args = parser.parse_args()

    if args.action == "status":
        if not args.slug:
            parser.error("--slug required")
        action_status(args.slug)
    elif args.action == "prepare":
        if not args.slug or not args.audio_dir:
            parser.error("--slug and --audio-dir required")
        action_prepare(args.slug, args.audio_dir)
    elif args.action == "train":
        if not args.slug:
            parser.error("--slug required")
        action_train(args.slug, args.batch_size_s2, args.epochs_s2,
                     args.batch_size_s1, args.epochs_s1,
                     skip_gpt=args.skip_gpt, force_gpt=args.force_gpt)
    elif args.action == "full":
        if not args.slug or not args.audio_dir:
            parser.error("--slug and --audio-dir required")
        action_full(args.slug, args.audio_dir)


if __name__ == "__main__":
    main()
