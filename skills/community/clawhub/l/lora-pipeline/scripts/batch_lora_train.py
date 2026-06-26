#!/usr/bin/env python3
"""
Kohya Batch LoRA Training Script for RunPod
適用於 SD 1.5，A5000 24GB 優化

================================================================================

--------------------------------------------------------------------------------
執行方式：
--------------------------------------------------------------------------------
1. RunPod 選擇 template: Kohya_ss GUI (ashleykza/kohya:cu124-py311-25.2.1)
2. 上傳此 script 到 /workspace/batch_lora_train.py
3. 將 datasets 放到 /workspace/datasets/（結構如下）
4. 執行：
   $ python /workspace/batch_lora_train.py

--------------------------------------------------------------------------------
資料夾結構：
--------------------------------------------------------------------------------

/workspace/datasets/                    # DATASETS_ROOT（父目錄）
├── 50_person1 man/                     # 格式: {重複次數}_{名稱} {class}
│   ├── image001.png
│   ├── image001.txt                    # caption 檔（與圖片同名）
│   ├── image002.jpg
│   ├── image002.txt
│   └── ...
├── 50_person2 woman/
│   ├── photo01.png
│   ├── photo01.txt
│   └── ...
├── 100_style1/                         # 重複次數可不同
│   └── ...
└── 50_another_concept man/
    └── ...

--------------------------------------------------------------------------------
命名規則：
--------------------------------------------------------------------------------
- 資料夾名稱格式: {數字}_{名稱}
  - 數字 = 每 epoch 重複次數（通常 50-100）
  - 名稱 = 會用於輸出檔名，例如 "person1 man" → "person1_man_lora.safetensors"

- 圖片格式: .png, .jpg, .jpeg, .webp 皆可
- Caption 檔: 與圖片同名，副檔名 .txt

--------------------------------------------------------------------------------
輸出：
--------------------------------------------------------------------------------
/workspace/kohya_ss/outputs/
├── person1_lora.safetensors            # "person1 man" → "person1"
├── person2_lora.safetensors            # "person2 woman" → "person2"
├── style1_lora.safetensors
└── another_concept_lora.safetensors

================================================================================
"""

import subprocess
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# ==================== 設定區 ====================

DATASETS_ROOT = "/workspace/datasets"
KOHYA_ROOT = "/workspace/kohya_ss"
OUTPUT_DIR = "/workspace/kohya_ss/outputs"
ACCELERATE_PATH = "/venv/bin/accelerate"
TEMP_TRAIN_DIR = "/tmp/kohya_train_temp"

# ==================== 訓練參數 ====================

TRAIN_CONFIG = {
    # 基本
    "pretrained_model": "runwayml/stable-diffusion-v1-5",
    "resolution": "512,512",

    # 訓練強度
    "train_batch_size": 4,          # A5000 OOM fix (lowered from 8)
    "max_train_steps": 600,
    "epoch": 1,

    # Learning Rate
    "learning_rate": 0.0002,        # batch_size 加倍，lr 也加倍
    "unet_lr": 0.0002,
    "text_encoder_lr": 0.0001,      # TE 通常用較低 lr
    "lr_scheduler": "cosine",
    "lr_warmup_steps": 100,

    # LoRA
    "network_dim": 64,
    "network_alpha": 32,

    # 優化
    "optimizer_type": "AdamW8bit",
    "mixed_precision": "fp16",
    "xformers": True,
    "cache_latents": True,
    "highvram": True,

    # 其他
    "clip_skip": 1,
    "noise_offset": 0.05,
    "shuffle_caption": True,
    "caption_extension": ".txt",
}

# ==================== TOML Template ====================

TOML_TEMPLATE = '''bucket_no_upscale = true
bucket_reso_steps = 64
cache_latents = {cache_latents}
caption_dropout_rate = 0.1
caption_extension = "{caption_extension}"
clip_skip = {clip_skip}
dynamo_backend = "no"
enable_bucket = true
epoch = {epoch}
gradient_accumulation_steps = 1
highvram = {highvram}
huber_c = 0.1
huber_scale = 1
huber_schedule = "snr"
learning_rate = {learning_rate}
loss_type = "l2"
lr_scheduler = "{lr_scheduler}"
lr_scheduler_args = []
lr_scheduler_num_cycles = 1
lr_scheduler_power = 1
lr_warmup_steps = {lr_warmup_steps}
max_bucket_reso = 2048
max_data_loader_n_workers = 6
max_grad_norm = 1
max_timestep = 1000
max_token_length = 150
max_train_steps = {max_train_steps}
min_bucket_reso = 256
mixed_precision = "{mixed_precision}"
network_alpha = {network_alpha}
network_args = []
network_dim = {network_dim}
network_module = "networks.lora"
noise_offset = {noise_offset}
noise_offset_type = "Original"
optimizer_args = []
optimizer_type = "{optimizer_type}"
output_dir = "{output_dir}"
output_name = "{output_name}"
persistent_data_loader_workers = 1
pretrained_model_name_or_path = "{pretrained_model}"
prior_loss_weight = 1
resolution = "{resolution}"
sample_sampler = "euler_a"
save_model_as = "safetensors"
save_precision = "fp16"
shuffle_caption = {shuffle_caption}
text_encoder_lr = {text_encoder_lr}
train_batch_size = {train_batch_size}
train_data_dir = "{train_data_dir}"
unet_lr = {unet_lr}
xformers = {xformers}
'''

# ==================== Functions ====================

def get_dataset_folders(root_path: str) -> list[tuple[str, str, str]]:
    """掃描符合 `數字_名稱` 格式的資料夾
    回傳: [(完整路徑, 資料夾名稱, 名稱部分), ...]
    """
    folders = []
    root = Path(root_path)

    if not root.exists():
        print(f"❌ 路徑不存在: {root_path}")
        return folders

    pattern = re.compile(r"^\d+_(.+)$")

    for item in sorted(root.iterdir()):
        if item.is_dir():
            match = pattern.match(item.name)
            if match:
                name_part = match.group(1)
                folders.append((str(item), item.name, name_part))

    return folders


def sanitize_output_name(name: str) -> str:
    """將名稱轉換為安全的檔名格式，移除結尾的 class word"""
    # 移除結尾的 class word（man, woman, person, style 等）
    name = re.sub(r"\s+(man|woman|person|style|girl|boy)$", "", name, flags=re.IGNORECASE)
    safe_name = re.sub(r"[^\w\-]", "_", name)
    safe_name = re.sub(r"_+", "_", safe_name).strip("_")
    return f"{safe_name}_lora"


def setup_temp_train_dir(dataset_path: str, folder_name: str) -> str:
    """建立臨時訓練目錄，用 symlink 指向實際 dataset"""
    if os.path.exists(TEMP_TRAIN_DIR):
        shutil.rmtree(TEMP_TRAIN_DIR)
    os.makedirs(TEMP_TRAIN_DIR)

    link_path = os.path.join(TEMP_TRAIN_DIR, folder_name)
    os.symlink(dataset_path, link_path)

    return TEMP_TRAIN_DIR


def create_toml_config(train_data_dir: str, output_name: str) -> str:
    """產生 toml config"""
    cfg = TRAIN_CONFIG
    return TOML_TEMPLATE.format(
        # 路徑
        output_dir=OUTPUT_DIR,
        output_name=output_name,
        train_data_dir=train_data_dir,
        pretrained_model=cfg["pretrained_model"],
        resolution=cfg["resolution"],
        # 訓練
        train_batch_size=cfg["train_batch_size"],
        max_train_steps=cfg["max_train_steps"],
        epoch=cfg["epoch"],
        # LR
        learning_rate=cfg["learning_rate"],
        unet_lr=cfg["unet_lr"],
        text_encoder_lr=cfg["text_encoder_lr"],
        lr_scheduler=cfg["lr_scheduler"],
        lr_warmup_steps=cfg["lr_warmup_steps"],
        # LoRA
        network_dim=cfg["network_dim"],
        network_alpha=cfg["network_alpha"],
        # 優化
        optimizer_type=cfg["optimizer_type"],
        mixed_precision=cfg["mixed_precision"],
        xformers=str(cfg["xformers"]).lower(),
        cache_latents=str(cfg["cache_latents"]).lower(),
        highvram=str(cfg["highvram"]).lower(),
        # 其他
        clip_skip=cfg["clip_skip"],
        noise_offset=cfg["noise_offset"],
        shuffle_caption=str(cfg["shuffle_caption"]).lower(),
        caption_extension=cfg["caption_extension"],
    )


def run_training(config_path: str) -> bool:
    """執行 Kohya 訓練"""
    script_path = os.path.join(KOHYA_ROOT, "sd-scripts", "train_network.py")

    cmd = [
        ACCELERATE_PATH, "launch",
        "--num_cpu_threads_per_process", "6",
        script_path,
        "--config_file", config_path
    ]

    print(f"🚀 {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, cwd=KOHYA_ROOT)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 執行失敗: {e}")
        return False


def main():
    print("=" * 60)
    print("Kohya Batch LoRA Training")
    print("=" * 60)
    print(f"📊 batch_size={TRAIN_CONFIG['train_batch_size']}, "
          f"steps={TRAIN_CONFIG['max_train_steps']}, "
          f"lr={TRAIN_CONFIG['learning_rate']}")
    print("=" * 60)

    # 掃描 datasets
    datasets = get_dataset_folders(DATASETS_ROOT)

    if not datasets:
        print(f"❌ 在 {DATASETS_ROOT} 找不到符合格式的資料夾")
        print("   預期格式: 50_name、100_another_name 等")
        return

    print(f"\n📁 找到 {len(datasets)} 個 dataset:")
    for path, folder_name, name in datasets:
        print(f"   - {name}")

    # 確認
    print("\n" + "=" * 60)
    response = input("是否開始訓練? (y/N): ").strip().lower()
    if response != "y":
        print("已取消")
        return

    # 準備目錄
    temp_config_dir = Path("/tmp/kohya_batch_configs")
    temp_config_dir.mkdir(exist_ok=True)
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # 訓練迴圈
    results = []

    for i, (dataset_path, folder_name, name) in enumerate(datasets, 1):
        print("\n" + "=" * 60)
        print(f"[{i}/{len(datasets)}] {name}")
        print("=" * 60)

        output_name = sanitize_output_name(name)
        train_data_dir = setup_temp_train_dir(dataset_path, folder_name)

        config_path = temp_config_dir / f"config_{output_name}.toml"
        toml_content = create_toml_config(train_data_dir, output_name)

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(toml_content)

        print(f"📂 {dataset_path}")
        print(f"💾 {OUTPUT_DIR}/{output_name}.safetensors")

        start_time = datetime.now()
        success = run_training(str(config_path))
        duration = datetime.now() - start_time

        results.append({"name": name, "success": success, "duration": str(duration)})

        status = "✅" if success else "❌"
        print(f"{status} {name} ({duration})")

    # 清理
    if os.path.exists(TEMP_TRAIN_DIR):
        shutil.rmtree(TEMP_TRAIN_DIR)

    # 總結
    print("\n" + "=" * 60)
    print("訓練總結")
    print("=" * 60)

    success_count = sum(1 for r in results if r["success"])
    print(f"成功: {success_count}/{len(results)}")

    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"  {status} {r['name']} ({r['duration']})")


if __name__ == "__main__":
    main()
