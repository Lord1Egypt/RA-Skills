---
name: lovart
description: 与 Lovart.ai API 集成，生成 AI 设计、图片和视频。支持图像生成、图像编辑、视频创建和模板工作流。
author: Claude Code
version: 1.0.0
---

# Lovart AI Design Skill

该 Skill 与 Lovart.ai API 集成，提供强大的 AI 设计能力，包括图像生成、图像编辑、视频创建等功能。

## 功能特性

- **AI 图像生成**：从文本描述生成高质量视觉内容
- **图像增强**：使用 AI 进行图像放大和优化
- **视频生成**：从图像或文本提示创建短视频
- **模板库**：访问平台提供的设计模板库
- **多模型支持**：支持 Flux、Stable Diffusion 等多种 AI 模型

## 触发词

当用户提到以下内容时，应触发此 Skill：
- "使用 Lovart 生成设计"
- "用 Lovart AI 创建图片"
- "Lovart 设计"
- "AI 设计生成"
- "生成产品图片"
- "创建营销素材"
- "AI 视频生成"

## API 配置

### 获取 API Key

1. 访问 [Lovart.ai](https://www.lovart.ai/)
2. 创建账户并登录
3. 在账户设置中生成 API Key
4. 将 API Key 保存到环境变量：`LOVART_API_KEY`

### 认证方式

所有 API 请求需要在 Authorization header 中包含 API Key：

```
Authorization: Bearer YOUR_API_KEY
```

## API 端点

### 1. 生成设计

**端点**: `POST /v1/design/generate`

**描述**: 基于文本提示和参数生成 AI 驱动的设计

**请求参数**:
- `prompt` (string): 设计描述文本
- `model` (string, 可选): 使用的 AI 模型 (如 "flux", "stable-diffusion")
- `width` (integer, 可选): 图像宽度
- `height` (integer, 可选): 图像高度
- `style` (string, 可选): 设计风格
- `template_id` (string, 可选): 使用的模板 ID

**响应**:
- `id` (string): 设计任务 ID
- `status` (string): 任务状态 (pending/processing/completed)
- `result_url` (string): 完成后的图像下载链接

### 2. 获取设计状态

**端点**: `GET /v1/design/{id}`

**描述**: 检查设计生成请求的状态

**响应**:
- `id` (string): 设计任务 ID
- `status` (string): 当前状态
- `progress` (integer): 处理进度 (0-100)
- `result_url` (string): 结果 URL（如果完成）

## 使用示例

### 示例 1: 生成产品图片

```bash
curl -X POST https://api.lovart.ai/v1/design/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A modern running shoe on a white background, professional product photography",
    "width": 1920,
    "height": 1080,
    "model": "flux"
  }'
```

### 示例 2: 创建营销海报

```bash
curl -X POST https://api.lovart.ai/v1/design/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Summer sale promotional poster with vibrant colors and modern typography",
    "style": "marketing",
    "template_id": "template_123"
  }'
```

### 示例 3: 检查生成状态

```bash
curl -X GET https://api.lovart.ai/v1/design/{id} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 最佳实践

### 提示词编写
- **具体明确**: 描述要详细，包括主体、风格、构图、光线等
- **风格参考**: 提及具体的设计风格或艺术家
- **技术规格**: 指定尺寸、格式等技术要求

**好的提示词示例**:
```
"A premium coffee product shot, top-down view, natural lighting,
wooden surface background, minimalist composition,
4K resolution, professional commercial photography"
```

### 错误处理
- 检查 API Key 是否有效
- 验证请求参数格式
- 处理网络超时和重试逻辑
- 监控配额使用情况

### 性能优化
- 使用异步任务处理
- 实现结果缓存
- 批量请求合并处理

## 定价信息

- **免费版**: 有限配额，探索平台功能
- **Starter**: $9/月，1200 快速积分
- **Basic**: $29/月，更多积分和标准处理
- **Pro**: $49/月，优先处理
- **Ultimate**: $99/月，最高优先级

所有付费计划包含完整的商业使用权限。

## 支持与资源

- **官方文档**: [Lovart API 文档](https://lovart.info/lovart-api)
- **开发者指南**: [Lovart for Developers](https://lovart.info/lovart-ai-code)
- **支持邮箱**: support@lovart.ai
- **社区**: Discord 社区

## 常见问题

**Q: 生成的图片可以商用吗？**
A: 是的，所有付费计划都包含完整的商业使用权限。

**Q: 支持哪些文件格式？**
A: 支持 PNG、JPG 等常见图像格式，具体取决于生成参数。

**Q: 可以批量生成吗？**
A: 是的，可以通过多个 API 调用实现批量生成。

**Q: 如何处理长时间运行的任务？**
A: 使用异步任务模式，通过 `/v1/design/{id}` 端点轮询状态。

## 注意事项

⚠️ **安全提醒**:
- 永远不要在客户端代码中暴露 API Key
- 始终通过后端服务器代理 API 请求
- 定期轮换 API Key
- 监控 API 使用情况以防止滥用

📋 **使用限制**:
- 遵守 Lovart 服务条款
- 尊重知识产权和版权
- 不得生成非法或有害内容
