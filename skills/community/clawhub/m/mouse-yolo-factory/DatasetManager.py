import os
import shutil
import time
import re
from tqdm import tqdm

class DatasetManager:
    def __init__(self, log_callback=None):
        self.log = log_callback if log_callback else print

    def get_latest_dataset(self, root_path):
        """從指定目錄中找出名稱最接近時間戳的最新資料夾"""
        if not os.path.exists(root_path):
            return None
        
        # 找出所有包含 'Dataset_' 開頭的資料夾
        folders = [os.path.join(root_path, d) for d in os.listdir(root_path) 
                   if os.path.isdir(os.path.join(root_path, d)) and d.startswith("Dataset_")]
        
        if not folders:
            return None
        
        # 根據資料夾的新舊排序（依建立時間或名稱）
        return max(folders, key=os.path.getmtime)

    def merge_and_generate(self, current_data_dir, yolo_root_dir, desc=""):
        """
        current_data_dir: 你確認過沒問題的新圖片+標註路徑
        yolo_root_dir: 存放所有版本 Dataset 的根目錄 (例如 D:/YOLO_Data)
        """
        timestamp = time.strftime("%Y%m%d_%H%M")
        new_version_name = f"Dataset_{timestamp}"
        target_dir = os.path.join(yolo_root_dir, new_version_name)
        
        latest_dataset = self.get_latest_dataset(yolo_root_dir)
        self.log(f"偵測到最新版本: {latest_dataset if latest_dataset else '無，將建立初始版本'}")

        # 1. 建立結構
        for split in ['train', 'val']:
            os.makedirs(os.path.join(target_dir, split, "images"), exist_ok=True)
            os.makedirs(os.path.join(target_dir, split, "labels"), exist_ok=True)

        # 2. 融合舊資料 (最新的那個版本)
        if latest_dataset:
            self.log(f"正在從 {os.path.basename(latest_dataset)} 融合舊數據...")
            for split in ['train', 'val']:
                self._copy_yolo_files(latest_dataset, target_dir, split, prefix="old")

        # 3. 融合新資料 (current_data_dir)
        # 這裡模擬將新資料依 8:2 隨機分配進 train/val
        self.log(f"正在將新路徑資料分配進新版本...")
        all_imgs = [f for f in os.listdir(current_data_dir) if f.lower().endswith(('.jpg', '.png'))]
        import random
        random.shuffle(all_imgs)
        
        split_idx = int(len(all_imgs) * 0.8)
        new_splits = {
            'train': all_imgs[:split_idx],
            'val': all_imgs[split_idx:]
        }

        for split, files in new_splits.items():
            for f in files:
                src_img = os.path.join(current_data_dir, f)
                self._safe_copy(src_img, target_dir, split, prefix=f"add_{timestamp}")

        # 4. 生成 log.txt 說明
        with open(os.path.join(target_dir, "log.txt"), "w", encoding="utf-8") as f:
            f.write(f"=== Dataset Merge Log ===\n")
            f.write(f"生成時間: {timestamp}\n")
            f.write(f"融合來源 A (舊): {latest_dataset if latest_dataset else 'None'}\n")
            f.write(f"融合來源 B (新): {current_data_dir}\n")
            f.write(f"備註說明: {desc}\n")

        self.log(f"融合完成！新版本路徑: {target_dir}")
        return target_dir

    def _copy_yolo_files(self, src_root, dst_root, split, prefix):
        src_img_dir = os.path.join(src_root, split, "images")
        if not os.path.exists(src_img_dir): return
        
        for f in os.listdir(src_img_dir):
            if f.lower().endswith(('.jpg', '.png')):
                self._safe_copy(os.path.join(src_img_dir, f), dst_root, split, prefix)

    def _safe_copy(self, src_img_path, dst_root, split, prefix):
        base = os.path.basename(src_img_path)
        name, ext = os.path.splitext(base)
        
        new_name = f"{prefix}_{name}"
        # 複製圖片
        shutil.copy2(src_img_path, os.path.join(dst_root, split, "images", f"{new_name}{ext}"))
        # 複製標註
        src_lbl = os.path.splitext(src_img_path)[0] + ".txt"
        if os.path.exists(src_lbl):
            shutil.copy2(src_lbl, os.path.join(dst_root, split, "labels", f"{new_name}.txt"))