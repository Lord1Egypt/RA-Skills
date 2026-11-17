# Execute Command

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Execute Command` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.executecommand`
- node group: `core-nodes`

## 核心要点

- Documentation for the Execute Command node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- Enter each command on one line separated by `&&`. For example, you can combine the change directory (cd) command with the list (ls) command using `&&`.
- Enter each command on a separate line. For example, you can write the list (ls) command on a new line after the change directory (cd) command.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

