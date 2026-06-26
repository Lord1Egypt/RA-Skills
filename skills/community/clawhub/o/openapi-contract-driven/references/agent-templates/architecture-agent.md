# Architecture Agent — OpenAPI 契约驱动规则

将此内容合并到 arch-agent 或 saas-arch-agent 的 AGENTS.md。

---

## OpenAPI 输出要求

**架构设计交付时必须包含 OpenAPI 3.0 YAML。** 这是前后端的唯一 API 契约。Markdown 文档为辅助说明。

- 输出路径：`standards/{project}-openapi.yaml`
- 参考模板：`skills/openapi-contract-driven/references/openapi-template.yaml`
- 每个微服务必须暴露 health 端点：`GET /api/v1/{module}/health`
- 所有端点标注 operationId（驼峰命名）
- 统一 Auth: Bearer JWT SecurityScheme
- 统一响应格式：`{code, message, data}`
- 统一错误模型：ErrorResponse（5 个标准响应）

## 强制项

- ❌ 不能用 Markdown 替代 OpenAPI YAML
- ❌ 不能漏 service tag 的任何端点
- ❌ 不能漏 health 端点
