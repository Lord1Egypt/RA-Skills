#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署脚本：将内置的「石油工程油藏论文写作专家团」安装到用户的 WorkBuddy 专家目录，
并向 marketplace.json 注册，使其在专家中心可见。

幂等：已存在则跳过复制，仅确保注册条目存在。
跨平台：自动解析 WORKBUDDY_CONFIG_DIR 或 ~/.workbuddy。
"""

import json
import os
import shutil
import sys


def resolve_config_dir():
    env = os.environ.get("WORKBUDDY_CONFIG_DIR")
    if env:
        return env
    return os.path.join(os.path.expanduser("~"), ".workbuddy")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(here)
    src = os.path.join(skill_root, "assets", "petroleum-reservoir-paper-team")
    if not os.path.isdir(src):
        print(f"[ERROR] 未找到专家团资源目录: {src}")
        sys.exit(1)

    config_dir = resolve_config_dir()
    plugins_dir = os.path.join(config_dir, "plugins", "marketplaces", "my-experts", "plugins")
    marketplace_json = os.path.join(config_dir, "plugins", "marketplaces", "my-experts", ".codebuddy-plugin", "marketplace.json")
    os.makedirs(plugins_dir, exist_ok=True)

    expert_name = "petroleum-reservoir-paper-team"
    dst = os.path.join(plugins_dir, expert_name)

    # 1) 复制专家团目录
    if os.path.exists(dst):
        print(f"[INFO] 专家团已存在于 {dst}，跳过复制。")
    else:
        shutil.copytree(src, dst)
        print(f"[OK] 已复制专家团到 {dst}")

    # 2) 注册到 marketplace.json
    if not os.path.exists(marketplace_json):
        print(f"[ERROR] 未找到 marketplace.json: {marketplace_json}")
        print("请确认 WorkBuddy 专家目录结构正确，或手动将专家团目录放入 plugins/ 后注册。")
        sys.exit(1)

    with open(marketplace_json, "r", encoding="utf-8") as f:
        market = json.load(f)

    plugins = market.get("plugins", [])
    already = any(p.get("name") == expert_name for p in plugins)
    if not already:
        plugins.append({
            "name": expert_name,
            "source": f"./plugins/{expert_name}",
            "description": "An eight-member expert team for petroleum reservoir engineering academic paper writing, covering topic selection, research, writing, review and formatting."
        })
        market["plugins"] = plugins
        with open(marketplace_json, "w", encoding="utf-8") as f:
            json.dump(market, f, ensure_ascii=False, indent=2)
        print("[OK] 已注册专家团到 marketplace.json")
    else:
        print("[INFO] marketplace.json 中已存在该专家团注册条目，跳过。")

    print("\n✅ 部署完成！请在 WorkBuddy 左侧「专家」→「我的专家」中查看「石油工程油藏论文写作专家团」。")


if __name__ == "__main__":
    main()
