---
name: pixshop-mcp
description: Pixshop MCP 集成 — 28+ AI 图片视频创意工具，Claude 直接调用 / Pixshop MCP — 28+ AI creative tools for image & video generation, editing, effects in Claude. Use when user wants AI image generation, photo editing, video creation, virtual try-on, face swap, style transfer, or creative effects.
allowed-tools: Bash, Read
---

# Pixshop MCP — AI 图片视频创意工具集 / AI Creative Tools

> **[Pixshop (pixshop.app)](https://pixshop.app)** — AI 图片编辑 & 视频创意平台，对标 Higgsfield.ai

将 Pixshop 的 28+ AI 创意技能作为 MCP 工具接入 Claude Desktop、Cursor 等客户端。一行配置即可获得图片生成、视频制作、人脸替换、虚拟试穿、风格转换等全部能力。

## Setup / 配置

在 Claude Desktop 或 Cursor 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "pixshop": {
      "url": "https://pixshop.app/api/mcp"
    }
  }
}
```

配置完成后重启客户端，即可通过自然语言调用所有工具。

**需要 [Pixshop 账号](https://pixshop.app) + 积分**（新用户注册赠送积分）。

## 工具列表 (28 Tools)

### 生成类 (Generation)

#### 1. `image-generate` — 文本生成图片 (2 credits)

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 图片描述，尽量详细具体 |
| `aspectRatio` | string | | 比例：`1:1`, `16:9`, `9:16`, `4:3`, `3:4` |
| `quality` | string | | 质量：`standard`, `hd` |
| `model` | string | | 模型：nano-banana, flux-2, seedream 等 15+ 模型 |

**示例**: `image-generate({ prompt: "赛博朋克城市夜景，霓虹灯光，雨天", aspectRatio: "16:9" })`

#### 2. `flux-generate` — Flux 模型生成 (3 credits)

高质量图片生成，使用 Flux Pro 模型。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 图片描述 |
| `aspectRatio` | string | | 比例 |

### 编辑类 (Editing)

#### 3. `image-edit` — 图片编辑 (1 credit)

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `prompt` | string | ✅ | 编辑指令 |
| `editType` | string | | 编辑类型 |

#### 4. `background-remove` — 背景移除/抠图 (1 credit)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |

#### 5. `style-transfer` — 风格转换 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `style` | string | ✅ | 风格：anime, oil-painting, watercolor, sketch, cyberpunk, ghibli, pixel-art, minimalist |
| `strength` | number | | 转换强度 0-1，默认 0.8 |

#### 6. `outpaint` — 画面扩展 (3 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `prompt` | string | | 扩展区域描述 |
| `direction` | string | | 扩展方向 |

#### 7. `image-inpaint` — 智能填充/擦除 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `maskUrl` | string | ✅ | 遮罩区域 |
| `prompt` | string | | 填充内容描述 |

#### 8. `reference-guide` — 参考图引导生成 (3 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 参考图片 URL |
| `prompt` | string | ✅ | 生成指令 |

#### 9. `image-fusion` — 图片融合 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 图片 A |
| `imageUrl2` | string | ✅ | 图片 B |
| `prompt` | string | | 融合说明 |

#### 10. `texture-transfer` — 材质迁移 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 |
| `textureUrl` | string | ✅ | 材质参考 |

#### 11. `age-transform` — 年龄变换 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 人像图片 |
| `targetAge` | string | ✅ | 目标年龄段 |

#### 12. `virtual-tryon` — 虚拟试穿 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 人物图片 |
| `garmentUrl` | string | ✅ | 服装图片 |

#### 13. `id-photo` — 证件照生成 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 人像图片 |
| `size` | string | | 证件照尺寸预设 |
| `background` | string | | 背景颜色 |

### 视频类 (Video)

#### 14. `video-generate` — 图片转视频 (6 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `prompt` | string | | 运动描述 |
| `duration` | string | | 时长：5/10/15 秒 |
| `motionType` | string | | 运动类型：zoom-in, zoom-out, pan-left, pan-right, orbit, static |

### 增强类 (Enhancement)

#### 15. `image-upscale` — 图片超分辨率 (3 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `scale` | string | | 倍数：2x, 4x |
| `enhanceDetails` | boolean | | 是否增强细节 |

### 特效类 (Effects)

#### 16. `inflate` — 膨胀效果 (2 credits)
#### 17. `melt` — 融化效果 (2 credits)
#### 18. `explode` — 爆炸效果 (2 credits)
#### 19. `cakeify` — 蛋糕化效果 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `prompt` | string | | 效果描述 |

### 商业类 (Commercial)

#### 20. `product-placement` — 产品植入 (3 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 产品图片 |
| `sceneUrl` | string | ✅ | 场景图片 |
| `prompt` | string | | 植入说明 |

#### 21. `product-showcase` — 产品展示图 (3 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 产品图片 |
| `style` | string | | 展示风格 |

#### 22. `ecommerce-template` — 电商模板 (2 credits)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 产品图片 |
| `template` | string | | 模板类型 |

### 提示词类 (Prompt) — 免费

#### 23. `prompt-search` — 提示词搜索 (free)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `categoryMain` | string | | 主分类 |
| `limit` | number | | 返回数量，默认 5 |

#### 24. `prompt-recommend` — 提示词推荐 (free)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `description` | string | ✅ | 需求描述 |
| `limit` | number | | 推荐数量 |

### Apps 类 (Nano Banana)

#### 25. `app-list` — 应用列表 (free)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `search` | string | | 搜索关键词 |
| `category` | string | | 分类筛选 |
| `limit` | number | | 返回数量 |

#### 26. `app-execute` — 执行应用 (varies)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `appId` | string | ✅ | 应用 ID |
| `prompt` | string | ✅ | 输入提示词 |
| `imageUrl` | string | | 参考图片 |

### 社交类 (Social) — 免费

#### 27. `post-publish` — 发布作品 (free)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 作品图片 |
| `title` | string | ✅ | 标题 |
| `description` | string | | 描述 |

#### 28. `remix-start` — 开始 Remix (free)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `postId` | string | ✅ | 原作品 ID |
| `prompt` | string | | 二创说明 |

## MCP Resources

| Resource URI | 类型 | 说明 |
|-------------|------|------|
| `pixshop://llms.txt` | text/plain | 平台能力概述 |
| `pixshop://tools` | application/json | 全部工具元数据 |

## 典型工作流

### 创意图片生成
`prompt-search("赛博朋克")` → 选择提示词 → `image-generate(prompt, aspectRatio: "16:9")` → `image-upscale(scale: "4x")` → `post-publish()`

### 电商产品图
`background-remove(产品图)` → `product-showcase(style: "minimalist")` → `ecommerce-template(template: "hero")`

### 人像创意
`style-transfer(photo, style: "anime")` → `age-transform(targetAge: "child")` → `inflate()` 膨胀特效

### 视频制作
`image-generate(prompt)` → `image-edit(调整)` → `video-generate(duration: "10", motionType: "orbit")`

## 注意事项

- **积分系统**：所有 AI 生成/编辑操作消耗积分（1-12 credits），免费搜索/浏览不消耗
- **需要登录**：使用 Pixshop 账号，新注册赠送积分
- **图片格式**：支持 PNG, JPEG, WebP，最大 20MB
- **视频生成**：消耗较高（6-12 credits），时长 5/10/15 秒
- **多 Provider 降级**：后端自动在 Gemini/Replicate/OpenRouter 间降级，确保高可用
- **多语言**：支持中/英/日/韩/西/德/法 7 种语言

## 在线体验

- [Pixshop 首页](https://pixshop.app) — AI 创意平台全景
- [Nano Banana Apps](https://pixshop.app/apps) — 48+ AI 应用市场
- [提示词库](https://pixshop.app/prompt-library) — 海量高质量提示词
- [特效展示](https://pixshop.app/effects) — 人像风格化 & 创意特效
- [Design Agent](https://pixshop.app/agent) — AI 设计工作台
- [定价方案](https://pixshop.app/pricing) — 免费 / 高级 / 企业

---
Powered by [Pixshop](https://pixshop.app) — AI 图片编辑 & 视频创意平台
