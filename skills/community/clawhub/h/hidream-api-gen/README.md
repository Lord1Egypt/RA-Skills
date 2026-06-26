# HiDream API Gen Skills

A comprehensive collection of AI generation skills for the OpenClaw platform (vivago.ai), enabling seamless integration of advanced video and image generation models into your applications or AI agents.

This repository provides Python scripts and modules that handle parameter validation, payload construction, and API communication for various AIGC models.

[中文介绍](#中文介绍)

## Security & Data Privacy

This tool implements an API client for HiDream/OpenClaw. To ensure transparency and security:

- **Credential Storage**: API tokens are stored locally in `~/.config/openclaw/hidream_config.json` with restrictive permissions (`0600`).
- **File Access**: Scripts may read local image/video files provided via command-line arguments or function calls for the purpose of base64 encoding and transmission to the API.
- **Environment Variables**: Sensitive information can be passed via environment variables (`HIDREAM_AUTHORIZATION`) to avoid persistent storage.
- **Data Exfiltration**: No data is transmitted to any destination other than the official HiDream/OpenClaw endpoints.

## Features

- **Multi-Model Support**: Ready-to-use scripts for popular models:
  - **Video**: Kling (Q2.5T/Q2.6), Sora-2-Pro, Seedance (1.0/1.5), Minimax Hailuo 02
  - **Image**: Seedream (M1/M2), Nano Banana
- **Dual Interface**:
  - **Python API**: Clean, type-hinted functions for direct code integration.
  - **CLI Tools**: robust command-line interface for manual testing and scripting.
- **AI-Ready**: Optimized for AI agents to understand and invoke, with built-in error handling guidance.
- **Unified Auth**: Simple token-based authentication via environment variables.

## Quick Start

### Installation

Clone the repository and install dependencies (requests):

```bash
pip install requests
```

### Configuration

You can configure your API token in two ways:

**Method 1: Interactive (Recommended)**

Run the configuration script and follow the prompts:

```bash
python3 scripts/configure.py
```
This will save your token to `~/.config/openclaw/hidream_config.json`.

**Method 2: Environment Variable**

Get your API token from [vivago.ai/platform/token](https://vivago.ai/platform/token) and set it:

```bash
export HIDREAM_AUTHORIZATION="your-sk-token"
```

### Usage (Python)

```python
from scripts.seedream import run as generate_image

# Generate a cyberpunk cat image
result = generate_image(
    version="M2",
    prompt="A cyberpunk cat on the moon",
    resolution="2048*2048"
)
print(result)
```

### Usage (CLI)

```bash
python3 scripts/kling.py --version "Q2.5T-std" --prompt "A flying car"
```

---

<a id="中文介绍"></a>

# HiDream API Gen Skills (中文介绍)

这是一个针对 OpenClaw 平台 (vivago.ai) 的 AI 生成技能集合，旨在帮助开发者轻松集成先进的视频和图像生成模型。

本项目提供了封装好的 Python 脚本和模块，处理了参数校验、Payload 构建以及与 API 的通信细节。

## 安全与数据隐私

本工具是 HiDream/OpenClaw 的 API 客户端实现。为确保透明度与安全性：

- **凭据存储**：API Token 本地存储于 `~/.config/openclaw/hidream_config.json`，并设置了严格的权限（`0600`）。
- **文件访问**：脚本可能会读取通过命令行参数或函数调用提供的本地图像/视频文件，其目的是进行 base64 编码并传输至 API。
- **环境变量**：敏感信息可以通过环境变量（`HIDREAM_AUTHORIZATION`）传递，以避免持久化存储。
- **数据泄露防护**：除官方 HiDream/OpenClaw 接口外，不会将任何数据传输至其他目的地。

## 功能特性

- **多模型支持**：开箱即用的主流模型支持：
  - **视频模型**: Kling (快手可灵 Q2.5T/Q2.6), Sora-2-Pro, Seedance (1.0/1.5), Minimax Hailuo 02
  - **图像模型**: Seedream (M1/M2), Nano Banana
- **双重接口**：
  - **Python API**: 清晰的、带类型提示的函数接口，适合代码直接调用。
  - **命令行工具**: 健壮的 CLI 接口，适合手动测试或脚本自动化。
- **AI 友好**: 专为 AI Agent 设计，包含错误处理指引，Agent 可轻松理解并调用。
- **统一鉴权**: 通过环境变量即可简单配置 Token。

## 快速开始

### 安装

克隆仓库并安装依赖 (`requests`)：

```bash
pip install requests
```

### 配置

你可以通过以下两种方式配置 API Token：

**方法 1: 交互式配置 (推荐)**

运行配置脚本并按照提示操作：

```bash
python3 scripts/configure.py
```
这会将你的 Token 保存到 `~/.config/openclaw/hidream_config.json`。

**方法 2: 环境变量**

前往 [vivago.ai/platform/token](https://vivago.ai/platform/token) 获取 API Token 并设置环境变量：

```bash
export HIDREAM_AUTHORIZATION="your-sk-token"
```

### 使用示例 (Python)

```python
from scripts.seedream import run as generate_image

# 生成一张赛博朋克猫的图片
result = generate_image(
    version="M2",
    prompt="A cyberpunk cat on the moon",
    resolution="2048*2048"
)
print(result)
```

### 使用示例 (CLI)

```bash
python3 scripts/kling.py --version "Q2.5T-std" --prompt "A flying car"
```
