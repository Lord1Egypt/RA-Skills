# OpenClaw 官方文档查询 - 使用示例

## 示例 1：功能查询

### 用户输入
```
OpenClaw 支持哪些聊天平台？
```

### 期望输出
```
📋 查询结果

## 核心答案
OpenClaw 支持微信、钉钉、飞书、Telegram、Discord 等多个主流聊天平台。

## 详细说明
OpenClaw 采用渠道（Channel）架构，每个聊天平台对应一个独立的渠道适配器。通过配置不同的渠道，可以实现一个 AI Agent 同时服务多个平台。

## 支持平台列表

| 平台 | 渠道名称 | 状态 |
|-----|---------|------|
| 微信 | wechat | ✅ 稳定支持 |
| 钉钉 | dingtalk | ✅ 稳定支持 |
| 飞书 | feishu | ✅ 稳定支持 |
| Telegram | telegram | ✅ 稳定支持 |
| Discord | discord | ✅ 稳定支持 |
| 企业微信 | wework | ✅ 稳定支持 |

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/channels/overview
- 章节位置：Channels → Supported Platforms
- 最后更新：2024-01-15

## ⚠️ 注意事项
- 不同平台配置方式略有差异
- 部分平台需要企业认证
- 建议查看各平台的具体配置文档
```

---

## 示例 2：配置指导

### 用户输入
```
如何配置 Gateway？
```

### 期望输出
```
📋 查询结果

## 核心答案
Gateway 配置通过 `config.yaml` 文件完成，位于 `~/.openclaw/gateway/` 目录。

## 详细说明
Gateway 是 OpenClaw 的核心组件，负责消息路由、技能调度和渠道管理。配置文件采用 YAML 格式，支持热重载。

## 操作步骤

### 1. 定位配置文件
```bash
# Linux/Mac
cd ~/.openclaw/gateway
vi config.yaml

# Windows
cd %USERPROFILE%\.openclaw\gateway
notepad config.yaml
```

### 2. 基础配置结构
```yaml
# 服务器配置
server:
  host: 0.0.0.0
  port: 18789

# 渠道配置
channels:
  - name: wechat
    enabled: true
    config:
      corp_id: "your_corp_id"
      agent_id: "your_agent_id"
      secret: "your_secret"

# 技能配置
skills:
  - name: example-skill
    enabled: true
    path: ./skills/example-skill
```

### 3. 验证配置
```bash
# 检查配置语法
openclaw config check

# 重启服务
openclaw restart
```

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/configuration/gateway
- 章节位置：Configuration → Gateway Setup
- 最后更新：2024-01-20

## ⚠️ 注意事项
- YAML 文件对缩进敏感，使用 2 空格缩进
- 修改配置后需要重启服务
- 端口 18789 需未被占用
- 敏感信息建议使用环境变量
```

---

## 示例 3：技能开发

### 用户输入
```
如何开发一个 OpenClaw 技能？
```

### 期望输出
```
📋 查询结果

## 核心答案
OpenClaw 技能是一个包含 `SKILL.md` 和 `CLAUDE.md` 的文件夹，放置在 `~/.openclaw/skills/` 目录下即可生效。

## 详细说明
技能是 OpenClaw 的核心扩展机制。通过技能，可以为 AI 添加专业知识、工作流程和行为规范。技能采用声明式设计，无需编写代码。

## 操作步骤

### 1. 创建技能目录
```bash
mkdir -p ~/.openclaw/skills/my-skill
cd ~/.openclaw/skills/my-skill
```

### 2. 创建 SKILL.md（技能定义）
```yaml
---
name: my-skill
description: 我的第一个技能
metadata:
  version: 1.0.0
  author: Your Name
  category: productivity
---

# 我的技能

技能的详细描述...
```

### 3. 创建 CLAUDE.md（核心指令）
```markdown
# 核心指令

你现在正在使用我的技能...

## 执行规则
1. 规则一
2. 规则二
```

### 4. 重启 Gateway
```bash
openclaw restart
```

## 技能文件结构
```
my-skill/
├── SKILL.md      # 必需：技能定义
├── CLAUDE.md      # 必需：核心指令
├── README.md     # 可选：说明文档
└── EXAMPLES.md   # 可选：使用示例
```

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/skills/development
- 章节位置：Skills → Development Guide
- 最后更新：2024-01-18

## ⚠️ 注意事项
- SKILL.md 和 CLAUDE.md 是必需文件
- 文件名大小写敏感
- 修改技能后需要重启 Gateway
- 建议添加 README 和 EXAMPLES 提升可读性
```

---

## 示例 4：问题排查

### 用户输入
```
我的技能不生效，怎么排查？
```

### 期望输出
```
📋 查询结果

## 核心答案
技能不生效通常由文件结构错误、语法问题或配置遗漏导致，可通过检查清单逐步排查。

## 详细说明
OpenClaw 在加载技能时会进行验证，但部分问题可能不会立即报错。建议按照以下步骤系统排查。

## 排查步骤

### 1. 检查文件结构
```bash
# 确认技能目录存在
ls ~/.openclaw/skills/my-skill/

# 必需文件
ls ~/.openclaw/skills/my-skill/SKILL.md
ls ~/.openclaw/skills/my-skill/CLAUDE.md
```

### 2. 验证 SKILL.md 格式
```yaml
# 检查 YAML frontmatter
---
name: my-skill          # 必需：技能名称
description: 描述       # 必需：技能描述
metadata:              # 必需：元数据
  version: 1.0.0
  author: Your Name
  category: productivity
---
```

### 3. 检查 Gateway 日志
```bash
# 查看启动日志
openclaw logs

# 查看错误信息
openclaw logs | grep -i error
```

### 4. 验证技能加载
```bash
# 列出已加载技能
openclaw skills list

# 检查特定技能状态
openclaw skills show my-skill
```

### 5. 测试技能触发
- 确认触发条件是否满足
- 检查 CLAUDE.md 中的指令是否正确
- 尝试简化技能内容逐步验证

## 常见问题

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| 技能未加载 | 文件名错误 | 确认 SKILL.md 和 CLAUDE.md |
| YAML 解析错误 | 格式问题 | 检查缩进和语法 |
| 技能不触发 | 条件不满足 | 检查 CLAUDE.md 触发条件 |
| 内容不生效 | 指令冲突 | 检查是否有其他技能覆盖 |

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/troubleshooting/skills
- 章节位置：Troubleshooting → Skill Issues
- 最后更新：2024-01-22

## ⚠️ 注意事项
- 修改技能后必须重启 Gateway
- YAML 文件对缩进敏感
- 查看日志是最高效的排查方式
- 复杂问题建议在 GitHub Issues 反馈
```

---

## 示例 5：API 使用

### 用户输入
```
OpenClaw 有哪些 API 接口？
```

### 期望输出
```
📋 查询结果

## 核心答案
OpenClaw 提供完整的 RESTful API，包括消息发送、技能管理、会话管理等接口。

## 详细说明
API 默认监听在 `http://localhost:18789/api`，支持 JSON 格式的请求和响应。

## 核心 API 列表

### 消息相关

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/message/send` | POST | 发送消息 |
| `/api/message/history` | GET | 获取历史消息 |

### 技能管理

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/skills` | GET | 列出所有技能 |
| `/api/skills/{name}` | GET | 获取技能详情 |
| `/api/skills/{name}/enable` | POST | 启用技能 |
| `/api/skills/{name}/disable` | POST | 禁用技能 |

### 会话管理

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/sessions` | GET | 列出所有会话 |
| `/api/sessions/{id}` | GET | 获取会话详情 |
| `/api/sessions/{id}/clear` | POST | 清除会话上下文 |

## 使用示例

### 发送消息
```bash
curl -X POST http://localhost:18789/api/message/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "wechat",
    "user": "user123",
    "message": "Hello from API"
  }'
```

### 列出技能
```bash
curl http://localhost:18789/api/skills
```

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/api/overview
- 章节位置：API Reference → Overview
- 最后更新：2024-01-25

## ⚠️ 注意事项
- API 默认无认证，生产环境建议配置认证
- 所有接口返回 JSON 格式
- 错误响应包含详细的错误信息
- 建议使用 HTTPS 部署
```

---

## 示例 6：部署相关

### 用户输入
```
如何部署 OpenClaw 到生产环境？
```

### 期望输出
```
📋 查询结果

## 核心答案
OpenClaw 支持 Docker、二进制文件和源码编译三种部署方式，推荐使用 Docker 进行生产部署。

## 详细说明
生产部署需要考虑高可用、安全配置、日志管理和监控告警等方面。

## 部署步骤（Docker 方式）

### 1. 准备配置文件
```bash
mkdir -p /opt/openclaw
cd /opt/openclaw

# 创建配置目录
mkdir -p config skills logs
```

### 2. 创建 docker-compose.yml
```yaml
version: '3'
services:
  openclaw-gateway:
    image: openclaw/gateway:latest
    container_name: openclaw-gateway
    restart: always
    ports:
      - "18789:18789"
    volumes:
      - ./config:/app/config
      - ./skills:/app/skills
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
      - LOG_LEVEL=info
```

### 3. 启动服务
```bash
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 4. 配置反向代理（Nginx）
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:18789;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 生产检查清单

- [ ] 配置 HTTPS 证书
- [ ] 设置日志轮转
- [ ] 配置监控告警
- [ ] 设置数据备份
- [ ] 配置防火墙规则
- [ ] 启用 API 认证

## 📖 来源引用
- 文档链接：https://docs.openclaw.ai/deployment/production
- 章节位置：Deployment → Production Guide
- 最后更新：2024-01-28

## ⚠️ 注意事项
- 生产环境必须配置 HTTPS
- 定期备份配置和数据
- 建议配置日志收集系统
- 关注官方安全更新公告
```

---

## 示例 7：文档未找到的情况

### 用户输入
```
OpenClaw 支持语音通话吗？
```

### 期望输出
```
📋 查询结果

## 查询状态
我在官方文档中没有找到关于"语音通话"功能的直接说明。

## 可能原因
1. 该功能尚未支持
2. 该功能在开发计划中
3. 该功能在文档的其他章节描述

## 建议操作

### 1. 查看官方资源
- GitHub Issues: https://github.com/openclaw/issues
- 官方社区: [社区链接]
- Release Notes: https://docs.openclaw.ai/changelog

### 2. 提交问题
如果这是您需要的功能，可以：
- 在 GitHub 提交 Feature Request
- 在社区讨论区发帖询问
- 联系官方技术支持

### 3. 替代方案
如果需要语音能力，可以考虑：
- 集成第三方语音服务
- 使用支持语音的平台渠道（如微信语音消息）

## 📖 已查询文档
- 主页：https://docs.openclaw.ai/
- 功能列表：https://docs.openclaw.ai/features
- 渠道说明：https://docs.openclaw.ai/channels

---

💡 提示：OpenClaw 持续更新中，建议关注官方动态获取最新功能信息。
```
