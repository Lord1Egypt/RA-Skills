# Knowfun Skills - 多平台AI集成

[English](README.md) | 简体中文

多平台AI编程助手集成工具，用于Knowfun.io API。支持Claude Code、Cursor、Cline和OpenClaw，生成教育内容、海报、游戏和视频。

[![许可证: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![平台](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20Cursor%20%7C%20Cline%20%7C%20OpenClaw-orange.svg)](PLATFORM_COMPARISON.md)
[![npm](https://img.shields.io/badge/npm-knowfun--skills-red.svg)](https://www.npmjs.com/package/knowfun-skills)
[![ClawHub](https://img.shields.io/badge/ClawHub-knowfun--skills-blue.svg)](https://clawhub.ai/duguyixiaono1/knowfun-skills)
[![安全性: 已验证](https://img.shields.io/badge/Security-Verified-success.svg)](SECURITY.md)
[![代码安全](https://img.shields.io/badge/Code%20Safety-Transparent-brightgreen.svg)](CLAWHUB_VERIFICATION.md)

## 什么是 Knowfun.io？

Knowfun.io 是一个 AI 驱动的平台，可将文本和文档转换为引人入胜的教育内容：
- 📚 **课程** - 带旁白的互动演示文稿
- 🎨 **海报** - 视觉信息图和营销素材
- 🎮 **游戏** - 互动学习体验
- 🎬 **视频** - 教育视频和纪录片

## 安全性与合规

这是 Knowfun.io API 的**官方、已验证集成**：

- ✅ **完全开源** - MIT 许可证，所有代码透明可审计
- ✅ **无任意代码执行** - 脚本路径硬编码，非用户可控
- ✅ **仅调用官方 API** - 只访问 https://api.knowfun.io 端点
- ✅ **行业标准安全** - API 密钥通过环境变量管理
- ✅ **无敏感数据泄露** - 凭证从不记录或暴露

**安全扫描器注意事项**：自动化工具可能会标记 bash 脚本的使用。这是误报 - 详见 [SECURITY.md](SECURITY.md) 的详细安全分析和 [CLAWHUB_VERIFICATION.md](CLAWHUB_VERIFICATION.md) 的验证步骤。

## 功能特性

### 平台支持
- 🎯 **Claude Code** - 原生 `/knowfun` 技能命令
- 🎯 **Cursor** - CLI工具 + 规则集成
- 🎯 **Cline** - CLI工具 + JSON配置
- 🎯 **OpenClaw** - CLI工具 + 技能定义

### 核心能力
- ✅ 通过自然语言创建内容生成任务
- ✅ 监控任务状态和进度
- ✅ 获取生成的内容
- ✅ 管理积分和 API 使用情况
- ✅ 获取配置选项和架构
- ✅ 多语言支持（English + 简体中文）

## 快速开始

选择您的平台：

- **Claude Code**: 查看 [Claude Code 安装](INSTALLATION_CN.md#claude-code-安装)
- **Cursor**: 查看 [Cursor 安装](INSTALLATION_CN.md#cursor-安装)
- **Cline**: 查看 [Cline 安装](INSTALLATION_CN.md#cline-安装)
- **OpenClaw**: 查看 [OpenClaw 安装](integrations/openclaw/README_CN.md)

或遵循 [5分钟快速入门指南](QUICKSTART_CN.md)

## 配置

1. **获取 API Key**
   - 访问 https://www.knowfun.io/api-platform
   - 点击"创建API Key"
   - 复制密钥（以 `kf_` 开头）

2. **配置环境变量**
   ```bash
   # 临时设置（当前会话）
   export KNOWFUN_API_KEY="kf_your_api_key_here"

   # 永久设置（添加到shell配置）
   echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## 使用方法

### Claude Code

```bash
# 使用原生斜杠命令
/knowfun create course "Python 编程入门"
/knowfun create poster "气候变化事实"
/knowfun status <taskId>
/knowfun credits
```

### Cursor / Cline / OpenClaw

```bash
# 直接使用CLI工具
knowfun create course "Python 编程入门"
knowfun create poster "气候变化事实"
knowfun status <taskId>
knowfun credits

# 或询问AI助手
"使用knowfun创建一个关于Python的课程"
```

### 所有命令

- `create <type> <content>` - 生成内容（course/poster/game/film）
- `status <taskId>` - 检查任务状态
- `detail <taskId>` - 获取详细结果
- `list [limit]` - 列出最近的任务
- `credits` - 检查积分余额
- `schema` - 获取配置选项

### 示例

#### 示例 1：从文本创建课程

```bash
/knowfun create course "机器学习基础：ML 是 AI 的一个子集，使计算机能够从数据中学习而无需显式编程。"
```

#### 示例 2：从 URL 创建课程

```bash
/knowfun create course https://example.com/document.pdf
```

#### 示例 3：检查状态并获取结果

```bash
# 创建任务并记下任务 ID
/knowfun create course "量子计算简介"

# 等待几分钟，然后检查状态
/knowfun status c3199fb3-350b-4981-858d-09b949bfae88

# 完成后获取详细结果
/knowfun detail c3199fb3-350b-4981-858d-09b949bfae88
```

## 文档

- **[QUICKSTART_CN.md](QUICKSTART_CN.md)**: 5分钟快速入门教程
- **[README_CN.md](README_CN.md)**: 完整概述（本文件）
- **[api-reference_CN.md](api-reference_CN.md)**: 完整 API 文档
- **[examples_CN.md](examples_CN.md)**: 20+ 使用示例
- **[SKILL.md](SKILL.md)**: Claude Code 技能定义

英文版本：
- **[README.md](README.md)**: English overview
- **[QUICKSTART.md](QUICKSTART.md)**: English quickstart
- **[api-reference.md](api-reference.md)**: English API reference
- **[examples.md](examples.md)**: English examples

## 配置选项

### 课程生成
- 内容风格：详细、简洁、对话式
- 语言：中文、英文等
- 音色类型和 TTS 风格
- 自定义要求

### 海报生成
- 用途类型：信息图（默认）、商务报告、营销、文章插图
- 风格：手绘（默认）、照片写实、动漫、科幻、自定义
- 宽高比：1:1、16:9、9:16、4:3、3:4

### 游戏生成
- 游戏类型：故事、互动（默认）、探索、任务、角色扮演、模拟、拼图、街机、卡牌、文字、时间线、自定义
- 自定义提示词
- 图片上传

### 视频生成
- 视频风格：旁白（默认）、故事、纪录片、教程、概念图解、案例分析、动画、电影感、宣传片、自定义
- 宽高比：16:9（默认）、9:16、1:1
- 自定义视觉风格

## API 端点

- **Base URL**: `https://api.knowfun.io`
- **创建任务**: `POST /api/openapi/v1/tasks`
- **获取状态**: `GET /api/openapi/v1/tasks/:taskId`
- **获取详情**: `GET /api/openapi/v1/tasks/:taskId/detail`
- **任务列表**: `GET /api/openapi/v1/tasks`
- **积分余额**: `GET /api/openapi/v1/credits/balance`
- **积分定价**: `GET /api/openapi/v1/credits/pricing`
- **使用统计**: `GET /api/openapi/usage`
- **配置架构**: `GET /api/openapi/v1/schema`

## 积分系统

每种任务类型消耗积分：
- **课程**: 100 积分（默认）
- **海报**: 100 积分（默认）
- **游戏**: 100 积分（默认）
- **视频**: 100 积分（默认）

查看余额：`/knowfun credits` 或 `knowfun credits`

**获取更多积分**: 访问 https://www.knowfun.io/api-platform 管理您的账户

## 速率限制

- 默认：60 次/分钟
- 默认：1000 次/天
- 可按 API key 配置

## 错误处理

常见错误及解决方案：

| 错误码 | 状态 | 解决方案 |
|--------|------|----------|
| INVALID_API_KEY | 401 | 检查你的 API key |
| API_KEY_EXPIRED | 401 | 重新生成 API key |
| INSUFFICIENT_CREDITS | 402 | 充值积分 |
| RATE_LIMIT_EXCEEDED | 429 | 等待后重试 |
| TASK_TYPE_NOT_ALLOWED | 403 | 检查 API key 权限 |

## 高级用法

### 使用回调

对于长时间运行的任务，设置回调 URL：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "unique-id",
    "taskType": "course",
    "material": {"text": "内容在这里"},
    "callbackUrl": "https://your-server.com/callback"
  }'
```

### 批量处理

处理多个项目：

```bash
# 创建任务列表
for topic in "Python" "JavaScript" "CSS"; do
  /knowfun create course "学习 $topic 基础"
  sleep 2
done
```

### 使用 curl

对于高级配置，直接使用 curl：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "course-001",
    "taskType": "course",
    "material": {
      "text": "你的内容在这里",
      "type": "text"
    },
    "config": {
      "course": {
        "contentStyle": "detailed",
        "contentLanguage": "zh",
        "explainLanguage": "zh"
      }
    }
  }'
```

## 故障排除

### API Key 未找到

```bash
# 检查是否设置
echo $KNOWFUN_API_KEY

# 临时设置
export KNOWFUN_API_KEY="kf_your_key"

# 或永久设置
echo 'export KNOWFUN_API_KEY="kf_your_key"' >> ~/.zshrc
```

### 任务处理时间过长

- 课程生成：通常 2-5 分钟
- 海报生成：通常 1-3 分钟
- 游戏生成：通常 3-7 分钟
- 视频生成：通常 5-10 分钟

如果任务卡住超过 15 分钟，请联系支持。

### 积分问题

```bash
# 检查余额
/knowfun credits

# 检查定价
curl -s https://api.knowfun.io/api/openapi/v1/credits/pricing \
  -H "Authorization: Bearer $KNOWFUN_API_KEY"
```

## 支持

- **网站**: https://www.knowfun.io
- **API 平台**: https://www.knowfun.io/api-platform
- **文档**: 查看 [api-reference_CN.md](api-reference_CN.md)
- **示例**: 查看 [examples_CN.md](examples_CN.md)
- **Issues**: 在 [GitHub Issues](../../issues) 上报告 bug 和请求功能

## 贡献

我们欢迎贡献！在提交 pull request 之前，请阅读我们的[贡献指南](CONTRIBUTING.md)。

- 🐛 [报告 bug](../../issues/new?template=bug_report.md)
- 💡 [请求功能](../../issues/new?template=feature_request.md)
- 📝 [改进文档](CONTRIBUTING.md#documentation-contributions)
- 🔧 [提交代码](CONTRIBUTING.md#code-contributions)

请注意，本项目发布时附带[行为准则](CODE_OF_CONDUCT.md)。参与即表示您同意遵守其条款。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

版权所有 (c) 2026 Knowfun.io

## 版本

- **版本**: 1.0.13
- **最后更新**: 2026-03-09
- **兼容**: Claude Code、Cursor、Cline、OpenClaw

---

