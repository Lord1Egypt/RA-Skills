# Kie AI Nano Banana Pro 生图 Skill

> 版本：v1.0 | 作者：Spark | 创建时间：2026-04-03

---

## 🎯 Skill 定位

**Kie AI Nano Banana Pro 官方生图助手** —— 专精于 Google Nano Banana Pro 模型的图像生成系统

**核心使命：** 通过 Kie AI API 调用 Google Nano Banana Pro 模型，生成高质量、多比例、多分辨率的专业图像

**官方文档：** https://docs.kie.ai/market/google/pro-image-to-image

---

## ⚡ 触发规则

### 主触发词
- `Kie AI` / `kie` / `Nano Banana` / `nano banana`
- `Google 生图` / `Google 图像生成`
- `Pro Image` / `pro image to image`
- `生图 API` / `图像生成 API`

### 场景触发
- "帮我生成一个图片..."
- "用 Kie AI 生成..."
- "Nano Banana 生图..."
- "Google 图像模型..."

### 不触发场景
- 其他平台生图（Midjourney/SD/NanobananaPro 独立 Skill）
- 非图像生成需求

---

## 🏗️ 核心工作流

### Step 1: 需求接收与解析

**必填信息提取：**
1. **提示词（prompt）** - 图像内容描述（最长 10000 字符）
2. **画幅比例（aspect_ratio）** - 1:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 21:9 / auto
3. **分辨率（resolution）** - 1K / 2K / 4K
4. **输出格式（output_format）** - png / jpg

**选填信息：**
- **参考图（image_input）** - 最多 8 张图片 URL
- **回调地址（callBackUrl）** - 生产环境推荐

### Step 2: API 调用准备

**API 端点：**
```
POST https://api.kie.ai/api/v1/jobs/createTask
```

**请求头：**
```json
{
  "Authorization": "Bearer <API_KEY>",
  "Content-Type": "application/json"
}
```

**请求体：**
```json
{
  "model": "nano-banana-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "图像描述...",
    "image_input": [],
    "aspect_ratio": "1:1",
    "resolution": "1K",
    "output_format": "png"
  }
}
```

### Step 3: 任务提交与状态查询

**提交响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskId": "task_nano-banana-pro_1765178625768"
  }
}
```

**状态查询：**
- 使用 `taskId` 查询任务状态
- 或通过 `callBackUrl` 接收完成通知

### Step 4: 结果交付

**成功响应：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "status": "completed",
    "imageUrl": "https://...",
    "thumbnailUrl": "https://..."
  }
}
```

---

## 🎨 输出标准

### 标准输出结构

```markdown
## 🎨 图像生成任务已提交

**任务 ID：** `task_nano-banana-pro_xxx`

**生成参数：**
- 提示词：[用户描述]
- 画幅比例：[比例]
- 分辨率：[分辨率]
- 输出格式：[格式]

**预计耗时：** 30-60 秒

**查询方式：**
1. 自动回调（如配置 callBackUrl）
2. 手动查询：`查询任务 task_xxx`

---

## 📋 提示词优化建议

[根据用户需求提供的优化建议]
```

---

## 🔧 API 集成规范

### 认证方式

**Bearer Token 认证：**
```
Authorization: Bearer YOUR_API_KEY
```

**获取 API Key：**
1. 访问 https://kie.ai/api-key
2. 创建新的 API Key
3. 妥善保管，切勿泄露

### 错误处理

**常见错误码：**

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 200 | 成功 | - |
| 401 | 未授权 | 检查 API Key 是否正确 |
| 402 | 余额不足 | 充值账户 |
| 422 | 参数验证失败 | 检查参数格式 |
| 429 | 请求频率超限 | 等待后重试 |
| 500 | 服务器错误 | 联系技术支持 |
| 501 | 生成失败 | 检查提示词或重试 |

### 回调配置

**回调 Payload：**
```json
{
  "taskId": "task_xxx",
  "status": "completed",
  "result": {
    "imageUrl": "https://...",
    "thumbnailUrl": "https://..."
  }
}
```

**回调验证：**
- 参考 [Webhook Verification Guide](/common-api/webhook-verification)
- 验证签名确保请求来源

---

## 📝 使用示例

### 示例 1：基础图像生成

**用户输入：**
> 帮我生成一个香蕉英雄的漫画海报，1:1 比例

**输出：**
```markdown
## 🎨 图像生成任务已提交

**任务 ID：** `task_nano-banana-pro_1765178625768`

**生成参数：**
- 提示词：Comic poster: cool banana hero in shades leaps from sci-fi pad
- 画幅比例：1:1
- 分辨率：1K
- 输出格式：png

**预计耗时：** 30-60 秒

**查询方式：**
- 手动查询：`查询任务 task_nano-banana-pro_1765178625768`
```

### 示例 2：多图参考生成

**用户输入：**
> 用这 3 张参考图生成新图像，16:9 宽屏，4K 分辨率

**输出：**
```json
{
  "model": "nano-banana-pro",
  "input": {
    "prompt": "基于参考图生成...",
    "image_input": [
      "https://...",
      "https://...",
      "https://..."
    ],
    "aspect_ratio": "16:9",
    "resolution": "4K",
    "output_format": "png"
  }
}
```

### 示例 3：生产环境回调

**用户输入：**
> 批量生成产品图，回调到 https://api.myshop.com/callback

**输出：**
```json
{
  "model": "nano-banana-pro",
  "callBackUrl": "https://api.myshop.com/api/callback",
  "input": {
    "prompt": "Product photography...",
    "aspect_ratio": "1:1",
    "resolution": "2K",
    "output_format": "png"
  }
}
```

---

## 🎯 提示词优化指南

### 基础结构

```
[主体描述] + [场景环境] + [风格美学] + [技术参数]
```

### 示例模板

**漫画海报：**
```
Comic poster: [角色] in [场景], [动作]. 
Six panels: 1) [场景 1], 2) [场景 2], 3) [场景 3]...
Footer shows [元素]. Tagline: [标语].
```

**产品摄影：**
```
Professional product photography: [产品], 
[背景], [光影], [构图].
Commercial quality, 8K, ultra detailed.
```

**风景摄影：**
```
Landscape photography: [场景], [时间], [天气].
[构图法则], [光影效果], [色彩方案].
8K, ultra HD, professional.
```

---

## 📊 参数详解

### 画幅比例 (aspect_ratio)

| 比例 | 适用场景 | 推荐平台 |
|------|----------|----------|
| `1:1` | 头像、产品主图 | 全平台 |
| `2:3` / `3:2` | 照片、印刷品 | 摄影 |
| `3:4` / `4:3` | 小红书、iPad | 小红书 |
| `4:5` / `5:4` | 竖版海报 | 社交媒体 |
| `9:16` | 抖音、视频号 | 抖音/快手 |
| `16:9` | B 站、YouTube | 视频平台 |
| `21:9` | 电影宽屏 | 院线 |
| `auto` | 自动适配 | 通用 |

### 分辨率 (resolution)

| 分辨率 | 像素 | 适用场景 |
|--------|------|----------|
| `1K` | ~1024px | 快速测试、社交媒体 |
| `2K` | ~2048px | 正式输出、商业使用 |
| `4K` | ~4096px | 高质量印刷、大幅海报 |

### 输出格式 (output_format)

| 格式 | 特点 | 适用场景 |
|------|------|----------|
| `png` | 无损压缩、支持透明 | 产品图、图标、需要后期 |
| `jpg` | 有损压缩、文件小 | 照片、网页展示 |

---

## 🔗 相关链接

- **官方文档：** https://docs.kie.ai/market/google/pro-image-to-image
- **API Key 管理：** https://kie.ai/api-key
- **任务状态查询：** https://docs.kie.ai/common-api/get-task-detail
- **Webhook 验证：** https://docs.kie.ai/common-api/webhook-verification

---

## 🚀 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-03 | 初始版本，Kie AI API 集成 |

---

**Skill 开发完成 · 可直接发布到 ClawHub**
