---
name: aipyapp
description: |
  AIPyApp (AI Python Application) 是一个 AI 驱动的 Python 自动化工具，能够根据用户需求自动创建工具并执行任务。
  当用户说"使用aipy"、"使用aipyapp"、"aipy run"、"安装aipyapp"、"抓取网页"、"执行python脚本"、
  "自动化任务"或类似表达时激活此技能。该技能支持：安装 aipyapp、配置 LLM 提供商、
  执行自然语言指令完成网页抓取、文件处理、内容转换等任务。
---

# Aipyapp - AI 自动化任务执行工具

## Overview

AIPyApp 是一个基于 AI 的 Python 自动化框架，能根据用户自然语言描述自动：
1. 分析需求并规划解决方案
2. 编写并执行 Python 脚本
3. 安装所需依赖
4. 返回执行结果

## 核心能力

- **智能任务分解**: 将自然语言任务转换为可执行步骤
- **动态代码生成**: 根据需求自动编写 Python 脚本
- **依赖自动管理**: 按需安装 Python 包
- **多模式运行**: run / agent / python / gui / ipython

## 安装 (当用户要求安装时)

```bash
# 检查并安装 python3-pip
apt update && apt install -y python3-full python3-pip

# 安装 aipyapp
python3 -m pip install aipyapp --break-system-packages
```

## 配置 LLM

在 `~/.aipyapp/aipyapp.toml` 添加配置：

```toml
[llm.openai]
type = "openai"
api_key = "your-key"
base_url = "https://api.openai.com/v1"
model = "gpt-4"
enable = true
default = true
```

支持: OpenAI, Anthropic, TrustToken, 自定义 OpenAI 兼容端点

## 执行任务

```bash
# 方式1: 单次任务 (最常用)
aipy run "抓取 https://example.com 保存为 markdown"

# 方式2: HTTP API 服务器 (n8n 集成)
aipy agent

# 方式3: Python 交互模式
aipy python
```

## 工作流程

1. **接收指令**: 用户描述任务
2. **AI 规划**: 分析需求，选择工具，生成代码
3. **执行**: 运行脚本，处理错误
4. **返回结果**: 输出执行结果

## 常用任务示例

### 网页抓取
```bash
aipy run "抓取 https://dev.to/article 保存为 markdown"
```

###图片处理
```bash
aipy run "将图片裁剪为 900x500 公众号封面尺寸"
```

###文件转换
```bash
aipy run "将 HTML 文件转换为 Markdown"
```

## scripts/

- `install.sh` - 一键安装脚本

## references/

- `config.example.toml` - 配置文件模板
