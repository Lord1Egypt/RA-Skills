
"""
Skill Name: LLM-Text-Correct
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: GPU 精修独立模块
所有 MacBERT 精修业务逻辑都在这里，主程序只负责导入和调用
"""

import sys
import gc
from pathlib import Path
import ensure_package
ensure_package.pip("pycorrector", "pycorrector","MacBertCorrector")
ensure_package.pip("huggingface_hub")
ensure_package.pip("torch")
from pycorrector import MacBertCorrector
from huggingface_hub import snapshot_download
import torch

# ==================== 模型映射（支持别名 + 完整 repo） ====================
MODEL_MAPPING = {
    "shibing624-macbert4csc-base-chinese": "shibing624/macbert4csc-base-chinese",
}

def download_model(model_name: str, models_dir: Path) -> str:
    """自动下载模型（失败时控制台美观格式化显示）"""
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
        print(f"✅ 模型已存在: {local_dir}")
        return str(local_dir)

    print(f"🔽 正在从 Hugging Face 下载模型: {model_name} → {repo_id}")
    print(f" 保存路径: {local_dir}（当前models目录）")
    local_dir.mkdir(parents=True, exist_ok=True)

    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_dir),
            allow_patterns=["*"]
        )
        print(f"✅ 下载完成！模型路径: {local_dir}")
        return str(local_dir)
    except Exception as e:
        download_url = f"https://huggingface.co/{repo_id}/tree/main"
        
        # 美观格式化输出
        print("\n" + "="*60)
        print("❌ 模型下载失败")
        print("="*60)
        print(f"错误原因: {str(e)}")
        print("\n💡 手动下载方案（推荐，3步搞定）：")
        print(" 1. 打开下面链接（直接复制到浏览器）：")
        print(f" 👉 {download_url}")
        print(" 2. 点击页面右上角 **Download** 按钮（或逐个文件下载）")
        print(" 需要下载全部文件：config.json、pytorch_model.bin、tokenizer.json 等")
        print(f" 3. 把所有文件放到以下目录：")
        print(f" 📁 {local_dir}")
        print(" 4. 重新运行命令即可（自动识别已存在模型）")
        print("\n📋 你的专属模型下载地址（已为你生成）：")
        print(f" {download_url}")
        print("="*60 + "\n")
        
        sys.exit(1)


class MacBertGPURefiner:
    """独立 GPU 精修类（全部业务逻辑封装在这里）"""
    def __init__(self, custom_confusion_path_or_dict, model_name="shibing624-macbert4csc-base-chinese"):
        self.model = None
        self.custom_confusion = custom_confusion_path_or_dict
        self.model_name = model_name  # 支持传入别名或完整 repo
        # 项目根目录下的 models/
        self.models_dir = Path(__file__).parent.parent / "models"
        self.model_path = None  # 稍后通过 download_model 获取

    def init(self):
        """本地加载或下载 MacBERT 模型"""
        if self.model is None:
            # 先确保模型存在（下载或使用本地）
            self.model_path = download_model(self.model_name, self.models_dir)
            
            model_dir = Path(self.model_path)
            if not model_dir.exists() or not (model_dir / "pytorch_model.bin").exists():
                print(f"❌ 模型目录无效或缺少关键文件：{self.model_path}", file=sys.stderr)
                return False

            print("🚀 正在从本地加载 MacBERT GPU 精修模型...", file=sys.stderr)
            print(f"   路径: {self.model_path}", file=sys.stderr)

            self.model = MacBertCorrector(
                model_name_or_path=self.model_path,
            )
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"✅ MacBERT 本地模型加载完成！设备: {device}", file=sys.stderr)
            return True
        return True

    def correct(self, text: str) -> str:
        """执行精修（KenLM 结果 → MacBERT 语义精修）"""
        if not self.init():
            return text
        try:
            results = self.model.correct_batch([text])
            return results[0]['target'] if results else text
        except Exception as e:
            print(f"⚠️ MacBERT 精修异常，回退原始结果: {e}", file=sys.stderr)
            return text

    def cleanup(self):
        """释放 GPU 显存"""
        if self.model is not None:
            del self.model
            self.model = None
            gc.collect()
            print("✅ GPU 精修模型显存已释放", file=sys.stderr)


# 全局单例（主程序会直接使用）
gpu_refiner = None