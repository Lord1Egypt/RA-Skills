---
name: openclaw-deploy-tracker
description: "记录和查询 OpenClaw 生态的部署服务。当需要新增部署、查询现有服务、更新服务状态、检查依赖关系时使用。规范记录格式，提供查询和写入的工作流。无需凭证。"
metadata: {"openclaw":{"emoji":"📡","requires":{"anyBins":[]}}}
---

# openclaw-deploy-tracker

记录和查询 OpenClaw 生态中部署的所有服务。当需要新增部署、查询现有服务、更新状态、检查端口冲突或依赖关系时触发。

## 记录规范

所有服务记录在 `memory/services/` 目录下，以服务为单位组织文件：

```
memory/services/
├── registry.md        ← 所有服务的索引（快速概览）
└── {service-name}.md  ← 单个服务的详细记录
```

## 索引文件格式（registry.md）

```markdown
# 服务注册表

更新时间：2026-04-01

## 按类型分类

### 容器 / Docker
| 服务 | 端口 | 状态 | 用途 | 负责人 |
|------|------|------|------|--------|
| wewe-rss | :4000 | running | 微信公众号 RSS | 小爪子 |

### 本地服务
| 服务 | 端口 | 状态 | 用途 | 负责人 |
|------|------|------|------|--------|
| openclaw-gateway | :18789 | running | Agent 调度核心 | 小爪子 |
| wewe-rss-api | :4001 | running | 公众号文章 REST API | 小爪子 |

### 远程 / 云服务
| 服务 | URL/地址 | 状态 | 用途 | 备注 |
|------|----------|------|------|------|
| ClawHub | clawhub.ai | running | Skill 市场 | 官方服务 |
| OpenClaw Docs | docs.openclaw.ai | running | 文档站 | 官方服务 |

## 按状态分类
- ✓ 运行中：wewe-rss, openclaw-gateway, wewe-rss-api
- ⏸ 已暂停：skill-creator（已禁用）
- ✗ 已停止：-
```

## 详细记录格式（{service-name}.md）

```markdown
# {服务名}

## 基本信息
- **类型**：容器/Docker、本地服务、远程服务、 Skill
- **状态**：running / stopped / paused / removed
- **部署日期**：YYYY-MM-DD
- **用途**：一句话描述
- **负责人**：谁负责维护

## 访问信息
- **URL / 地址**：`http://localhost:4000`
- **端口**：4000（如适用）
- **凭证**：环境变量 / 文件路径（不写明文值）
  - 示例：`AUTH_CODE` 环境变量，配置在 docker-compose.yml

## 技术细节
- **依赖服务**：wewe-rss（容器）、OpenClaw Gateway
- **数据存储**：卷挂载路径、数据库类型
- **网络模式**：bridge / host / 自定义网络
- **健康检查**：`curl http://localhost:4001/api/health`

## 部署命令
```bash
cd ~/.openclaw/workspace/wewe-rss && docker compose up -d
```

## 最近变更
- 2026-04-01：新增部署，订阅了「数字生命卡兹克」公众号
```

## 工作流

### 记录新部署

1. **创建详细记录** → `memory/services/{service-name}.md`
2. **更新索引** → `memory/services/registry.md`

记录原则：
- 凭证只写位置，不写明文值
- 包含健康检查命令
- 包含部署/启动命令
- 包含关键配置路径

### 查询现有服务

**按端口查**：
```bash
grep -r "端口\|:4000\|:18789" memory/services/
```

**按类型查**：
```bash
grep -r "类型.*Docker\|容器" memory/services/ -l
```

**按状态查**：
```bash
grep -r "状态.*running\|running" memory/services/ -l
```

**快速概览**：
直接读 `memory/services/registry.md`

### 更新服务状态

当服务状态变更时：
1. 修改 `memory/services/{name}.md` 中的状态
2. 更新 `registry.md` 对应行
3. 记录变更时间和原因

## Agent Rules

- 部署新服务后，**立即**记录，不要"之后再说"
- 凭证只写变量名/路径，不写实际值
- 删除服务时，在记录中标记 `状态: removed`，保留文件（历史可追溯）
- 定期检查：收到服务相关问题时，先查 registry.md 确认状态
