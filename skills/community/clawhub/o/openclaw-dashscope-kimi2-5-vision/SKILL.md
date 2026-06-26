---
name: openclaw-dashscope-kimi2-5-vision
description: 使用 Kimi K2.5 识别图片，专为阿里百炼 GLM 用户设计。自动从 OpenClaw 配置读取 API Key。当模型返回"no media-understanding provider"或用户要求图片分析时触发。
author: Mac大护法
created: 2026-03-29
---

# Kimi K2.5 图片识别

为使用阿里百炼 GLM 模型的用户提供图片识别能力。自动检测并复用已有 API Key。

## 自动检测流程

脚本会自动按以下顺序查找 API Key：

1. 环境变量 `DASHSCOPE_API_KEY`
2. OpenClaw 配置 `env.DASHSCOPE_API_KEY`
3. OpenClaw 配置 `models.providers.qwencode.apiKey`
4. OpenClaw 配置 `models.providers.dashscope.apiKey`

找到后会自动设置环境变量并缓存，下次直接使用。

## 使用方法

```bash
python3 scripts/recognize.py <图片路径> [--prompt "提示词"]
```

**示例：**
```bash
# 默认详细描述
python3 scripts/recognize.py /path/to/image.jpg

# 自定义提示
python3 scripts/recognize.py /path/to/screenshot.png --prompt "提取所有文字"
```

## 首次使用

首次运行时，脚本会提示你将 API Key 写入 `~/.openclaw/.env` 以持久化：

```bash
echo 'DASHSCOPE_API_KEY=sk-sp-你的key' >> ~/.openclaw/.env
```

这样重启后也能直接使用。

## 找不到 API Key？

如果所有位置都没找到，脚本会告诉你去阿里百炼控制台生成：

1. 打开 https://bailian.console.aliyun.com/
2. 登录阿里云账号
3. 进入「API-KEY 管理」创建 Key
4. 设置到环境变量或 OpenClaw 配置中