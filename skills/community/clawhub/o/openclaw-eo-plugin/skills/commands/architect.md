---
name: architect
source: eo-native
compatibility: full
description: 架构设计指令，调度 Architect 专家进行系统架构设计和技术选型
whenToUse: 当需要进行系统架构设计、技术选型、风险评估时使用
allowedTools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
context: fork
expert: architect
aliases: ["/architect", "/架构", "/architecture"]
version: 1.0.1
---

# /architect - 架构设计指令

> **v1.0.1 新增**: 支持 `context: fork` 模式，可作为子代理并行执行

## 功能
调度 Architect 专家，进行系统架构设计和技术选型。

## 参数
```
/architect <需求描述> [options]

参数:
  <需求描述>    必填，业务需求或系统描述
  --scale <规模> 可选，系统规模
                  值: small | medium | large | enterprise
                  默认: medium
  --constraints <约束> 可选，技术约束
                         值: 云原生 | 传统部署 | 混合云
                         默认: 云原生
```

## 执行流程（v1.0.1 Fork 模式）

```
用户输入 /architect "设计一个日活10万电商平台"
    │
    ▼
┌─────────────────────────────────────┐
│  registry.ts 解析 frontmatter        │
│  context: fork                      │
│  expert: architect                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  spawnExpertAgent({                  │
│    agentType: 'architect',           │
│    isolation: 'worktree'            │
│  })                                 │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Architect 子代理     │
    │ - 技术选型            │
    │ - 架构图绘制          │
    │ - 风险评估            │
    └─────────────────────┘
```

## 输出格式

```markdown
# 🏗️ 架构设计 - [项目名称]

## 📊 系统规模
- **日活用户**: 10,000+
- **日均请求**: 1,000,000
- **数据量**: 100GB/天

## 🛠️ 技术选型

| 层级 | 推荐技术 | 备选 |
|------|---------|------|
| 前端 | Next.js 14 | Vue 3 |
| 后端 | Node.js + Fastify | Go + Gin |
| 数据库 | PostgreSQL | MySQL |
| 缓存 | Redis Cluster | Memcached |
| 消息队列 | Kafka | RabbitMQ |
| 容器化 | Docker + K8s | - |

## 🏛️ 高层架构

## 📦 模块划分

### 模块1: 用户中心
- **职责**: 用户注册、登录、权限管理
- **API**: `/api/users/*`
- **数据库**: `users` 表

### 模块2: 订单系统
- **职责**: 订单创建、支付、履约
- **API**: `/api/orders/*`

## ⚠️ 风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 高并发 | 中 | 高 | 自动扩缩容 + 限流 |
| 数据一致性 | 高 | 中 | Saga 模式 + 补偿事务 |
| 第三方 API 不稳定 | 中 | 中 | 熔断器 + 重试 |
```

## 对应专家
- Backend Architect
- Solution Architect
- Cloud Architecture Specialist
