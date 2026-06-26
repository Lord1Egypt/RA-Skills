# Parameter Guide — 参数优化指南

> **核心**: 提示词优化 + 宽高比选择

---

## 1. 提示词优化 (Prompt Engineering)

### 1.1 任务类型识别

**关键原则**: 修改任务不要动用户提示词！

| 任务类型 | 特征 | 提示词处理 |
|---------|------|-----------|
| **新生成** (text-to-image) | 用户要求生成全新图像/视频 | ✅ 优化提示词 |
| **修改任务** (image-to-image) | 用户提供参考图 + 修改要求 | ❌ **保持原样** |

**为什么修改任务不优化？**
- 用户提示词是**精确的修改意见**
- 擅自优化可能曲解用户意图
- 例如："把背景改成蓝色" → 不要扩展为"深蓝色海洋背景，波光粼粼..."

---

### 1.2 提示词优化规则 (仅用于新生成任务)

#### 通用原则

**必须包含**:
- 主体对象、背景环境、构图取景
- 风格 (未指定默认真实照片风格)
- 颜色、纹理、材质、光照氛围
- 表情、姿势、道具 (如适用)
- 可见文字内容 (如需要)

**禁用词汇** ⚠️:
```
hyper-realistic, very detailed, vibrant, breathtaking, stunning, 
cinematic, epic, 8K, Unreal Engine, dramatic lighting, volumetric lighting
```

**语言规则**:
- 非英文 → 隐式翻译为英文
- 必须出现的文字内容 → 保留原语言

**字数限制**: 100词以内

---

### 1.3 视频生成补充 (运镜语言)

**视频 = 图像 + 运镜**

#### 运镜速查表

| 类型 | 运镜 | 英文 | 情绪效果 |
|------|------|------|---------|
| **基础** | 静止 | Static | 对话、静物 |
| | 平移 | Pan | 展示环境 |
| | 推拉 | Dolly In/Out | 强调/展现 |
| | 跟拍 | Tracking | 角色移动 |
| | 环绕 | Orbit | 产品展示 |
| | 升降 | Crane Up/Down | 宏大场景 |
| **特殊** | 推拉变焦 | Dolly Zoom | 眩晕、不安 |
| | 第一人称 | FPV Drone | 速度、刺激 |
| | 360环绕 | 360 Orbit | 优雅、展示 |
| | 手持 | Handheld | 真实、纪实 |

#### 情绪-技术映射

| 目标情绪 | 推荐运镜 |
|---------|---------|
| 恐惧/不安 | Dolly Zoom + Dutch Angle |
| 速度/刺激 | FPV Drone + Crash Zoom |
| 优雅/时尚 | 360 Orbit + Arc Shot |
| 英雄/史诗 | Bullet Time + Crane Up |
| 混乱/失控 | Snorricam + Handheld |
| 真实/纪实 | Handheld + Rack Focus |

#### 视频提示词结构

```
[场景描述] + [运镜技术] + [情绪氛围]
```

**示例**:
```
A premium smartwatch on a white pedestal, metallic silver finish, 
studio lighting. Camera: 360 Orbit, slow rotation. Atmosphere: 
clean, modern, luxurious.
```

---

### 1.4 Midjourney 特殊说明

#### 宽高比参数

Midjourney 需要在**提示词末尾**指定宽高比：

```
提示词内容 --ar 16:9
```

**常用参数**:
- `--ar 1:1` (正方形)
- `--ar 16:9` (横屏)
- `--ar 9:16` (竖屏)
- `--ar 4:3` / `--ar 3:4` (标准)
- `--ar 21:9` (超宽屏)

#### Niji 动漫模型 ⭐

**动漫风格任务必须启用 Niji 模式**:

```
提示词内容 --niji 7 --ar 16:9
```

- `--niji 7` - Midjourney 专用动漫模型（最新版本）
- `--niji 6` - 上一代动漫模型（备选）
- **适用**: 动漫风格、卡通化、漫画风格、日系插画、Chibi/Q版
- **效果**: 大幅提升动漫风格生成质量

#### Descriptive 提示词风格 🎯

**Midjourney 需要描述性（Descriptive）提示词，不要使用指令式（Instructive）**

**❌ 错误 (Instructive - 包含动词指令)**:
```
transform into anime style
turn into cute cartoon
convert to manga style
make it look like watercolor
```

**✅ 正确 (Descriptive - 只描述画面)**:
```
anime style, vibrant colors, kawaii aesthetic
cute cartoon character, big eyes, soft colors
manga art style, black and white, dynamic lines
watercolor painting, soft brush strokes, pastel tones
```

**Few-shot 示例**:

| 任务 | ❌ Instructive | ✅ Descriptive |
|------|---------------|----------------|
| 真人照片→动漫 | "transform this photo into anime style" | "anime style, Japanese manga art, vibrant colors, kawaii, dynamic pose --niji 7" |
| 风景→水彩 | "turn into watercolor painting" | "watercolor landscape, soft brush strokes, pastel colors, dreamy atmosphere" |
| 人物→卡通 | "convert to cute cartoon" | "cute cartoon character, big sparkling eyes, chibi style, colorful, playful" |

**image_to_image 极简流程**:
- **只需风格词** + 参考图 → Midjourney 自动理解图片内容
- 示例: `chibi style, kawaii, big head, large eyes --niji 7 --ar 1:1`
- 无需描述图片内容（人物、动作、场景），模型会自动提取

**完整示例**:
```
A modern living room with minimalist furniture, natural lighting, 
photographic style --ar 16:9

chibi style, super deformed, big head, large sparkling eyes, 
vibrant anime colors --niji 7 --ar 1:1
```

---

## 2. 宽高比选择 (Aspect Ratio Selection)

### 2.1 核心策略

```
用户需求
  ↓
1. 精确像素数 → 计算宽高比 → 选择最接近尺寸
2. 指定宽高比 → 直接使用 (如模型支持)
3. 都不支持 → 计算最接近比例
4. 模型不支持 → 推荐换模型
```

**关键**: 优先满足宽高比，其次是精确尺寸

---

### 2.2 模型支持

| 模型 | 宽高比 | 实现方式 |
|------|--------|---------|
| SeeDream 4.5 | 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 | API 参数 |
| Nano Banana | 1:1, 16:9, 9:16, 4:3, 3:4 | API 参数 |
| Midjourney | 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 等 | **提示词参数 `--ar`** ⚠️ |

**Midjourney 特殊性**:
- 不使用 API 参数 `aspect_ratio`
- 必须在提示词末尾添加 `--ar 16:9`
- 如果用户选择 Midjourney + 指定宽高比 → 自动在提示词末尾添加 `--ar`

---

### 2.3 决策示例

**场景 1**: 用户要求 1920×1080
- 计算比例: 16:9
- SeeDream 4.5 支持 16:9 → 选择 2560×1440 (2k, 16:9)
- 告知: "生成 2560×1440 (16:9)，最接近您的需求"

**场景 2**: 用户要求 16:9 横屏
- SeeDream 4.5 → `aspect_ratio="16:9"`
- Midjourney → 提示词末尾加 `--ar 16:9`

**场景 3**: 用户要求 7:3 (2.33)
- 计算最接近: 21:9 (2.33) 完全匹配
- 选择 21:9

**场景 4**: 用户要求 21:9，但用 Nano Banana (不支持)
- 方案 A: 推荐换 SeeDream 4.5 或 Midjourney
- 方案 B: 使用最接近的 16:9 (1.78)

---

### 2.4 常用比例速查

| 用途 | 比例 | 尺寸 |
|------|------|------|
| 社交头像 | 1:1 | 1024×1024 |
| 横屏视频 | 16:9 | 1920×1080 |
| 竖屏视频 | 9:16 | 1080×1920 |
| 电影超宽 | 21:9 | 2560×1097 |
| 照片标准 | 4:3, 3:2 | 2048×1536 |

---

## 3. Quick Reference

### 提示词优化决策

| 任务 | 处理 |
|------|------|
| 新生成 (text-to-image) | ✅ 优化提示词 (100词内) |
| 修改任务 (image-to-image) | ❌ 保持用户原提示词 |
| Midjourney | ✅ 提示词末尾加 `--ar 16:9` |

### 宽高比选择决策

| 场景 | 处理 |
|------|------|
| 指定像素 (1920×1080) | 计算比例 (16:9) → 选最接近尺寸 |
| 指定比例 (16:9) | 直接使用 (如支持) |
| 比例不支持 (7:3) | 计算最接近 (21:9) |
| 模型不支持 | 推荐换模型 |

### Midjourney 特别提醒

⚠️ Midjourney 宽高比必须在**提示词末尾**用 `--ar 16:9` 指定，不能用 API 参数！

---

**记住**: 修改任务不要动提示词 + 优先满足宽高比 🎯
