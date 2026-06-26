#!/bin/bash
# pdf-finance-parser 环境配置示例
# 用法：复制为 env.sh（与 SKILL.md 同目录或调用 CWD），脚本自动加载

# ─────────────────────────────────────────────────────────────────────
# v0.3 主路径：LAS 算子 + 后处理（必填）
# ─────────────────────────────────────────────────────────────────────
export LAS_API_KEY="las-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# export LAS_REGION="cn-beijing"                  # 默认 cn-beijing 可省
# export LAS_API_BASE=""                          # 自定义 endpoint 可省

# TOS 凭证（本地 PDF 上传到 LAS 必需）
export TOS_BUCKET="your-bucket-name"              # ← 你的桶名
export TOS_ACCESS_KEY="AKLT..."                   # ← TOS AccessKey
export TOS_SECRET_KEY="..."                       # ← TOS SecretKey
export TOS_REGION="cn-beijing"                    # 若桶在别的 region 单独指定
# export TOS_ENDPOINT=""                          # 默认按 region 推断

# ─────────────────────────────────────────────────────────────────────
# 备选 VLM 路径（v0.2 fallback；遇密集表格 90s timeout 易失败，主路径用 LAS）
# ─────────────────────────────────────────────────────────────────────
# 选项 A: 火山方舟 (Doubao Vision)
# export ARK_API_KEY="ark-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# export VLM_MODEL="doubao-seed-1-6-vision-250815"
# export ARK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"   # 默认

# 选项 B: 阿里 DashScope (Qwen-VL)
# export DASHSCOPE_API_KEY="your-dashscope-key"
# export VLM_MODEL="qwen-vl-max"

# 选项 C: OpenAI 兼容端点
# export OPENAI_API_KEY="sk-..."
# export OPENAI_BASE_URL="https://api.openai.com/v1"

# 选项 D: 本地 Ollama
# export VLM_PROVIDER="ollama"
# export VLM_BASE_URL="http://localhost:11434/v1"
# export VLM_MODEL="qwen2.5-vl:7b"

# ─────────────────────────────────────────────────────────────────────
# 通用覆盖（可选）
# ─────────────────────────────────────────────────────────────────────
# export VLM_TIMEOUT_SECONDS="90"
# export VLM_MAX_RETRIES="3"
# export VLM_PROVIDER="ark"                       # ark / openai / dashscope / ollama