# Coordinator — API 契约审计流程

合并到 coordinator-spawn-template.md 或 main agent 的 AGENTS.md。

---

## 🔗 API 契约审计

**何时执行：** 任何微服务部署上线后 / 多 agent 开发完成后 / 用户报告「页面空白」时。

### 步骤

1. `read standards/{project}-openapi.yaml`
2. 提取所有 `operationId + path + method` → 记为 A（契约端点）
3. 从前端 apiClient 提取所有导出函数 → 记为 B（前端调用）
4. 对比：
   - **B 有、A 无** → 🚨 前端调了但后端没设计 → 追问 saas-arch-agent
   - **A 有、服务器 502/无响应** → 🚨 部署坏了 → 派 saas-ops-agent
   - **A 有、服务器 200** → ✅
5. 输出审计表，派活修缺口

## 决策矩阵

| 触发信号 | 动作 |
|---------|------|
| 用户反馈「页面空白/X 模块没数据」 | 先执行 API 契约审计 |
| arch-agent 交付架构 | 检查是否输出 OpenAPI YAML。没有 → 打回 |
| ops-agent 部署完成 | 派 ops-agent 执行两步验证 |
| 多 agent 开发完成 | coordinator 执行契约审计 |
