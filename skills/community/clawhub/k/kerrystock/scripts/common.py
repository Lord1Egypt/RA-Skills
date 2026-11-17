#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kerrystock 公用路径解析：让技能在任意 WorkBuddy 安装 / 任意用户机器上可移植。

解决原脚本写死本机专属路径（如 /Users/<user>/.workbuddy/...、/Volumes/WorkBuddy 5.2.6-arm64/...）
导致：(1) 泄漏用户机器环境；(2) 在他人机器或未来 WorkBuddy 版本上跑不通。

解析优先级：
  1) 环境变量（WESTOCK_DATA_SCRIPT / NEODATA_SCRIPT / WB_FINANCE_QUANT_DIR / NODE_BIN）最高优先；
  2) 自动探测常见 WorkBuddy 安装位置（/Volumes/WorkBuddy*/、/Applications/）；
  3) 找不到则返回 None，由调用方给出清晰报错。
"""
import os
import glob


def _builtin_skill_path(rel: str):
    """定位 builtin 技能内的文件/目录。

    rel 示例：
      'westock-data/scripts/index.js'
      'neodata-financial-search/scripts/query.py'
      'wb-finance-skill/scripts/quant'
    返回首个存在的绝对路径，找不到返回 None。
    """
    home = os.path.expanduser("~")
    bases = [
        "/Volumes/WorkBuddy*/WorkBuddy.app/Contents/Resources/app.asar.unpacked/resources/builtin-skills",
        "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/resources/builtin-skills",
        os.path.join(home, ".workbuddy/skills"),  # 兜底：用户级同名技能
    ]
    for b in bases:
        hits = sorted(glob.glob(os.path.join(b, rel)))
        if hits:
            return hits[0]
    return None


def _managed_node():
    """返回 managed node 可执行文件路径；找不到回退到 PATH 上的 node。"""
    env = os.environ.get("NODE_BIN")
    if env:
        return env
    home = os.path.expanduser("~")
    # managed node：~/.workbuddy/binaries/node/versions/<ver>/bin/node
    hits = sorted(glob.glob(os.path.join(home, ".workbuddy/binaries/node/versions/*/bin/node")))
    if hits:
        return hits[-1]  # 取最高版本
    return "node"
