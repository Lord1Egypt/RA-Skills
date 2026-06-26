# ClawHub Metadata

version: 1.5.1
slug: mbti-guru
name: MBTI Guru
description: |
  专业MBTI人格测试工具，支持中英双语PDF报告。
  提供4种测试版本(70/93/144/200题)，自动进度保存，
  历史记录，认知功能分析，职业建议和人际关系匹配。
  基于OpenClaw架构，支持Telegram、Discord、飞书、微信等所有渠道。
  
summary: MBTI personality test with bilingual PDF reports and multi-channel support
owner: effeceee

tags:
- mbti
- personality
- test
- chinese
- bilingual
- pdf
- openclaw

requirements:
  python: ">=3.8"
  packages:
    matplotlib: ">=3.5.0"
    reportlab: ">=4.0.0"
    numpy: ">=1.20.0"

features:
  - id: versions
    title: 四个测试版本
    description: 70/93/144/200题，适应不同场景
  - id: bilingual_pdf
    title: 中英双语PDF报告
    description: 专业排版，含维度分析、优势劣势、职业建议
  - id: progress_save
    title: 进度自动保存
    description: 每题保存，退出后可继续
  - id: history
    title: 测试历史记录
    description: 保存最近20条测试记录
  - id: cognitive
    title: 认知功能分析
    description: 16种人格的认知功能深度解析
  - id: relationships
    title: 人际关系匹配
    description: 职场建议和情感匹配建议
  - id: channels
    title: 全渠道支持
    description: Telegram、Discord、飞书、微信等OpenClaw支持的渠道

commands:
  - /start
    description: 开始新测试
  - /resume
    description: 继续未完成的测试
  - /history
    description: 查看测试历史
  - /status
    description: 查看当前状态
  - /cancel
    description: 取消当前测试

data_storage:
  sessions:
    path: data/sessions/
    format: json
    description: 测试进度（自动保存）
  history:
    path: data/history/
    format: json
    description: 历史记录（测试完成后保存）
  privacy: |
    所有数据存储在本地服务器，不上传外部。
    用户可删除data/目录清除所有数据。

channels:
  telegram:
    required: false
    config: openclaw_telegram_botToken
    description: 通过OpenClaw配置Telegram Bot Token
  discord:
    required: false
    description: OpenClaw自动支持
  feishu:
    required: false
    description: OpenClaw自动支持
  wechat:
    required: false
    description: OpenClaw自动支持
