---
name: gnano-ihogmn
description: GNano Ihogmn 图片生成技能 - 支持动态 API 配置，根据 Token 自动获取可用功能，支持文生图和图生图
---

# GNano Ihogmn 图片生成技能 V1

GNano Ihogmn 图片生成技能 - 第一版。支持动态 API 配置，根据用户提供的 Token 自动获取可用功能和参数。

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 验证安装

```bash
python scripts/get_config.py --token "YOUR_API_TOKEN"
```

## 核心特性

- **动态配置**: 不内嵌 API Token，每个新任务需要用户提供
- **自动探测**: 根据 Token 获取该账户支持的模型、分辨率、参考图限制等
- **任务记忆**: 在同一任务会话内记住配置，后续对话快速出图
- **模型支持**: 自动适配 gemini-3-pro-image-preview 和 gemini-3.1-flash-image-preview
- **路径处理**: 支持相对路径和绝对路径，自动转换

## 使用流程

### 1. 新建任务（首次对话）

用户首次使用或明确说"新建任务"时：

**步骤 1: 请求 API Token**
```
"请提供您的 GNano API Token，我将根据您的账户配置获取可用功能。"
"如果您没有 Token，请访问 https://gnano.ihogmn.top 获取。"
```

**步骤 2: 验证并获取配置**
```bash
python scripts/get_config.py --token "用户提供的TOKEN"
```

返回配置示例：
```json
{
  "success": true,
  "api_token": "xxx",
  "api_url": "https://gnano.ihogmn.top",
  "models": ["gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview"],
  "default_model": "gemini-3.1-flash-image-preview",
  "resolutions": ["1K", "2K", "4K"],
  "default_resolution": "2K",
  "max_reference_images": 2,
  "max_reference_size_mb": 2,
  "rate_limit_per_minute": 2
}
```

**步骤 3: 向用户展示配置**
```
"✅ 配置成功！您的账户支持以下功能：
- 可用模型: gemini-3.1-flash-image-preview, gemini-3-pro-image-preview
- 默认模型: gemini-3.1-flash-image-preview
- 支持分辨率: 1K, 2K, 4K
- 参考图限制: 最多2张，每张≤2MB
- 速率限制: 每分钟2张

现在可以直接告诉我您想生成什么图片了！"
```

### 2. 常规出图对话

在同一任务内，用户直接说：
- "出图：一只可爱的猫咪"
- "生成一张风景图"

**执行命令：**
```bash
python scripts/generate_image.py \
  --token "YOUR_TOKEN" \
  --prompt "一只可爱的猫咪" \
  --model "gemini-3.1-flash-image-preview" \
  --resolution "2K" \
  --output "result.png"
```

#### 使用参考图（图生图）

**使用方法：**

1. **将参考图放到工作区目录**
   - 把图片文件复制到工作区目录
   - 或使用绝对路径

2. **使用参考图生成**
   ```bash
   python scripts/generate_image.py \
     --token "YOUR_TOKEN" \
     --prompt "将图中人物外套脱掉" \
     --reference "woman.jpg" \
     --output "result.png"
   ```

**注意：**
- 参考图必须已保存到工作区目录
- 支持最多 2 张参考图，每张不超过 2MB
- 支持格式：PNG, JPG, JPEG, WEBP, GIF
- 支持相对路径和绝对路径

### 3. 切换任务/重置配置

用户说：
- "新建任务"
- "切换 Token"
- "重置配置"

清除当前保存的配置，然后返回步骤 1，重新请求 API Token。

## 脚本说明

### get_config.py - 获取配置

验证 API Token 并获取账户能力配置。

```bash
# 基本用法
python scripts/get_config.py --token "YOUR_API_TOKEN"

# 指定自定义 API 地址
python scripts/get_config.py --token "YOUR_API_TOKEN" --api-url "https://custom.api.com"

# 保存配置到文件
python scripts/get_config.py --token "YOUR_API_TOKEN" --output "config.json"
```

**返回字段：**
- `success`: 是否成功
- `api_token`: API Token
- `api_url`: API 地址
- `models`: 可用模型列表
- `default_model`: 默认模型
- `resolutions`: 支持的分辨率
- `default_resolution`: 默认分辨率
- `max_reference_images`: 最大参考图数量
- `max_reference_size_mb`: 参考图大小限制(MB)
- `rate_limit_per_minute`: 每分钟出图限制
- `error`: 错误信息（如有）
- `warning`: 警告信息（如有）

### generate_image.py - 生成图片

根据配置生成图片。

```bash
# 基本用法
python scripts/generate_image.py --token "TOKEN" --prompt "提示词"

# 完整参数
python scripts/generate_image.py \
  --token "TOKEN" \
  --prompt "一只可爱的猫咪" \
  --api-url "https://gnano.ihogmn.top" \
  --model "gemini-3.1-flash-image-preview" \
  --available-models "gemini-3.1-flash-image-preview,gemini-2.5-flash-image" \
  --resolution "2K" \
  --reference "ref1.png,ref2.png" \
  --output "output.png" \
  --max-ref 2 \
  --max-ref-size 2
```

**参数说明：**
- `--token, -t`: API Token（必需）
- `--prompt, -p`: 提示词（必需）
- `--api-url, -u`: API 地址
- `--model, -m`: 模型名称（优先使用）
- `--available-models`: 可用模型列表（逗号分隔，用于自动选择最佳模型）
- `--resolution, -r`: 分辨率 (1K, 2K, 4K)
- `--reference, -ref`: 参考图路径，多个用逗号分隔
- `--output, -o`: 输出图片路径
- `--max-ref`: 最大参考图数量
- `--max-ref-size`: 参考图大小限制(MB)
- `--verbose, -v`: 输出详细日志

**返回字段：**
- `success`: 是否成功
- `output_path`: 输出图片路径
- `model`: 使用的模型
- `mime_type`: 图片 MIME 类型
- `file_size`: 文件大小（字节）
- `file_size_mb`: 文件大小（MB）
- `references_used`: 使用的参考图数量
- `elapsed_time`: 生成耗时（秒）
- `error`: 错误信息（如有）
- `details`: 详细错误信息（如有）

**进度输出（stderr）：**
脚本会输出 JSON 格式的进度信息到 stderr：
```json
{"type": "progress", "message": "使用模型: gemini-3.1-flash-image-preview", "step": 1, "total": 5}
{"type": "progress", "message": "正在生成图片，请稍候...", "step": 4, "total": 5}
```

## 任务状态管理

任务状态可以保存在工作区的 `.workbuddy/gnano-tasks/` 目录下：

```
WORKSPACE/
└── .workbuddy/
    └── gnano-tasks/
        ├── {conversation_id}.json   # 当前对话的任务状态
        └── {other_conv_id}.json     # 其他对话的任务状态
```

任务状态文件格式：
```json
{
  "api_token": "your-token",
  "api_url": "https://gnano.ihogmn.top",
  "models": ["gemini-3.1-flash-image-preview"],
  "default_model": "gemini-3.1-flash-image-preview",
  "resolutions": ["1K", "2K", "4K"],
  "default_resolution": "2K",
  "max_reference_images": 2,
  "max_reference_size_mb": 2,
  "rate_limit_per_minute": 2,
  "supports_text_to_image": true,
  "supports_image_editing": true,
  "created_at": "2026-03-23T08:00:00",
  "updated_at": "2026-03-23T08:00:00",
  "last_accessed_at": "2026-03-23T08:00:00"
}
```

任务状态的读取和写入由 WorkBuddy 自动处理，无需额外脚本。

## 完整对话示例

### 示例 1: 新建任务并出图

**用户**: "我想用 GNano 出图"

**助手**: 
"请提供您的 GNano API Token，我将根据您的账户配置获取可用功能。
如果您没有 Token，请访问 https://gnano.ihogmn.top 获取。"

**用户**: "我的 Token 是 abc123"

**助手**: 
```bash
python scripts/get_config.py --token "abc123"
```

"✅ 配置成功！您的账户支持以下功能：
- 可用模型: gemini-3.1-flash-image-preview
- 默认模型: gemini-3.1-flash-image-preview
- 支持分辨率: 1K, 2K, 4K
- 参考图限制: 最多2张，每张≤2MB
- 速率限制: 每分钟2张

现在可以直接告诉我您想生成什么图片了！"

**用户**: "出图：一只可爱的猫咪在草地上玩耍"

**助手**:
```bash
python scripts/generate_image.py --token "abc123" --prompt "一只可爱的猫咪在草地上玩耍" --model "gemini-3.1-flash-image-preview" --resolution "2K" --output "generated_cat.png"
```

[显示生成的图片]

### 示例 2: 使用参考图

**用户**: "参考图：woman.jpg，提示词：将外套脱掉"

**助手**:
```bash
python scripts/generate_image.py --token "abc123" --prompt "将外套脱掉" --reference "woman.jpg" --model "gemini-3.1-flash-image-preview" --resolution "2K" --output "result.png"
```

[显示生成的图片]

### 示例 3: 切换 Token

**用户**: "我想换一个 Token"

**助手**:
"已清除当前配置。请提供新的 GNano API Token："

## 依赖要求

### 必需依赖
- **Python**: >= 3.8
- **requests**: >= 2.31.0 (用于 HTTP 请求)

### 安装方法
```bash
pip install requests
```

## 安装 troubleshooting

### 问题：requests 模块找不到
**解决**: 安装依赖
```bash
pip install requests
```

### 问题：Python 版本过低
**解决**: 升级 Python 到 3.8 或更高版本
```bash
# 检查版本
python --version
```

## 注意事项

1. **所有回复使用中文**
2. **首次对话必须请求 API Token**，不能跳过
3. **同一任务内记住配置**，后续对话快速出图，无需重复输入 Token
4. **Token 仅保存在本地任务状态**，不对外传输
5. **支持相对路径和绝对路径**，自动转换
6. **严格遵守速率限制**，每分钟最多2张
7. **参考图限制**：最多2张，每张不超过2MB
8. **如果 Token 失效**，提示用户重新提供

## 错误处理

### Token 无效
```
"❌ API Token 无效或已过期。请检查您的 Token 是否正确，或重新获取一个新的 Token。"
```

### 请求过于频繁
```
"⚠️ 请求过于频繁，请稍后再试。您的账户限制为每分钟2张图片。"
```

### 参考图过大
```
"⚠️ 参考图超过大小限制（2MB）。请压缩图片后重试。"
```

### 网络错误
```
"❌ 无法连接到 API 服务器。请检查网络连接后重试。"
```
