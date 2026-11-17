#!/usr/bin/env bash
# ============================================================
# 话袋笔记 Skill · OAuth 设备授权
#
# 当前 OAuth 前端确认页尚未开放，暂不作为用户配置方式。
# 请使用话袋开放平台创建 API Key，并配置 HUADAI_API_KEY。
# ============================================================
set -euo pipefail

echo "OAuth 授权方式暂未开放。"
echo ""
echo "请改用 API Key 配置方式："
echo "1. 打开 https://ihuadai.cn/desktop/openai"
echo "2. 创建 API Key"
echo "3. 设置环境变量: export HUADAI_API_KEY=<你的Key>"
exit 1
