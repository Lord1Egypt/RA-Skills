"""
配置文件
存储API密钥和其他配置
"""

import os
from pathlib import Path


class Config:
    """应用配置"""
    
    # 百度OCR配置
    # 请从 https://cloud.baidu.com/product/ocr 获取免费API Key
    BAIDU_API_KEY = os.getenv("BAIDU_API_KEY", "")
    BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY", "")
    
    # 输入输出目录
    INPUT_DIR = "fp"
    OUTPUT_DIR = "output"
    
    # OCR引擎选择: "baidu" 或 "local"
    OCR_ENGINE = "baidu"
    
    @classmethod
    def load_from_file(cls, config_file: str = None):
        """从配置文件加载"""
        if config_file is None:
            # 尝试多个位置
            possible_paths = [
                Path("config.txt"),
                Path(__file__).parent.parent / "config.txt",
                Path.cwd() / "config.txt",
            ]
            for path in possible_paths:
                if path.exists():
                    config_path = path
                    break
            else:
                config_path = Path("config.txt")
        else:
            config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == "BAIDU_API_KEY":
                            cls.BAIDU_API_KEY = value
                        elif key == "BAIDU_SECRET_KEY":
                            cls.BAIDU_SECRET_KEY = value
                        elif key == "OCR_ENGINE":
                            cls.OCR_ENGINE = value
    
    @classmethod
    def save_to_file(cls, config_file: str = "config.txt"):
        """保存到配置文件"""
        config_path = Path(config_file)
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write("# 发票识别工具配置文件\n")
            f.write("# 请从 https://cloud.baidu.com/product/ocr 获取免费API Key\n\n")
            f.write(f"BAIDU_API_KEY={cls.BAIDU_API_KEY}\n")
            f.write(f"BAIDU_SECRET_KEY={cls.BAIDU_SECRET_KEY}\n")
            f.write(f"OCR_ENGINE={cls.OCR_ENGINE}\n")


def setup_config():
    """交互式配置向导"""
    print("\n" + "=" * 60)
    print("发票识别工具 - 配置向导")
    print("=" * 60)
    
    print("\n本工具支持两种OCR引擎：")
    print("1. 百度OCR API（推荐）- 识别准确率高，有免费额度")
    print("2. 本地OCR - 完全离线，但准确率较低")
    
    print("\n推荐使用百度OCR API：")
    print("  1. 访问 https://cloud.baidu.com/product/ocr")
    print("  2. 注册并登录百度智能云账号")
    print("  3. 创建应用，获取 API Key 和 Secret Key")
    print("  4. 免费额度：50000次/天（个人用户足够使用）")
    
    choice = input("\n是否现在配置百度OCR? (y/n): ").strip().lower()
    
    if choice == 'y':
        api_key = input("请输入百度API Key: ").strip()
        secret_key = input("请输入百度Secret Key: ").strip()
        
        Config.BAIDU_API_KEY = api_key
        Config.BAIDU_SECRET_KEY = secret_key
        Config.OCR_ENGINE = "baidu"
        
        # 保存配置
        Config.save_to_file()
        print(f"\n[OK] 配置已保存到: config.txt")
        return True
    else:
        print("\n将使用本地OCR引擎（识别准确率较低）")
        Config.OCR_ENGINE = "local"
        Config.save_to_file()
        return False
