---
name: modelscope-image-gen
description: 通过魔搭社区(ModelScope) API 生成图片。先使用 --list-models 查看可用模型，然后根据用户需求由 AI 生成专业的提示词，最后调用 API 生成图片。支持 Kolors、Stable Diffusion XL、FLUX 等多种文生图模型。当用户需要使用魔搭社区、ModelScope 或中文 AI 模型生成图片时使用此技能。
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["python3"]
      env: ["MODELSCOPE_API_KEY"]
    primaryEnv: "MODELSCOPE_API_KEY"
    install:
      - id: "python-brew"
        kind: "brew"
        formula: "python"
        bins: ["python3"]
        label: "安装 Python (brew)"
---

# 魔搭社区图片生成

通过魔搭社区（ModelScope）API 调用多种文生图模型生成图片。**使用流程：查看模型列表 → 选择模型 → AI 生成提示词 → 生成图片**。

## 概述

本技能支持通过魔搭社区 API 生成高质量图片。核心特点：

1. **预配置模型列表** - 无需网络请求，直接查看可用模型
2. **AI 生成提示词** - 根据用户需求场景生成专业优化的提示词
3. **多模型支持** - Kolors、Stable Diffusion XL、FLUX 等

## 使用场景

当出现以下情况时使用本技能：

- 用户请求使用魔搭社区或 ModelScope 生成图片
- 用户需要从中文文本提示词生成图片
- 用户需要专业优化的提示词来生成高质量图片

## 工作流程

### 第一步：查看可用模型

```bash
python3 {baseDir}/scripts/gen.py --list-models
```

这会显示完整的模型信息：
- **推荐模型**：预设的高质量模型，包含 ID、名称、说明、支持语言
- **其他模型**：更多支持 API 推理的模型，同样显示完整信息

**模型列表存储在 `references/models.md` 中**，方便后期新增和修改。

### 第二步：选择模型（使用子agent）

**重要**：当需要与用户交互确认风格和模型选择时，**建议使用子agent**处理。

原因：
- 防止上下文污染（模型列表有 30+ 个，详细信息会占用大量 token）
- 模型选择是一个独立决策过程，不应在主对话中展开
- 用户可能需要多次比较不同模型，子agent可以独立处理

**使用方式**：

```python
# 启动子agent处理模型选择
Task(
    subagent_type="general-purpose",
    prompt="根据用户需求，从 references/models.md 中推荐最合适的模型。用户需求：{user_request}",
    description="帮助用户选择合适的文生图模型"
)
```

子agent应：
1. 加载 `references/models.md`
2. 根据用户需求（风格、语言、场景）推荐 2-3 个最合适的模型
3. 说明每个模型的特点和适用场景
4. 等待用户确认
5. 将确认结果返回给主agent

### 第三步：AI 生成专业提示词

根据用户的需求场景，AI 会生成专业的提示词。

**提示词结构**：
```
主体 + 细节描述 + 背景 + 风格 + 光影
```

**示例**：
- 用户需求："生成一张猫的照片"
- AI 生成提示词：`一只优雅的橘猫，蓬松的毛发，灵动的眼神，躺在柔软的沙发上，温馨的家居环境，电影级摄影风格，自然阳光照射`

**提示词生成技巧**请参考：`references/prompt_guide.md`

### 第四步：生成图片

```bash
python3 {baseDir}/scripts/gen.py \
  --prompt "<AI生成的提示词>" \
  --model <用户确认的模型>
```

## 推荐模型

### 核心推荐（默认使用）

| 简称 | 特点 | 支持语言 |
|------|------|----------|
| `kolors` | 快手可图，高质量生成（默认） | 中文、英文 |
| `qwen-image` | 通义千问图像，下载量 230万+ | 中文、英文 |
| `qwen-image-2512` | 通义千问最新版，写实摄影 | 中文、英文 |
| `z-image-turbo` | 阿里造相快速版，下载量 408K | 英文 |
| `flux-dev` | FLUX.1-dev，下载量 130万+ | 英文 |
| `flux-schnell` | FLUX.1 schnell，快速生成 | 英文 |
| `sd-x1` | SDXL，高质量艺术创作 | 英文 |
| `sd-turbo` | SDXL Turbo，快速生成 | 英文 |
| `majicflus` | 麦橘超然，下载量 54万+ | 英文 |

> **完整模型列表**：使用 `--list-models` 查看，或加载 `references/models.md` 查看所有 34 个模型。

### 按场景快速选择

| 场景 | 推荐模型 |
|------|---------|
| 中文提示词 | `kolors`, `qwen-image`, `qwen-image-2512` |
| 快速生成 | `sd-turbo`, `z-image-turbo` |
| 高质量艺术 | `sd-x1`, `flux-dev` |
| 写实摄影 | `qwen-image`, `flux-xhs` |
| 人像 | `sdxl-asian`, `majicmix-realistic` |
| 小红书风格 | `flux-xhs` |

## 使用示例

### 示例 1：人物肖像

```bash
# 查看模型
python3 {baseDir}/scripts/gen.py --list-models

# AI 生成提示词并执行
python3 {baseDir}/scripts/gen.py \
  --prompt "优雅的女性，精致的妆容，温柔的眼神，华丽的晚礼服，城市夜景背景，电影级肖像风格，柔和的伦勃朗光" \
  --model kolors \
  --count 4
```

### 示例 2：自然风景

```bash
python3 {baseDir}/scripts/gen.py \
  --prompt "壮丽的雪山，云雾缭绕，倒影如镜的湖泊，蔚蓝天空，超写实摄影风格，黄金时刻光线" \
  --model sd-x1
```

### 示例 3：赛博朋克城市

```bash
python3 {baseDir}/scripts/gen.py \
  --prompt "未来城市夜景，高耸的摩天大楼，霓虹闪烁的街道，全息广告牌，飞行的汽车，赛博朋克风格，夜幕下的霓虹灯光" \
  --model flux-schnell \
  --count 8
```

## 命令参数

```bash
python3 {baseDir}/scripts/gen.py [选项]

必需参数:
  --prompt TEXT        图片提示词（由 AI 根据用户需求生成）

可选参数:
  --model TEXT         模型名称或 ID [默认: kolors]
  --count INT         生成图片数量 [默认: 4]
  --size TEXT         图片尺寸 [默认: 1024x1024]
  --out-dir PATH      输出目录 [默认: ./tmp/modelscope-image-gen-TIMESTAMP]
  --api-key TEXT      API Key（或设置 MODELSCOPE_API_KEY 环境变量）
  --list-models       列出所有可用的文生图模型
```

## 提示词生成指南

### 核心结构

```
主体 + 细节描述 + 背景 + 风格 + 光影
```

### 五大要素

1. **主体**：画面的核心元素（人物、物体、场景）
2. **细节描述**：动作、表情、服饰、材质、颜色
3. **背景**：环境、场景、氛围
4. **风格**：艺术流派、艺术家风格、视觉风格
5. **光影**：光线类型、方向、强度

### 生成原则

- **词序权重**：重要元素前置
- **具体化**：避免模糊词汇
- **长度控制**：中文 20-50 字
- **风格统一**：元素协调一致

### 快速示例

**人物肖像**
```
优雅的女性，精致的妆容，温柔的眼神，华丽的晚礼服，
城市夜景背景，电影级肖像风格，柔和的伦勃朗光
```

**自然风景**
```
壮丽的雪山，云雾缭绕，倒影如镜的湖泊，
蔚蓝天空，超写实摄影风格，黄金时刻光线
```

**详细指南**请查看：`references/prompt_guide.md`

## 输出内容

生成完成后，输出目录包含：

- `*.png` - 生成的图片文件
- `prompts.json` - 提示词与文件名映射
- `index.html` - HTML 图片库（浏览器打开查看）

## API 端点

**图片生成接口**：
```
POST https://api-inference.modelscope.cn/v1/images/generations
```

**认证方式**：
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**注意**：
- API 兼容 OpenAI 格式
- 可使用 OpenAI SDK 调用
- 详细文档：`references/api_reference.md`

## 使用限制

根据魔搭社区的规定：

1. **仅支持特定模型**：只有标记为 `inference_type` 的模型才能通过 API 调用
2. **非商业用途**：API Inference 为非商业化产品
3. **并发限制**：建议控制并发请求数量
4. **速率限制**：可能存在请求频率限制

详细说明：https://modelscope.cn/docs/model-service/API-Inference/limits

## 故障排除

### 缺少 API Key

```
错误: 缺少 MODELSCOPE_API_KEY
```

解决方案：
```bash
export MODELSCOPE_API_KEY='your-api-key'
```

获取 API Key：https://modelscope.cn/my/myaccesstoken

### 模型不支持 API

确保使用 `--list-models` 中列出的模型。

### 提示词效果不佳

- 增加具体细节描述
- 指定明确的风格
- 调整词序，重要元素前置
- 控制提示词长度（20-50 中文字）

## 相关资源

- **脚本代码**：`scripts/gen.py`
- **API 参考**：`references/api_reference.md`
- **提示词指南**：`references/prompt_guide.md`

## 相关链接

- [魔搭社区官网](https://modelscope.cn)
- [API 推理文档](https://modelscope.cn/docs/model-service/API-Inference/intro)
- [使用限制](https://modelscope.cn/docs/model-service/API-Inference/limits)
- [模型库](https://modelscope.cn/models)
- [AIGC 模型](https://modelscope.cn/aigc/models)
