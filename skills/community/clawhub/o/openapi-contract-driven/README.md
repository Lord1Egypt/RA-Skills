# OpenAPI Contract-Driven Development

> 让前端 agent 连犯错的机会都没有。

## 🔥 起源：一次全链路事故

2026-06-07，LexGuard（法律合同审查助手）生产环境出现「合同列表 500」「审查规则 502」「设置页面空白」三个用户报障。

排查发现：

```
pm-agent 漏需求 → arch-agent 漏设计 → frontend-agent 自造端点 → backend-agent 没实现 → 用户 500
```

**API 契约审计结果触目惊心：**

```
🟢 32 端点正常    🟡 5 个路由/缺失    🔴 16 个致命问题
```

16 个 🔴 的根因全是同一类问题：**前端 agent 和 backend agent 是两套独立大脑，没有共享一份 API 契约**。

三个小时后，本 Skill 诞生。

---

## 🛡️ 四道防线

```
OpenAPI YAML 是唯一契约
    │
    ▼
┌─────────────────────────────────┐
│ ① 规范层：check-api-rules.sh     │  7 条规则，部署前自动检查
│ ② 代码层：apiClient 生成         │  前端只能 import 生成的函数
│ ③ 运行时：ops-agent curl 验证     │  部署后逐端口逐端点
│ ④ 审计层：coordinator 期望对照    │  前后端需求 vs 契约 diff
└─────────────────────────────────┘
```

**效果：** 前端 agent 想手写 `fetch('/api/v1/xxx')`？`apiClient.ts` 里没有这个函数 → TypeScript 编译报错。改 `apiClient.ts`？文件头标了「由 OpenAPI 契约生成，禁止手改」，Git blame 随时追责。

**唯一路径：** 改 OpenAPI YAML → 重新生成 → 两端同步 → Git 提交记录完整。

---

## 💡 跨项目验证

在 LexGuard 和寓居智联两个生产项目同时跑通：

| 项目 | 微服务 | 端点 | 规则检查 | apiClient |
|------|--------|------|---------|-----------|
| LexGuard（法律合同审查） | 4 | 30 | 6/7 ✅ | 11KB |
| 寓居智联（资产管理） | 10 | 46 | 6/7 ✅ | 17KB |

---

## 🚀 5 分钟启动

```bash
# 1. 安装
openclaw skills install openapi-contract-driven

# 2. 从模板创建
cp references/openapi-template.yaml standards/my-project-openapi.yaml

# 3. 验证 YAML 规范
bash references/check-api-rules.sh standards/my-project-openapi.yaml
# 期望：✅ 6/7 通过

# 4. 🆕 自动生成前端 apiClient
bash references/generate-api-client.sh standards/my-project-openapi.yaml \
  > frontend/src/api/generated/apiClient.ts

# 5. 🆕 接入 CI
cp references/ci-github-actions.yml .github/workflows/openapi-check.yml
```

存量项目？→ 看 `references/migration-guide.md`

---

## 🆕 v1.1 更新日志

| 新增/修复 | 说明 |
|:------|:------|
| `generate-api-client.sh` | YAML → TypeScript 自动生成，682行纯 bash/awk |
| `ci-github-actions.yml` | PR 时自动检查契约，违规阻断合并 |
| `migration-guide.md` | 存量项目四阶段渐进迁移，含 MVP 路径 |
| `check-api-rules.sh` 修复 | 不再因缩进风格差异误报 |
| 英文 description | 触达国际 DevOps 用户 |
| 路径修正 | `scripts/` → `references/` |

---

## 📋 包含文件（v1.1 修正版）

```
openapi-contract-driven/
├── SKILL.md                              ← 本 Skill
├── README.md                             ← 本文件
├── references/
│   ├── openapi-template.yaml              ← 新项目起始模板
│   ├── .spectral.yaml                     ← 7 条核心规则
│   ├── check-api-rules.sh                 ← 无依赖检查脚本（bash only）
│   ├── generate-api-client.sh             ← 🆕 YAML → TypeScript 自动生成
│   ├── apiClient-template.ts              ← 前端 apiClient 手动模板
│   ├── ci-github-actions.yml              ← 🆕 GitHub Actions CI 模板
│   ├── migration-guide.md                 ← 🆕 存量项目四阶段迁移指南
│   └── agent-templates/                   ← 5 个角色规则片段
│       ├── architecture-agent.md           ← 架构师：必须输出 YAML
│       ├── backend-agent.md                ← 后端：禁止自造端点
│       ├── frontend-agent.md               ← 前端：禁止手写 fetch
│       ├── ops-agent.md                    ← 运维：部署后两步验证
│       └── coordinator.md                  ← 协调者：契约审计流程
```

---

## 🎯 什么时候用

- 新项目启动，需要建立 API 规范体系
- 多个 AI agent 并行开发，频繁出现「前后端不一致」
- 用户反馈「页面空白／502／500」但找不出根因
- 想从根本上杜绝「前端自造端点，后端漏实现」

**什么时候不用：** 单人项目、非 REST API、临时脚本。

---

## 📖 参考资料

- [Zalando REST API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) — 企业级 API 规范范本
- [Azure API Style Guide](https://github.com/Azure/azure-api-style-guide) — Spectral 规则集实践
- [OpenAPI 3.0.3](https://spec.openapis.org/oas/v3.0.3) — 协议标准
