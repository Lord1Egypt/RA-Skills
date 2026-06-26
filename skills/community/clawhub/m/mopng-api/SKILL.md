---
name: mopng-api
description: 使用 mopng.cn (MoPNG) API 进行图片处理，包括智能抠图、高清放大、智能扩图、图片翻译、文生图、图生图等功能。支持 API Key 鉴权；处理本地文件时会上传至 MoPNG 服务。
metadata:
  openclaw:
    requires:
      bins:
        - uv
        - python3
      env:
        - MOPNG_API_KEY
        - OPENCLAW_WORKSPACE
    primaryEnv: MOPNG_API_KEY
---

# mopng-api

使用 mopng.cn 的 OpenAPI 进行多种图片处理任务。

## 环境变量

| 变量 | 说明 |
|------|------|
| `MOPNG_API_KEY` | **必填。** 在 https://mopng.cn/agent 获取，通过 OpenClaw 宿主配置或本机环境注入；**不要**在对话、截图或公开仓库中粘贴。 |
| `OPENCLAW_WORKSPACE` | **由宿主注入（OpenClaw 运行时）。** 设为工作区绝对路径时，脚本仅允许该目录内的输入/输出路径；未设置时回退为当前工作目录（例如本地直接运行脚本）。 |
| `MOPNG_EXTRA_ALLOWED_IMAGE_HOSTS` | **可选。** 逗号分隔的额外允许域名或后缀（如 `cdn.example.com`、`.cdn.example.com`），用于 `--input` 传入的远程图片 URL；默认仅允许 `*.mopng.cn`。 |

## API Key 配置

1. 登录 https://mopng.cn/agent 获取 API Key  
2. 仅在 OpenClaw / 客户端**私密配置**或本机 Shell、`.env`（勿提交 Git）中设置 `MOPNG_API_KEY`  
3. 勿将密钥粘贴到 AI 聊天以请模型「代写」环境变量——聊天内容可能留存或被记录，密钥应只进宿主配置或本机私密存储

## 功能列表

| 功能 | 命令 | 计费 |
|------|------|------|
| 智能抠图 | `remove-bg` | 1点/张 |
| 高清放大 | `upscale` | 2点/张 |
| 智能扩图 | `outpainting` | 按量计费 |
| 图片翻译 | `translation` | 按量计费 |
| 文生图 | `text-to-image` | 按量计费 |
| 图生图 | `image-to-image` | 按量计费 |

## Claude 命令使用指南

### 智能抠图 (remove-bg)


**基本用法：**
```
remove-bg ./photo.jpg
```

**指定输出路径：**
```
remove-bg ./photo.jpg --output ./result.png
```

**选项说明：**
- `--output ./result.png` 指定输出路径
- `--output-format png|jpg` 输出格式（默认: png）
- `--return-mask` 返回蒙版
- `--only-mask` 仅返回蒙版
- `--async-mode` 异步模式（大文件建议使用）

---

### 高清放大 (upscale)

**基本用法（2倍放大）：**
```
upscale ./photo.jpg
```

**指定放大倍数：**
```
upscale ./photo.jpg --scale 4 --output ./result.png
```

**选项说明：**
- `--scale 2|4` 放大倍数（默认: 2）
- `--tile-size 192` 瓦片大小（默认: 0）
- `--tile-pad 24` 瓦片填充（默认: 10）
- `--output-format png|jpg` 输出格式
- `--async-mode` 异步模式（建议使用）

---

### 智能扩图 (outpainting)

**基本用法：**
```
outpainting ./photo.jpg
```

**指定扩展方向：**
```
outpainting ./photo.jpg --direction all --expand-ratio 0.5 --output ./result.png
```

**选项说明：**
- `--direction all|up|down|left|right` 扩展方向（默认: all）
- `--expand-ratio 0.1-1.0` 扩展比例（默认: 0.5）
- `--angle 0` 旋转角度
- `--best-quality` 最佳质量

---

### 图片翻译 (translation)

**基本用法：**
```
translation ./photo.jpg --target-language en
```

**选项说明：**
- `--target-language` 目标语言（必填），如 en, zh, ja, ko
- `--source-language` 源语言（默认: auto）
- `--domain-hint` 领域提示
- `--sensitive-word-filter` 敏感词过滤

---

### 文生图 (text-to-image)

**基本用法：**
```
text-to-image --prompt "一只红嘴蓝鹊站在树枝上"
```

**指定输出路径：**
```
text-to-image --prompt "一只可爱的猫咪" --output ./cat.png
```

**选项说明：**
- `--prompt "描述"` 提示词（必填，最长 8000 字符）
- `--model wanx-v2.5` 模型名称（默认: wanx-v2.5）
- `--negative-prompt "描述"` 负面提示词（可选，最长 8000 字符）
- `--width 1024 --height 1024` 图片尺寸
- `--n 1` 生成数量
- `--no-sensitive-word-filter` 关闭服务端敏感词过滤（默认：**开启**）

---

### 图生图 (image-to-image)

**基本用法：**
```
image-to-image --input ./photo.jpg --prompt "把天空变成日落金色"
```

**选项说明：**
- `--input ./photo.jpg` 输入图片路径（必填）
- `--prompt "描述"` 编辑提示词（必填，最长 8000 字符）
- `--model wanx-v2.5` 模型名称（默认: wanx-v2.5）
- `--negative-prompt "描述"` 负面提示词（可选，最长 8000 字符）
- `--strength 0.7` 编辑强度（0.0-1.0，越大变化越大）
- `--width/--height` 输出尺寸
- `--no-sensitive-word-filter` 关闭服务端敏感词过滤（默认：**开启**）

---

### 查看可用模型

```
list-models --type text_to_image
```

---

## 安全约束

- **数据流：** 使用本地文件路径时，图片会经 MoPNG API **上传**至服务方用于处理；远程图片 URL 则直接由服务端拉取。请勿对含敏感内容的图片使用该技能，除非你接受该处理与传输。
- **远程输入 URL：** 仅允许 `https://`，且主机名须在 `*.mopng.cn` 内，或通过 `MOPNG_EXTRA_ALLOWED_IMAGE_HOSTS` 声明的域名；禁止带账号口令的 URL，以降低对任意外链的 SSRF 风险。
- **生成类提示词：** `text-to-image` / `image-to-image` 默认向 API 开启 `sensitive_word_filter`；完整内容与合规判定由 **MoPNG 服务端**策略执行，客户端另限制提示词长度。
- **工作区：** 当 `OPENCLAW_WORKSPACE` 已设置时，本地 `--input` / `--output` 须落在该目录内（脚本会校验）；未设置时以当前工作目录为根。
- 本地 `--input` 须为真实图片文件；允许的输入格式: `.png`, `.jpg`, `.jpeg`, `.webp`
- `--output` 写入 `outputs/mopng-api` 下（工作区相对路径会解析到该目录）
- 大文件会被拒绝（大小与像素上限见实现）

## 异步任务

当任务需要较长时间处理时，会自动进入异步模式。系统会轮询直到任务完成。

**轮询间隔：** 2-5 秒

## 注意事项

- API 调用会消耗账户积分
- 本地图片会自动上传到临时存储获取 URL
- 远程输入须为 **https** 且主机在允许列表中（见上）；不需本地上传
- 仓库 CI 对 `scripts/` 运行 `pytest` 与 `bandit`，便于持续做基础安全扫描
