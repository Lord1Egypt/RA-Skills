#!/usr/bin/env python3
"""
OpenClaw Model Switcher - 命令行快速切换工具
用法:
    python switch_model.py --status              查看当前模型
    python switch_model.py --list               列出所有已保存模型
    python switch_model.py --provider xxx --model yyy   切换到指定模型
    python switch_model.py --restart            重启 Gateway
"""
import argparse
import json
import os
import sys
import time
import subprocess

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_ROOT = os.path.join(SKILL_ROOT, "backend")
sys.path.insert(0, BACKEND_ROOT)

def get_config_path():
    return os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")

def load_config():
    path = get_config_path()
    if not os.path.exists(path):
        print(f"配置文件不存在: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    path = get_config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"配置已保存到: {path}")

def get_current_model():
    cfg = load_config()
    return (
        cfg.get("agents", {})
        .get("defaults", {})
        .get("model", {})
        .get("primary", "")
    )

def list_models():
    cfg = load_config()
    providers = cfg.get("models", {}).get("providers", {})
    current = get_current_model()

    print("\n=== 已保存的模型 ===")
    if not providers:
        print("  (无)")
        return

    for pid, p in providers.items():
        models = p.get("models", [])
        for m in models:
            mid = m.get("id", "?")
            full = f"{pid}/{mid}"
            marker = " ← 当前" if full == current else ""
            print(f"  [{pid}] {mid}{marker}")
    print()

def show_status():
    current = get_current_model()
    if current:
        print(f"\n当前模型: {current}\n")
    else:
        print("\n当前模型: 未设置\n")

def switch_model(provider_id: str, model_id: str):
    cfg = load_config()

    # 设置当前模型
    agents = cfg.setdefault("agents", {}).setdefault("defaults", {})
    agents.setdefault("model", {})["primary"] = f"{provider_id}/{model_id}"
    agents.setdefault("models", {})[f"{provider_id}/{model_id}"] = {}

    save_config(cfg)
    print(f"✓ 已切换到: {provider_id}/{model_id}")
    print("  请运行 --restart 重启 Gateway 使更改生效")

def restart_gateway():
    print("正在重启 OpenClaw Gateway...")
    try:
        # 尝试用 taskkill
        subprocess.run("taskkill /F /IM openclaw.exe", shell=True, capture_output=True)
        time.sleep(1)
    except Exception:
        pass

    # 启动 gateway
    gateway_cmd = os.path.join(os.path.expanduser("~"), ".openclaw", "gateway.cmd")
    if os.path.exists(gateway_cmd):
        subprocess.Popen(f'"{gateway_cmd}"', shell=True, creationflags=0x08000000)
        print("✓ Gateway 重启完成")
    else:
        print(f"! Gateway 启动脚本不存在: {gateway_cmd}")
        print("  请手动重启 OpenClaw")

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 模型切换工具")
    parser.add_argument("--status", action="store_true", help="查看当前模型")
    parser.add_argument("--list", action="store_true", help="列出所有已保存模型")
    parser.add_argument("--provider", help="提供商 ID")
    parser.add_argument("--model", help="模型 ID")
    parser.add_argument("--restart", action="store_true", help="重启 Gateway")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.list:
        list_models()
    elif args.restart:
        restart_gateway()
    elif args.provider and args.model:
        switch_model(args.provider, args.model)
    else:
        show_status()
        print(__doc__)

if __name__ == "__main__":
    main()
