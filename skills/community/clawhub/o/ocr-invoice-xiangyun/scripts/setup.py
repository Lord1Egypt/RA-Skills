#!/usr/bin/env python3
"""
凭据初始化脚本
首次使用时运行：python scripts/setup.py
也可用于更新已有凭据
"""
import json
import sys
from pathlib import Path


def main():
    config_path = Path(__file__).parent.parent / "config.json"

    existing_key    = ""
    existing_secret = ""
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            existing_key    = cfg.get("key", "")
            existing_secret = cfg.get("secret", "")
        except Exception:
            pass

    print("=" * 60)
    print("  翔云 OCR 凭据配置")
    print("  获取地址：https://netocr.com → 登录 → 个人中心")
    print("=" * 60)

    if existing_key and existing_secret:
        masked = existing_key[:4] + "****" + existing_key[-4:]
        print(f"\n  当前已配置：key={masked}")
        choice = input("  是否更新？(y/N): ").strip().lower()
        if choice != "y":
            print("  未作修改，退出。")
            return

    key    = input("\n  请输入 ocrKey    : ").strip()
    secret = input("  请输入 ocrSecret : ").strip()

    if not key or not secret:
        print("[ERROR] key 和 secret 不能为空")
        sys.exit(1)

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"key": key, "secret": secret}, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 凭据已保存至：{config_path}")
    print("     现在可以运行：python scripts/invoice.py --image <发票路径> --verify --export")


if __name__ == "__main__":
    main()
