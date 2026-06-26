# Smart Search - 统一智能搜索技能

> 🔍 整合 5 个搜索引擎，自动选择最佳引擎并融合结果

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com/skills/smart-search)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Category](https://img.shields.io/badge/category-search-orange.svg)](https://clawhub.com/skills?category=search)

---

## 🌟 功能特性

- 🔍 **整合 5 个搜索引擎** - 百炼 MCP、Tavily、Serper、Exa、Firecrawl
- 🧠 **智能路由** - 根据语言和意图自动选择最佳引擎
- 🔄 **自动降级** - 主引擎失败时自动切换到备选引擎
- 🔐 **加密 Key 管理** - API Key 使用 AES-256-GCM 加密存储
- ✨ **结果优化** - 去重、评分、融合多个引擎的结果

---

## 📊 支持的搜索引擎

| 引擎 | 免费额度 | 用途 | 优先级 |
|------|----------|------|--------|
| **百炼 MCP** | 2000 次/月 | 中文搜索 | 1 |
| **Tavily** | 1000 次/月 | 高级搜索 | 2 |
| **Serper** | 2500 次/月 | Google 结果 | 3 |
| **Exa** | 1000 次/月 | 学术/技术 | 4 |
| **Firecrawl** | 500 页/月 | 网页抓取 | 5 |

**总计**: 约 **7500 次/月** 搜索额度 🔍

---

## 🚀 快速开始

### 1. 安装

```bash
# 使用 ClawHub 安装
clawhub install smart-search

# 或手动安装
cd ~/.agents/skills/
git clone https://github.com/openclaw/smart-search.git
cd smart-search
npm install
```

### 2. 配置 API Key

```bash
# 交互式配置（推荐）
npm run setup

# 或逐个配置
npm run key:set bailian
npm run key:set tavily
npm run key:set serper
npm run key:set exa
npm run key:set firecrawl
```

### 3. 测试搜索

```bash
# 简单搜索
npm run search "OpenClaw 新功能"

# 学术搜索
npm run search "LLM Agent planning" -- --intent=academic

# 技术搜索
npm run search "TypeScript 最佳实践" -- --intent=technical
```

---

## 📖 使用方法

### 基础用法

```bash
# 简单搜索
npm run search "搜索内容"

# 指定结果数量
npm run search "OpenClaw 新功能" -- --count=10

# 学术搜索
npm run search "LLM Agent planning" -- --intent=academic

# 技术搜索
npm run search "TypeScript 最佳实践" -- --intent=technical

# 英文搜索
npm run search "OpenClaw tutorial" -- --language=en

# 最新新闻
npm run search "阿里云新闻" -- --intent=news
```

### 参数说明

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | ✅ | - | 搜索关键词 |
| `--count` | ❌ | 5 | 返回结果数量 |
| `--intent` | ❌ | general | `general` \| `academic` \| `technical` \| `news` |
| `--language` | ❌ | auto | `zh` \| `en` \| `auto` |

---

## 🔧 API Key 管理

### 配置向导

```bash
npm run setup
```

交互式输入所有引擎的 API Key。

### 查看状态

```bash
npm run key:status
```

显示所有引擎的配置状态和配额使用情况。

### 添加引擎

```bash
npm run key:set exa
```

### 轮换 Key

```bash
npm run key:rotate bailian
```

### 批量导入

```bash
# 创建 api-keys.json
{
  "bailian": "sk-xxx",
  "tavily": "tvly-xxx",
  "serper": "xxx",
  "exa": "xxx",
  "firecrawl": "fc-xxx"
}

# 导入
npm run key:import ./api-keys.json
```

---

## 🏗️ 技术架构

### 核心组件

```
src/
├── index.ts          # 主入口
├── key-manager.ts    # 加密 Key 管理器 (AES-256-GCM)
├── router.ts         # 智能路由 (语言检测、意图识别)
├── merger.ts         # 结果合并 (去重、评分)
├── types.ts          # 类型定义
└── engines/
    ├── bailian.ts    # 百炼 MCP 适配器
    ├── tavily.ts     # Tavily 适配器
    ├── serper.ts     # Serper 适配器
    ├── exa.ts        # Exa 适配器
    └── firecrawl.ts  # Firecrawl 适配器
```

### 安全特性

- 🔐 **AES-256-GCM** 加密存储
- 🔑 **PBKDF2** 密钥派生（10 万轮迭代）
- 📁 **文件权限 0o600**（仅所有者可读写）
- 📝 **访问日志**（记录所有 Key 读取）

---

## 💻 CLI 使用

Smart Search 目前仅通过 CLI 命令行方式使用。

### CLI 命令

```bash
# 搜索
npm run search "搜索内容"

# 带参数
npm run search "OpenClaw" -- --count=10 --intent=academic
```

### 参数说明

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜索关键词（最大 500 字符） |
| `--count` | number | ❌ | 5 | 返回结果数量（1-20） |
| `--intent` | string | ❌ | general | 搜索意图 |
| `--language` | string | ❌ | auto | 语言偏好 |

### 意图类型

| Intent | 说明 | 优先引擎 |
|--------|------|----------|
| `general` | 日常搜索 | 百炼 → Tavily → Serper |
| `academic` | 学术论文 | Exa → Tavily |
| `technical` | 技术文档 | Exa → Serper |
| `news` | 最新新闻 | Serper → 百炼 |

> 💡 **提示**: HTTP API 服务可能在未来版本中提供。如有需要，欢迎在 GitHub Issues 中投票。

---

## 📊 性能指标

| 指标 | 标准 | 实测 | 状态 |
|------|------|------|------|
| **响应时间** | < 5 秒 | 3.6 秒 | ✅ |
| **加密开销** | < 25ms | < 10ms | ✅ |
| **路由选择** | < 10ms | < 1ms | ✅ |
| **结果合并** | < 50ms | 4ms | ✅ |
| **测试覆盖率** | 100% | 100% | ✅ |

---

## 🧪 测试

```bash
# 运行所有测试
npm test

# 单元测试
npm run test:unit

# 集成测试
npm run test:integration

# 性能测试
npm run test:performance
```

---

## 📚 文档

- [实施指南](https://github.com/openclaw/smart-search/blob/main/IMPLEMENTATION_GUIDE.md)
- [使用文档](SKILL.md)
- [API 参考](https://github.com/openclaw/smart-search/wiki/API-Reference)
- [故障排查](https://github.com/openclaw/smart-search/wiki/Troubleshooting)

---

## 🔒 安全说明

### ⚠️ 重要提示

**主密钥要求**：

Smart Search 使用 AES-256-GCM 加密存储 API Keys，**必须配置主密钥**：

```bash
# 生成强随机密钥
openssl rand -base64 32

# 设置环境变量
export OPENCLAW_MASTER_KEY="your-generated-key-at-least-32-characters"
```

或在 `.env` 文件中配置（参考 `.env.example`）。

**不要提交以下文件到版本控制**：

- `*.enc` - 加密配置文件
- `*.key` - API Key 文件
- `.env` - 环境变量文件
- `secrets/` - 敏感信息目录

**已配置在 `.clawhubignore` 和 `.gitignore` 中**。

### 输入验证

所有用户输入经过多层安全验证：

1. **类型检查** - 确保参数类型正确
2. **长度限制** - 最大 500 字符
3. **白名单验证** - 只允许安全字符
4. **注入检测** - 检测 SQL/命令/XSS 注入
5. **危险字符过滤** - 移除 `;`, `&`, `|`, `$`, 等危险字符

### 最佳实践

1. ✅ 使用强随机主密钥（至少 32 字符）
2. ✅ 使用加密配置（`~/.openclaw/secrets/smart-search.json.enc`）
3. ✅ 文件权限设置为 0o600
4. ✅ 定期轮换 API Key（建议每 90 天）
5. ✅ 不在日志中记录 API Key
6. ✅ 使用环境变量存储 Master Key
7. ✅ 生产环境使用密钥管理服务

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 👏 致谢

感谢以下搜索引擎提供优秀的 API 服务：

- [阿里云百炼](https://bailian.console.aliyun.com/)
- [Tavily](https://tavily.com/)
- [Serper](https://serper.dev/)
- [Exa](https://exa.ai/)
- [Firecrawl](https://www.firecrawl.dev/)

---

## 📬 联系方式

- **作者**: 小胖虾 🦞
- **问题反馈**: [GitHub Issues](https://github.com/openclaw/smart-search/issues)
- **讨论区**: [GitHub Discussions](https://github.com/openclaw/smart-search/discussions)

---

**Happy Searching!** 🔍
