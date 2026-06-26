---
name: image-assets-resize
description: 直接以参考KV/海报/拍脸图为输入，调用 gpt-image-2 或 Nano Banana 模型，按目标规格批量生成精确尺寸的图片文件，交付前AI自检文字裁切、元素完整性等问题。支持自定义规范学习、产品设计语言积累。
version: 1.0.0
author: OrangeMoon
trigger: 用户需要根据参考KV/海报/拍脸图适配生成不同尺寸的图片物料、延展KV尺寸、批量生产多平台配图
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
        - GPT_IMAGE2_API_KEY
      bins:
        - python3
    emoji: "🖼️"
    homepage: https://github.com/openclaw/clawhub
    skillKey: image-resize
args:
  - name: image-path
    description: 参考KV/海报路径（直接作为 edit 输入）
    required: false
  - name: platforms
    description: 目标平台Key，逗号分隔。支持内置平台(wechat-cover/douyin-cover/xiaohongshu-cover/bilibili-cover等) 或自定义格式"名称:宽x高"
    required: true
  - name: scene
    description: 活动/场景名称（用于文件名和 prompt）
    required: true
  - name: brand
    description: 品牌名称
    required: false
  - name: quality
    description: 生成质量 low/medium/high
    required: false
  - name: output-dir
    description: 输出目录
    required: false
  - name: extra-prompt
    description: 额外指令。添加元素如"顶部加'五一狂欢'文字"；去除元素如"不要带logo"
    required: false
  - name: verify
    description: 生成后 AI 自检验证
    required: false
output:
  type: object
  properties:
    success: boolean
    total: number
    ok: number
    results:
      type: array
      items:
        type: object
        properties:
          platform: string
          output_path: string
          success: boolean
          error: string
    output_dir: string
    scene: string
  example: |
    {"tool": "image-assets-resize", "success": true, "total": 2, "ok": 2,
     "results": [
       {"platform": "wechat-cover", "output_path": "output/xxx_wechat.png", "success": true},
       {"platform": "douyin-cover", "output_path": "output/xxx_douyin.png", "success": true}
     ],
     "output_dir": "output", "scene": "五一活动"}
---

# Image Assets Resize — 图片物料尺寸延展

直接以参考KV/海报/拍脸图为输入，调用 gpt-image-2 或 Nano Banana 模型原图延展，
按目标规格批量生成精确尺寸的图片文件，交付前AI自检文字裁切、元素完整性等问题。

## 核心思路

把参考图直接传给图像模型的 edit 模式，用一句中文描述目标尺寸即可。模型原生理解图片内容，无需先分析再描述，也无需中间裁切。

## 快速开始

```bash
# 0. 首次使用：初始化配置（选择模型、设置API密钥）
python scripts/generate_image.py --setup

# 1. 根据参考图生成单平台配图
python scripts/generate_image.py \
  -i 参考KV.png \
  -p wechat-cover \
  -s "五一福利活动"

# 2. 多平台批量生成
python scripts/generate_image.py \
  -i 参考KV.png \
  -p wechat-cover,xiaohongshu-cover,douyin-cover \
  -s "618大促"

# 3. 高质量 + AI自检
python scripts/generate_image.py \
  -i 参考KV.png \
  -p wechat-cover,weibo-horizontal \
  -s "双11活动" \
  -q high \
  --verify

# 4. 需要添加文字/图标时使用 --extra-prompt
python scripts/generate_image.py \
  -i 参考KV.png \
  -p douyin-cover \
  -s "五一活动" \
  --extra-prompt "在顶部添加文字'五一狂欢'，底部加一个红色按钮"

# 5. 需要纯净版（去除原图LOGO/文案）
python scripts/generate_image.py \
  -i 参考KV.png \
  -p douyin-cover \
  -s "王者荣耀" \
  --extra-prompt "不要带logo"

# 6. 查看所有平台
python scripts/generate_image.py --list-platforms

# 7. 查看平台规格详情
python scripts/generate_image.py --get-spec wechat-cover

# 8. 自定义平台规格（临时使用，自动学习）
python scripts/generate_image.py \
  -i 参考KV.png \
  -p "我的海报:1200x800" \
  -s "五一活动"
# 首次使用后自动保存为 custom_我的海报_1200x800，下次可直接用 -p custom_我的海报_1200x800

# 9. 永久添加自定义平台规格
python scripts/generate_image.py --add-spec "我的海报" 1200 800

# 10. 列出所有自定义规格
python scripts/generate_image.py --list-custom
```

## 支持的模型

| 模型 | 配置名称 | 说明 |
|------|---------|------|
| **GPT Image 2** | `gpt-image-2` | OpenAI 官方图像生成模型，速度快，质量稳定 |
| **Nano Banana 2** | `nano-banana-2` | Google Gemini 3.1 Flash Image，性价比高，中文渲染好 |
| **Nano Banana Pro** | `nano-banana-pro` | Google Gemini 3 Pro Image，专业级画质 |

通过 `--setup` 选择模型，或直接编辑 `~/.content-marketing/config.json`。

## 完整流程

```
首次使用: --setup 选择模型 → 配置API地址/密钥
  ↓
输入参考图 (-i)
  ↓
[1] 查询平台规格 → 确定目标尺寸
  ↓
[2] 计算合法生成尺寸 → 16 的倍数且 ≥ 1MP
  ↓
[3] 一句话 prompt 调用 backend（gpt-image-2 / nano-banana）
     → "以这张参考图为基准，适配生成一张【平台名】，尺寸WxH..."
  ↓
[4] 微缩放至精确尺寸（通常 ≤ 1%，无视觉损失）
  ↓
[5]（可选）AI 自检验证
  ↓
[6] 规范命名保存 + 记录品牌学习数据
```

## 命令行参数

| 参数 | 简写 | 说明 | 必填 |
|------|------|------|------|
| `--image-path` | `-i` | 参考KV/海报路径（直接作为 edit 输入） | 推荐 |
| `--brand` | `-b` | 品牌名称（默认 "default"） | 否 |
| `--platforms` | `-p` | 目标平台Key，逗号分隔 | 是 |
| `--scene` | `-s` | 活动/场景名称 | 是 |
| `--quality` | `-q` | low/medium/high（默认 medium） | 否 |
| `--output-dir` | `-o` | 输出目录（默认 output/） | 否 |
| `--version` | | 版本号（默认 1） | 否 |
| `--verify` | | 生成后执行 AI 自检验证 | 否 |
| `--extra-prompt` | | 额外指令。添加元素：`"顶部加'五一狂欢'文字"`；去除元素(纯净版)：`"不要带logo"` | 否 |
| `--dry-run` | | 预览 prompt 不生成图片 | 否 |
| `--setup` | | 初始化配置向导（选择模型、设置API） | 否 |
| `--show-config` | | 显示当前配置 | 否 |
| `--add-spec` | | 添加自定义平台规格，如 `--add-spec "我的平台" 1200 800` | 否 |
| `--remove-spec` | | 删除自定义平台规格，如 `--remove-spec custom_我的平台_1200x800` | 否 |
| `--list-custom` | | 列出所有自定义规格 | 否 |
| `--base64` | | 云端模式：结果 JSON 中包含 base64 编码图片，供 OpenClaw 直接展示给用户 | 否 |

## 输出规范

```
output/{场景}_{平台名称}_{宽}x{高}_v{版本}.png
```

示例：
```
output/五一福利活动_微信公众号封面_900x383_v1.png
output/五一福利活动_抖音视频封面_1080x1920_v1.png
output/618大促_小红书笔记封面_1242x1660_v1.png
```

## 尺寸处理逻辑

图像模型要求宽高为 16 的倍数且总像素数不低于约 1MP。工具自动处理：

1. 以目标尺寸为基准，等比例放大到满足最低像素预算
2. 对齐到最近的 16 倍数
3. 生成后微缩放至精确目标尺寸（缩放因子通常 ≥ 0.94，无视觉损失）

例如：目标 900×383 → 生成尺寸 1536×656 → 缩放至 900×383（比例差 < 1%）

## Prompt 模式

| 模式 | 触发条件 | 行为 |
|:----|:---------|:-----|
| **完整版（默认）** | 不加 `--extra-prompt` | 保留原图所有视觉元素（角色/文字/图标/装饰），仅调整构图 |
| **纯净版** | `--extra-prompt "不要带logo"` | 仅保留角色和背景，去除文字/LOGO/装饰 |
| **添加元素** | `--extra-prompt "加文字..."` | 在保留原图基础上按指令添加新元素 |

## AI 自检（可选）

添加 `--verify` 参数启用 GPT-4o 质量检查，检测文字裁切、元素完整性等问题。

## 自学习与反馈

每次生成后可通过 feedback 记录评分和意见，系统会累积品牌设计语言。

```bash
python scripts/generate_image.py --feedback "品牌名" 0 5 "配色准确，继续保持"
```

## 支持的平台规格

| 场景 | 尺寸 | 比例 |
|------|------|------|
| 微信公众号封面 | 900×383 | 900:383 |
| 公众号方形缩略图 | 300×300 | 1:1 |
| 朋友圈竖版海报 | 1080×1920 | 9:16 |
| 朋友圈方版海报 | 1080×1080 | 1:1 |
| 小红书封面 | 1242×1660 | 3:4 |
| 小红书方版 | 1080×1080 | 1:1 |
| 抖音封面 | 1080×1920 | 9:16 |
| 微博横版 | 1200×675 | 16:9 |
| 微博方版 | 1200×1200 | 1:1 |
| 微博竖版 | 1200×1500 | 4:5 |
| 视频号封面 | 1080×1080 | 1:1 |
| B站封面 | 1146×717 | 16:10 |
| 知乎封面 | 1080×1080 | 1:1 |
| 淘宝主图 | 800×800 | 1:1 |
| 快手封面 | 1080×1920 | 9:16 |
| Facebook 方版贴文 | 1200×1200 | 1:1 |
| Facebook 横版贴文 | 1200×630 | 40:21 |
| Facebook 封面照片 | 1200×628 | 300:157 |
| Facebook 快拍 | 1080×1920 | 9:16 |
| Instagram 方版贴文 | 1200×1200 | 1:1 |
| Instagram 竖版贴文 | 630×1200 | 21:40 |
| Instagram 快拍 | 1080×1920 | 9:16 |
| X (Twitter) 方版贴文 | 1200×1200 | 1:1 |
| X (Twitter) 横版贴文 | 1200×900 | 4:3 |
| X (Twitter) 封面横幅 | 1500×500 | 3:1 |
| X (Twitter) 信息流图片 | 1600×900 | 16:9 |
| Pinterest 图钉 | 1000×1500 | 2:3 |
| Pinterest 方版图钉 | 1000×1000 | 1:1 |
| Pinterest Idea Pin | 1080×1920 | 9:16 |
| LinkedIn 横版贴文 | 1200×627 | 1200:627 |
| LinkedIn 方版贴文 | 1080×1080 | 1:1 |
| LinkedIn 公司封面 | 1128×191 | 1128:191 |

完整规格含安全区说明见 [references/platform-specs.md](references/platform-specs.md)。

## 云端 OpenClaw 部署

当这个 skill 部署在云端 OpenClaw 时，用户通过会话交互：

```
用户 ──(上传参考图 + 文字需求)──→ OpenClaw Agent
                                      │
                         保存上传图片到临时目录
                                      │
                         调用 python generate_image.py \
                           -i <临时路径> -p wechat-cover -s "五一" --base64
                                      │
                         脚本输出 JSON（含 base64 图片）
                                      │
                         Agent 解析 JSON，将会话中的图片展示给用户
                                      │
用户 ←──(收到适配后的图片)──── OpenClaw Agent
```

### 输入流程

1. 用户在会话中直接上传原始图片素材
2. OpenClaw Agent 收到上传文件，保存到服务器临时目录
3. Agent 调用 `generate_image.py`，将临时路径传入 `--image-path`
4. 如果 OpenClaw 不支持文件上传，需要将图片先转存到可访问的 URL，或通过其他方式传入

### 输出流程

1. 脚本生成图片后保存到本地，同时输出 `## Result` JSON
2. **普通模式**（不加 `--base64`）：JSON 只包含路径，需要 Agent 自行读取文件返回给用户
3. **云端模式**（`--base64`）：JSON 中每个成功结果包含 `image_base64` 字段，Agent 可直接用 `data:image/png;base64,...` 在会话中展示
4. 建议云端调用始终加 `--base64` 参数

### 示例输出（--base64 模式）

```json
{
  "tool": "image-assets-resize",
  "success": true,
  "total": 2,
  "ok": 2,
  "results": [
    {
      "platform": "wechat-cover",
      "output_path": "output/五一_微信公众号封面_900x383_v1.png",
      "success": true,
      "image_base64": "iVBORw0KGgo..."
    }
  ],
  "output_dir": "output",
  "scene": "五一"
}
```

配置文件位置：`~/.content-marketing/config.json`

```json
{
  "backend": "gpt-image-2",
  "base_url": "https://api.openai.com/v1",
  "api_key_env": "OPENAI_API_KEY"
}
```

| 字段 | 说明 |
|------|------|
| `backend` | `gpt-image-2` / `nano-banana-2` / `nano-banana-pro` |
| `base_url` | API 地址（可配置中转网关） |
| `api_key_env` | 环境变量名（推荐，避免密钥明文存储） |
| `api_key` | 密钥明文（不推荐，仅当无法使用环境变量时） |

通过 `--setup` 交互式配置，或直接编辑 JSON 文件。

## 自定义平台规格

三种方式新增自定义规格：

**1. 内联格式（即用即学）**
```
-p "我的平台:宽x高"
```
首次使用自动保存，下次可直接用 key 调用。

**2. 永久添加**
```
--add-spec "平台名称" 宽度 高度
```
保存后永久可用，`--list-custom` 查看所有自定义规格。

**3. 删除**
```
--remove-spec custom_key
```

自定义规格存储在 `~/.content-marketing/custom_specs.json`，可与他人共享复制。
