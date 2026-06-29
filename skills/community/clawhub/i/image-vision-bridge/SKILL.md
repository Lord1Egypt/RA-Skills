---
name: image-vision
description: 本地图片视觉理解桥接。当用户明确要求分析、描述或理解图片内容时，调用本地 Ollama 视觉模型（qwen3.5:4b）读取图片并以文字描述返回，让不具备多模态能力的推理模型也能"看见"图片。
trigger:
  - 用户明确要求分析、描述、阅读、理解图片内容
  - 用户发送了图片文件并询问相关内容
permissions:
  shell: true
  files: true
  network: true
privacy: >
  图片文件会被读取并以 base64 编码发送到本地 Ollama API（127.0.0.1:11434）。
  所有处理在本机完成，数据不离开你的设备。
---

# Image Vision Bridge

本地视觉桥接 —— 当用户明确要求分析图片时，调用 Ollama 本地视觉模型（qwen3.5:4b / qwen3.5:9b）读图并返回文字描述。

⚠️ **隐私提示**: 图片内容会被读取并发送到本地 Ollama 服务进行处理。所有数据仅在本机传输，不上传云端。

## 使用方式

```bash
python scripts/describe_image.py "<图片路径>"
```

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 视觉模型名 | `qwen3.5:4b` |
| `--prompt` | 自定义分析指令 | 详细描述所有细节 |

### 模型选择

- **qwen3.5:4b** (~3.4GB) — 轻量化，首次加载约30秒，后续秒级响应。适合日常读图。
- **qwen3.5:9b** (~6.6GB) — 更高质量，描述更准确细腻。适合需要精准理解的场景。

### 自定义 prompt 示例

```bash
# 提取图中文字
--prompt "请逐字提取图片中所有文字内容，不要遗漏任何文字。"

# 分析 UI 界面
--prompt "这是一个软件界面截图，请分析其布局、按钮、输入框等交互元素。"

# 提取代码
--prompt "完整提取截图中的代码，保留缩进和格式。"
```

## 工作流程

1. 用户明确要求分析图片 → 检测到图片路径
2. 脚本将图片 base64 编码 → 发送到本地 Ollama API（127.0.0.1）
3. qwen3.5 视觉模型分析图片 → 返回文字描述
4. 描述注入对话 → 基于描述继续完成任务

## 前置条件

- ✅ Ollama 已安装并运行
- ✅ qwen3.5:4b 已拉取（已就绪）
- ✅ Python 3.9+

## 故障排除

如果 Ollama 模型崩溃（"llama-server process has terminated"），需要重启 Ollama 服务：
```bash
# macOS / Linux
pkill ollama && ollama serve &

# Windows (PowerShell)
Get-Process -Name "ollama*" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```
