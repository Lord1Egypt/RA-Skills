# Postgres node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Postgres node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.postgres`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Postgres node in n8n. Follow technical documentation to integrate Postgres node into your workflows.

## 关键操作 / 参数线索

- **Delete**: Delete an entire table or rows in a table
- **Execute Query**: Execute an SQL query
- **Insert**: Insert rows in a table
- **Insert or Update**: Insert or update rows in a table
- **Select**: Select rows from a table
- **Update**: Update rows in a table
- **Credential to connect with**: Create or select an existing Postgres credential.
- **Operation**: Select **Delete**.
- **Schema**: Choose the schema that contains the table you want to work on. Select **From list** to choose the schema from the dropdown list or **By Name** to enter the schema name.
- **Table**: Choose the table that you want to work on. Select **From list** to choose the table from the dropdown list or **By Name** to enter the table name.
- **Command**: The deletion action to take:
- **Truncate**: Removes the table's data but preserves the table's structure.
- **Restart Sequences**: Whether to reset auto increment columns to their initial values as part of the Truncate process.
- **Delete**: Delete the rows that match the "Select Rows" condition. If you don't select anything, Postgres deletes all rows.
- **Select Rows**: Define a **Column**, **Operator**, and **Value** to match rows on.
- **Combine Conditions**: How to combine the conditions in "Select Rows". **AND** requires all conditions to be true, while **OR** requires at least one condition to be true.
- **Drop**: Deletes the table's data and structure permanently.
- **Cascade**: Whether to also drop all objects that depend on the table, like views and sequences. Available if using **Truncate** or **Drop** commands.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

