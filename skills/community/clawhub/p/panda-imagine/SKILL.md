---
name: panda-imagine
description: >-
  多 Provider 图片生成引擎。支持 OpenAI、Azure、Google Gemini、OpenRouter、
  通义万相(DashScope)、MiniMax、即梦(Jimeng)、豆包(Seedream)、Replicate。
  支持文生图、参考图、宽高比、批量生成。
  触发词："生成图片"、"画图"、"generate image"、"create image"。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/hash-panda/panda-skills#panda-imagine
    requires:
      anyBins:
        - bun
        - npx
---

# 图片生成引擎

多 Provider 图片生成引擎，通过统一的 CLI 接口调用 9 种图片生成服务。

## 脚本路径

1. `{baseDir}` = 本 SKILL.md 所在目录
2. 脚本路径 = `{baseDir}/scripts/main.ts`
3. 运行时: `bun` 可用 → `bun`; 否则 `npx -y bun`

## 步骤 0: 加载偏好 ⛔ 阻塞

检查 EXTEND.md：

```bash
test -f .panda-skills/panda-imagine/EXTEND.md && echo "project"
test -f "$HOME/.panda-skills/panda-imagine/EXTEND.md" && echo "user"
```

| 结果 | 操作 |
|------|------|
| 找到 | 加载、解析、应用 |
| 未找到 | ⛔ 运行 [首次配置](references/config/first-time-setup.md) → 保存 → 继续 |

兼容读取: `.baoyu-skills/baoyu-imagine/EXTEND.md`（fallback）

## 使用方式

```bash
# 基本用法
${BUN_X} {baseDir}/scripts/main.ts --prompt "一只猫" --image cat.png

# 指定宽高比
${BUN_X} {baseDir}/scripts/main.ts --prompt "风景画" --image out.png --ar 16:9

# 高质量
${BUN_X} {baseDir}/scripts/main.ts --prompt "一只猫" --image out.png --quality 2k

# 从提示词文件生成
${BUN_X} {baseDir}/scripts/main.ts --promptfiles prompt.md --image out.png

# 参考图（Google, OpenAI, Azure, OpenRouter, Replicate, MiniMax, Seedream）
${BUN_X} {baseDir}/scripts/main.ts --prompt "改为蓝色" --image out.png --ref source.png

# 通义万相
${BUN_X} {baseDir}/scripts/main.ts --prompt "一只可爱的猫" --image out.png --provider dashscope

# MiniMax（角色参考图）
${BUN_X} {baseDir}/scripts/main.ts --prompt "站在窗前" --image out.jpg --provider minimax --ref portrait.png

# 即梦（自动检测 dreamina CLI 或 API 模式）
${BUN_X} {baseDir}/scripts/main.ts --prompt "科技海报" --image out.png --provider jimeng

# 即梦 + 参考图（需要 dreamina CLI）
${BUN_X} {baseDir}/scripts/main.ts --prompt "改为水彩风格" --image out.png --provider jimeng --ref source.png

# 豆包 Seedream
${BUN_X} {baseDir}/scripts/main.ts --prompt "一只猫" --image out.png --provider seedream

# 批量模式
${BUN_X} {baseDir}/scripts/main.ts --batchfile batch.json
```

### 批量文件格式

```json
{
  "jobs": 4,
  "tasks": [
    {
      "id": "hero",
      "promptFiles": ["prompts/hero.md"],
      "image": "out/hero.png",
      "ar": "16:9"
    }
  ]
}
```

## 选项

| 选项 | 描述 |
|------|------|
| `--prompt <text>`, `-p` | 提示词文本 |
| `--promptfiles <files...>` | 从文件读取提示词（多文件拼接） |
| `--image <path>` | 输出图片路径 |
| `--batchfile <path>` | 批量任务 JSON 文件 |
| `--jobs <count>` | 批量 worker 数量（默认自动，上限见配置） |
| `--provider <name>` | 强制指定 Provider |
| `--model <id>`, `-m` | 模型 ID |
| `--ar <ratio>` | 宽高比（如 16:9, 3:4） |
| `--size <WxH>` | 尺寸（如 1024x1024） |
| `--quality normal\|2k` | 质量预设（默认 2k） |
| `--imageSize 1K\|2K\|4K` | 图片尺寸（Google/OpenRouter） |
| `--ref <files...>` | 参考图 |
| `--n <count>` | 生成数量 |
| `--json` | JSON 输出 |

## 环境变量

| 变量 | 描述 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API 密钥 |
| `AZURE_OPENAI_BASE_URL` | Azure 资源端点 |
| `GOOGLE_API_KEY` | Google API 密钥 |
| `OPENROUTER_API_KEY` | OpenRouter API 密钥 |
| `DASHSCOPE_API_KEY` | 通义万相 API 密钥 |
| `MINIMAX_API_KEY` | MiniMax API 密钥 |
| `REPLICATE_API_TOKEN` | Replicate API 令牌 |
| `JIMENG_ACCESS_KEY_ID` | 即梦火山引擎 Access Key（API 模式） |
| `JIMENG_SECRET_ACCESS_KEY` | 即梦火山引擎 Secret Key（API 模式） |
| `ARK_API_KEY` | 豆包 Seedream ARK API 密钥 |

**加载优先级**: CLI 参数 > EXTEND.md > 环境变量 > `.panda-skills/.env` > `~/.panda-skills/.env`

即梦 Provider 无需设置环境变量——安装 dreamina CLI 并登录后即可使用。

## Provider 选择

| Provider | 默认模型 | 参考图 |
|----------|---------|:---:|
| google | gemini-3-pro-image-preview | ✓ |
| openai | gpt-image-1.5 | ✓ |
| azure | gpt-image-1.5 | ✓ |
| openrouter | gemini-3.1-flash-image-preview | ✓ |
| dashscope | qwen-image-2.0-pro | ✗ |
| minimax | image-01 | ✓ |
| jimeng | jimeng_t2i_v40 | ✓(CLI) |
| seedream | doubao-seedream-5-0 | ✓ |
| replicate | google/nano-banana-pro | ✓ |

即梦双模式:
- **CLI 模式**（优先）：安装了 [dreamina CLI](https://jimeng.jianying.com/cli) → 自动使用，支持 `--ref` 参考图
- **API 模式**（fallback）：设置了 `JIMENG_ACCESS_KEY_ID` → 使用火山引擎 HMAC 签名，不支持 `--ref`

安装 dreamina CLI:
```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
dreamina login
```

自动选择逻辑:
1. 有 `--ref` 且无 `--provider` → 按 google > openai > azure > openrouter > replicate > seedream > minimax > jimeng 顺序
2. 指定 `--provider` → 使用该 Provider
3. 仅一个 API Key（或 dreamina CLI）→ 使用对应 Provider
4. 多个可用 → 使用第一个

## 质量预设

| 预设 | Google | OpenAI | 用途 |
|------|--------|--------|------|
| normal | 1K | 1024px | 快速预览 |
| 2k（默认） | 2K | 2048px | 封面、插画、信息图 |

## 错误处理

- API Key 缺失 → 报错并提示设置
- 生成失败 → 自动重试最多 3 次
- 参考图 + 不支持的 Provider → 报错并提示替代方案

## 参考文档

| 文件 | 内容 |
|------|------|
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次配置流程 |
| [references/config/preferences-schema.md](references/config/preferences-schema.md) | EXTEND.md schema |
