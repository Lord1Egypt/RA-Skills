# Object Type — 把数据库的表变成"会说话"的业务对象

## 4层结构

**第一层：元数据层（Metadata）**

| 字段 | 作用 |
|------|------|
| API Name | `snake_case`，一旦确定不可更改，跨系统对象加业务前缀 |
| Display Name | 给人看的展示名称，支持多语言本地化 |
| Description | **最重要**——AI Agent 理解对象语义的核心输入，不能留空 |
| Sink & Cube | 是否将数据同步到 Foundry 数据仓库（可选，用于 BI 分析场景） |
| Status | Active / Deprecated。Deprecated 后仍可查询，Foundry UI 标注警告 |

**第二层：属性层（Properties）**
- **主键**：必须有且仅有一个，优先 UUID/雪花 ID，不用业务字段（业务字段会变，主键选错导致所有下游 Link 失效）
- **普通属性**：每个属性包含 Type（数据类型）、Display Name / Description、Security Metric（可选，用于列级安全控制）
- **派生属性**：由 Function 动态计算。需要实时性或跨对象聚合时用派生属性；纯静态转换在 Pipeline 层预计算更高效

**第三层：数据源层**
- 主数据集（Primary Backing Dataset）：核心数据源
- 补充数据集：最多 3 个，关联键必须建索引

**第四层：安全层（三级，先粗后细）**
- 对象级（Object-Level）：控制谁能看到这个对象，最粗粒度，优先配置
- 列级（Property-Level）：隐藏薪资、手机号等敏感字段
- 行级（Row-Level）：多租户场景，按属性值过滤行

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 用业务字段当主键 | 用 UUID/雪花 ID |
| Description 留空 | AI Agent 依赖它理解对象语义 |
| 一步到位配置行级权限 | 先搭对象级粗粒度，再逐步细化 |
