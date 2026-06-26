---
name: openapi-contract-driven
description: >
  OpenAPI Contract-Driven Development workflow for multi-agent teams.
  Solves the systemic defect of "frontend invents endpoints, backend forgets to implement"
  in multi-agent collaboration. Use when: (1) starting a new project or standardizing
  API collaboration, (2) frequently seeing "blank page / 500 / 502" with no clear root cause,
  (3) need to establish API contract system across human/AI agent teams.

  OpenAPI 契约驱动开发工作流。解决多 Agent 协作中「前端自造端点，后端漏实现」
  这个系统性缺陷。Use when: (1) 新项目启动或已有项目需要规范 API 协作，
  (2) 频繁出现"页面空白 / 500 / 502"但找不到根因，
  (3) 需要在多人/AI agent 团队中建立 API 契约体系。
  NOT for: 单人项目、临时脚本、非 REST API 项目。
---

# OpenAPI Contract-Driven Development

**一句话：让前端 agent 连犯错的机会都没有。**

## 解决的问题

```
pm-agent 漏需求 → 架构漏设计 → 前端自造端点 → 后端没实现 → 用户看到 500

          ↓ 本 Skill 在此切断
          
OpenAPI YAML 是唯一契约 → 代码生成 → 前端只能调生成的函数 → 编译期暴露缺口
```

## 核心原理

| 防线 | 机制 | 拦截什么 |
|------|------|---------|
| ① 契约层 | `check-api-rules.sh` 7条规则 | operationId缺失、ApiResponse未包裹、ErrorResponse缺失 |
| ② 代码生成 | `apiClient.ts` 从前端唯一入口 | 手写 fetch/axios、自造端点 |
| ③ 运行时 | ops-agent 逐端口 curl | 路由错误、服务宕机、端口不匹配 |
| ④ 设计审计 | coordinator 前后端期望对照 | 架构漏设计、需求未覆盖 |

## 快速开始

### 1. 安装

```bash
openclaw skills install openapi-contract-driven

# 可选：openapi-typescript（TypeScript 类型生成）
npm install -D openapi-typescript
```

### 2. 从模板生成项目 OpenAPI 规范

```bash
cp references/openapi-template.yaml standards/{project}-openapi.yaml
# 编辑 YAML，定义你的端点
```

### 3. 运行规则检查

```bash
bash references/check-api-rules.sh standards/{project}-openapi.yaml
# 期望：✅ 6/7 通过
```

### 4. 自动生成前端 API Client

```bash
# 🆕 v1.1：一条命令从 YAML 生成完整 apiClient.ts
bash references/generate-api-client.sh standards/{project}-openapi.yaml \
  > frontend/src/api/generated/apiClient.ts
```

不用再手写端点函数。`generate-api-client.sh` 从 YAML 自动提取所有 path + method → operationId，生成类型安全的 `export const xxx = { ... }`。

### 5. 接入 CI 自动检查

```bash
# 🆕 v1.1：复制 GitHub Actions 工作流
cp references/ci-github-actions.yml .github/workflows/openapi-check.yml
```

之后每次 PR 都会自动运行 `check-api-rules.sh`，契约违规直接阻断合并。

### 6. 配置 Agent 团队

将 `references/agent-templates/` 下的规则片段合并到对应角色的 Agent 配置中：

| 模板文件 | 合并到 |
|---------|--------|
| `architecture-agent.md` | arch-agent / saas-arch-agent 的 AGENTS.md |
| `backend-agent.md` | backend-agent / legal-backend-agent 的 AGENTS.md |
| `frontend-agent.md` | frontend-agent / legal-frontend-agent 的 AGENTS.md |
| `ops-agent.md` | ops-agent / saas-ops-agent 的 AGENTS.md |
| `coordinator.md` | 小雨（main agent）的 coordinator-spawn-template.md |

### 存量项目？

→ 看 `references/migration-guide.md`，四阶段渐进式迁移，不改现有代码一行业务逻辑。

## 工作流

```
                    ┌─────────────────────────────┐
                    │  pm-agent: 产品需求           │
                    └──────────────┬──────────────┘
                                   ▼
                    ┌─────────────────────────────┐
                    │  arch-agent: 架构设计         │
                    │  → 输出 OpenAPI YAML (强制)   │
                    └──────────────┬──────────────┘
                                   ▼
                    ┌─────────────────────────────┐
                    │  coordinator: 对照审计         │
                    │  前端期望 vs YAML 定义         │
                    └──────────────┬──────────────┘
                           ┌───────┴───────┐
                           ▼               ▼
              ┌──────────────────┐ ┌──────────────────┐
              │ frontend-agent    │ │ backend-agent     │
              │ 只 import 生成的   │ │ 对照 YAML 实现    │
              │ apiClient         │ │ Controller        │
              └────────┬─────────┘ └────────┬─────────┘
                       │                    │
                       └────────┬───────────┘
                                ▼
                    ┌─────────────────────────────┐
                    │  ops-agent: 部署后验证        │
                    │  ① check-api-rules.sh        │
                    │  ② curl 逐端口逐端点          │
                    └─────────────────────────────┘
```

## 7 条核心规则

`.spectral.yaml` 规则集（不与 Spectral CLI 耦合，bash 脚本可独立运行）：

1. **operationId 完整性** — 前端代码生成强依赖（error）
2. **ApiResponse 强制 wrapper** — 防止「有的返回 T，有的返回 {data:T}」（error）
3. **ErrorResponse 标准模型** — 前端不用猜 error shape（warn）
4. **分页参数统一** — PageParam + SizeParam + SortParam（warn）
5. **health 端点** — 每个服务必须暴露（warn）
6. **日期格式显式标注** — `format: date-time`（warn）
7. **BearerAuth securityScheme** — 统一认证声明（error）

## 文件清单

```
openapi-contract-driven/
├── SKILL.md
├── README.md
└── references/
    ├── openapi-template.yaml          新项目起始模板
    ├── .spectral.yaml                  7 条核心规则
    ├── check-api-rules.sh              规则检查脚本（bash only）
    ├── generate-api-client.sh          🆕 YAML → TypeScript 自动生成
    ├── apiClient-template.ts           前端 apiClient 手动模板
    ├── ci-github-actions.yml           🆕 GitHub Actions CI 模板
    ├── migration-guide.md              🆕 存量项目迁移指南
    └── agent-templates/
        ├── architecture-agent.md
        ├── backend-agent.md
        ├── frontend-agent.md
        ├── ops-agent.md
        └── coordinator.md
```

## 跨项目验证

已在两个项目上跑通：

| 项目 | 端点 | 规则检查 | apiClient |
|------|------|---------|-----------|
| LexGuard（法律合同审查） | 30 | 6/7 ✅ | 11KB |
| 寓居智联（资产管理） | 46 | 6/7 ✅ | 17KB |

## 🆕 v1.1 更新日志

| 新增/修复 | 说明 |
|:------|:------|
| `generate-api-client.sh` | 从 YAML 自动生成 TypeScript apiClient，682行纯 bash/awk，零依赖 |
| `ci-github-actions.yml` | PR 时自动运行契约检查，违规阻断合并 |
| `migration-guide.md` | 存量项目四阶段渐进迁移，含 MVP 最小可行路径 |
| `check-api-rules.sh` 修复 | 不再因 YAML 缩进风格差异误报；$ref 和注释引用同时匹配 |
| 英文 description | 触达国际 DevOps 用户 |
| 路径修正 | `scripts/` → `references/` |

## 参考资料

- [Zalando REST API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) — 企业级 API 规范
- [Azure API Style Guide](https://github.com/Azure/azure-api-style-guide) — Spectral 规则集实践
- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.3) — 协议标准
