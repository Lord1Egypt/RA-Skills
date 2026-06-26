# config（配置 schema）测试方案

## 1. 目的与覆盖范围

`tests/config` 覆盖钉钉配置 schema 的验证逻辑，确保配置项的默认值和约束条件正确应用。

主要覆盖（以测试文件实际引用为准）：

- **DingtalkConfigSchema**：Zod schema 验证配置结构

## 2. 用例表（覆盖现有测试）

### 2.1 DingtalkConfigSchema

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | 空配置应用默认值 | dmPolicy 为 `open`，groupPolicy 为 `open`，requireMention 为 `true` |
| 2 | defaultAccount 不在 accounts 列表中 | 抛出包含 `defaultAccount` 的错误 |
| 3 | dmPolicy 为 allowlist 但 allowFrom 为空 | 抛出包含 `allowFrom` 的错误 |

## 3. 预期正确输出与潜在错误

- **正确**：默认值正确应用；跨字段引用约束有效验证（defaultAccount 必须在 accounts 中）；条件约束正确触发（allowlist 需要 allowFrom）。
- **潜在错误原因**：默认值与实际业务需求不一致；约束条件过于宽松或严格；错误提示信息不够清晰。
