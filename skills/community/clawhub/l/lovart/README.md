# Lovart AI Design Skill

与 Lovart.ai API 集成的 AI 设计生成 Skill，支持图像生成、图像编辑和视频创建。

## 快速开始

### 1. 安装和配置

首先，获取 Lovart API Key：

1. 访问 [Lovart.ai](https://www.lovart.ai/) 注册账户
2. 在账户设置中生成 API Key
3. 设置环境变量：

```bash
export LOVART_API_KEY='your_api_key_here'
```

### 2. 使用示例

生成产品图片：

```bash
curl -X POST https://api.lovart.ai/v1/design/generate \
  -H "Authorization: Bearer $LOVART_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional product photography of modern running shoes, white background, studio lighting",
    "width": 1920,
    "height": 1080,
    "model": "flux"
  }'
```

## 功能特性

- 🎨 **AI 图像生成**: 从文本描述生成高质量视觉内容
- 🖼️ **图像增强**: 使用 AI 进行图像放大和优化
- 📹 **视频生成**: 从图像或文本提示创建短视频
- 📐 **模板库**: 访问平台提供的设计模板库
- 🤖 **多模型支持**: 支持 Flux、Stable Diffusion 等多种 AI 模型

## 触发词

当用户提到以下内容时，此 Skill 会被触发：

- "使用 Lovart 生成设计"
- "用 Lovart AI 创建图片"
- "Lovart 设计"
- "AI 设计生成"
- "生成产品图片"
- "创建营销素材"
- "AI 视频生成"

## 文件结构

```
skill-lovart/
├── skill.md          # Skill 定义和配置
├── prompt.md         # 执行提示和工作流程
├── config.json       # 技术配置
├── examples.sh       # 使用示例脚本
└── README.md         # 本文件
```

## API 端点

### 生成设计
```
POST /v1/design/generate
```

基于文本提示和参数生成 AI 驱动的设计。

### 获取设计状态
```
GET /v1/design/{id}
```

检查设计生成请求的状态。

## 定价

- **免费版**: 有限配额
- **Starter**: $9/月（1200 积分）
- **Basic**: $29/月
- **Pro**: $49/月
- **Ultimate**: $99/月

所有付费计划包含商业使用权限。

## 支持与资源

- 📚 [API 文档](https://lovart.info/lovart-api)
- 👨‍💻 [开发者指南](https://lovart.info/lovart-ai-code)
- 📧 support@lovart.ai

## 注意事项

⚠️ **安全提醒**:
- 永远不要在客户端代码中暴露 API Key
- 始终通过后端服务器代理 API 请求
- 定期轮换 API Key

📋 **使用限制**:
- 遵守 Lovart 服务条款
- 尊重知识产权和版权
- 不得生成非法或有害内容

## 许可证

MIT License

---

作者: Claude Code
版本: 1.0.0
