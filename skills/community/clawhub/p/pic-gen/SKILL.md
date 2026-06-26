---
name: pic-gen
description: Tired of getting mediocre AI images? This skill solves the problem: you describe what you want in plain language, and pic-gen (1) picks the best model for your scene, and (2) rewrites your description into professional-grade prompts that actually produce stunning results. Supports Qwen Wanxiang, Banana/Flux, DALL-E 3 — or just the prompt output if you prefer your own pipeline. Trigger: "draw a...", "generate image of...", "optimize this prompt", "AI art".
requires:
  python:
    packages: ["requests", "pyyaml", "banana-dev"]
  bins: []
---

# pic-gen — AI 图片生成与提示词优化

## 产品对话交互策略

pic-gen 的核心理念：**像和产品经理对话一样，一步一步引导用户完成图片生成**，而不是堆参数。

### 对话状态机

```
IDLE
  │
  ├─ 用户描述图片需求 ──────────────────────────→ ASK_MODEL
  │
ASK_MODEL
  │
  ├─ 用户说「通义」/「qwen」 ─→ 读取 config，默认用 qwen ─→ CONFIRM_PROMPT
  ├─ 用户说「banana」/「flux」 ─→ 用 banana ─→ CONFIRM_PROMPT
  ├─ 用户说「dalle」 ─→ 用 dalle ─→ CONFIRM_PROMPT
  ├─ 用户说「直接生成」 ─→ 用 config 默认模型 ─→ CONFIRM_PROMPT
  │
CONFIRM_PROMPT
  │
  ├─ 用户说「可以/好/生成」 ─→ OPTIMIZE → GENERATE
  ├─ 用户说「改一下 XXX」 ─→ 修改提示词 ─→ CONFIRM_PROMPT
  │
GENERATE
  │
  ├─ 图片生成成功 ─→ 返回图片 + 操作选项 ─→ IDLE
  └─ 生成失败 ─→ 错误原因 + 重试选项 ─→ GENERATE
```

### 首次使用流程

```
用户：「画一只猫」
  ↓
Bot：「好的！想用什么模型生成？」
  「1. 通义万相（默认）2. Banana (Flux) 3. DALL-E」
  ↓
用户：「1」
  ↓
Bot 检测到 config 里没有 API key，询问用户：
  「请提供你的 DashScope API Key」

  同时告知用户也可以手动配置：
  「💡 也可以手动配置：编辑 pic-gen/config/models.yaml，填入 api_key 字段。
   ⚠️ 注意：不要把包含真实 Key 的配置文件分享给他人。」

  ↓
用户：「sk-xxxxxxxx」
  ↓
Bot 写入 config/models.yaml，并回复：
  「✅ Key 已保存！正在生成…」
  ↓
Bot 优化提示词 → 生成图片 → 返回
```

### 密钥更新流程

用户可以说：
- 「更新通义 key 为 sk-xxx」
- 「换成 banana」
- 「设置默认模型为 dalle」

Bot 自动修改 `config/models.yaml`，无需重启。

### 专家模式（一步直达）

用户也可以一句话搞定所有参数：
- 「用 flux 生成赛博朋克城市，16:9，高细节」
- 「qwen, 梵高风格画向日葵」

### 提示词确认流程

```
Bot：「为你优化后的提示词如下：」
📝 通义万相版：「一片向日葵花田，梵高后印象派风格，浓烈的黄色和蓝色对比，笔触感，星空下的夜晚」
🎨 Midjourney 版：「a sunflower field, post-impressionist style Van Gogh, vivid yellow and blue contrast, brushstroke texture, starry night, --ar 16:9 --s 400」
⚡ Stable Diffusion 版：「masterpiece, best quality, sunflower field, Van Gogh style, post-impressionist, vivid colors, starry night background, oil painting」
[✅ 生成] [✏️ 修改提示词] [⚙️ 调整参数]
```

---

## 目录结构

```
pic-gen/
├── SKILL.md               ← 本文件
├── config/
│   └── models.yaml        ← 模型配置文件（用户 API Key 在此）
├── scripts/
│   ├── optimize.py         ← 核心：提示词优化
│   ├── generate_qwen.py   ← 通义万相生成器
│   ├── generate_banana.py ← Banana/Flux 生成器
│   └── generate_dalle.py  ← DALL-E 生成器
└── references/
    ├── midjourney.md      ← MJ 格式参考
    ├── stable-diffusion.md ← SD 格式参考
    ├── flux.md            ← Flux 格式参考
    └── dalle.md           ← DALL-E 格式参考
```

---

## 提示词优化规则（optimize.py）

输入：用户简单描述（中文或英文）
输出：各平台优化后的提示词

### 优化维度

| 维度 | 说明 | 示例 |
|---|---|---|
| 主体 | 具体物种/颜色/动作/表情 | 「猫」→「橘猫，坐姿，眯眼打盹」 |
| 场景 | 地点/时间/天气/背景 | 「在户外」→「京都寺庙庭院，春日午后」 |
| 风格 | 艺术家/流派/渲染方式 | 「好看」→「宫崎骏动画风格，柔和光影」 |
| 光影 | 光源方向/软硬/色温 | 「亮」→「逆光，金色边缘光，暖色调」 |
| 构图 | 视角/焦距/景深/比例 | 「拍猫」→「低角度平视，浅景深，85mm」 |
| 氛围 | 情绪词/色调关键词 | 「开心」→「活泼，明亮，童趣」 |
| 技术参数 | 平台专属参数 | --ar 16:9 / --s 400 / negative prompt |

### 平台输出格式

```python
# platforms: ["qwen", "midjourney", "stable_diffusion", "flux", "dalle"]
# each platform returns optimized string
```

---

## 配置管理（config/models.yaml）

### API Key 安全说明 ⚠️

**API Key = 你的账号密码，禁止泄露或分享。**

- **不要**把包含真实 Key 的配置文件发到 GitHub、Discord、群聊等任何公开或 semi-public 地方
- 提交到 GitHub 前，确保 `config/models.yaml` 中 api_key 字段为空或使用环境变量
- 建议使用环境变量方式引用 Key，而非直接写在 yaml 里：

```yaml
# 方式一：直接填写（仅本地使用，不提交到 Git）
models:
  qwen:
    api_key: "sk-xxxxxxxx"

# 方式二：留空，通过环境变量注入（推荐）
models:
  qwen:
    api_key: ""
```

```bash
# 运行前设置环境变量
export DASHSCOPE_API_KEY="sk-xxxxxxxx"
export BANANA_API_KEY="your-banana-key"
export OPENAI_API_KEY="sk-xxxxxxxx"
```

### 配置文件位置

```
pic-gen/config/models.yaml
```

用户可通过以下任一方式配置：

| 方式 | 说明 |
|---|---|
| **对话提供** | 直接发送 Key 给 Bot，Bot 自动写入配置文件 |
| **手动编辑** | 编辑 `config/models.yaml`，填入 api_key |
| **环境变量** | 设置 `DASHSCOPE_API_KEY` / `BANANA_API_KEY` / `OPENAI_API_KEY` |

### 配置文件格式

```yaml
default: qwen

models:
  qwen:
    enabled: true
    api_key: ""          # 填写你的 DashScope API Key
    model: "qwen-image-2.0-pro"
    default_size: "1024*1024"
    default_style: "auto"

  banana:
    enabled: false
    api_key: ""          # 填写你的 Banana API Key
    model: "flux-dev"
    default_size: "1024*1024"

  dalle:
    enabled: false
    api_key: ""          # 填写你的 OpenAI API Key
    model: "dall-e-3"
    default_size: "1024*1024"
```

### 配置操作命令

| 用户说 | Bot 操作 |
|---|---|
| 「设置通义 key 为 xxx」 | 写入 `models.qwen.api_key` |
| 「开启 banana」 | 写入 `models.banana.enabled: true` |
| 「设置默认模型为 flux」 | 写入 `default: banana` |
| 「查看当前配置」 | 读取并展示（非敏感字段） |

---

## 脚本说明

### optimize.py

```bash
python3 scripts/optimize.py --input "一只猫" --platform qwen
```

把简单描述转化为各平台最优提示词。

### generate_qwen.py

```bash
python3 scripts/generate_qwen.py \
  --prompt "优化后的提示词" \
  --size 1024*1024 \
  --count 1 \
  --download \
  --output ./output
```

需要 `DASHSCOPE_API_KEY` 环境变量或 config 中的 api_key。

### generate_banana.py

```bash
python3 scripts/generate_banana.py \
  --prompt "optimized prompt" \
  --model flux-dev \
  --download \
  --output ./output
```

需要 `BANANA_API_KEY` 环境变量。

### generate_dalle.py

```bash
python3 scripts/generate_dalle.py \
  --prompt "optimized prompt" \
  --size 1024x1024 \
  --download \
  --output ./output
```

需要 `OPENAI_API_KEY` 环境变量。

---

## 平台格式参考（references/）

详细格式说明、参数列表、示例提示词见各参考文件。

---

## 版本

- v0.1.0 - 初始骨架

