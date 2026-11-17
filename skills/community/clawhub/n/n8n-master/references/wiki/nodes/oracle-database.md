# Oracle Database node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Oracle Database node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.oracledb`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Oracle Database node in n8n. Follow technical documentation to integrate Oracle Database node into your workflows.

## 关键操作 / 参数线索

- **Delete**: Delete an entire table or rows in a table
- **Execute SQL**: Execute an SQL statement
- **Insert**: Insert rows in a table
- **Insert or Update**: Insert or update rows in a table
- **Select**: Select rows from a table
- **Update**: Update rows in a table
- **Credential to connect with**: Create or select an existing Oracle Database credential.
- **Operation**: Select **Delete**.
- **Schema**: Choose the schema that contains the table you want to work on. Select **From list** to choose the schema from the dropdown list or **By Name** to enter the schema name.
- **Table**: Choose the table that you want to work on. Select **From list** to choose the table from the dropdown list, or select **By Name** to enter the table name.
- **Command**: The deletion action to take:
- **Truncate**: Removes the table's data but preserves the table's structure.
- **Delete**: Delete the rows that match the "Select Rows" condition. If you don't select anything, Oracle Database deletes all rows.
- **Select Rows**: Define a **Column**, **Operator**, and **Value** to match rows on. The value
- **Combine Conditions**: How to combine the conditions in "Select Rows". The **AND** requires all conditions to be true, while **OR** requires at least one condition to be true.
- **Drop**: Deletes the table's data and structure permanently.
- **Auto Commit**: When this property is set to true, the transaction in the current connection is automatically committed at the end of statement execution.
- **Statement Batching**: The way to send statements to the database:

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

