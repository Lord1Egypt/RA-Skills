# Rename Keys

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Rename Keys` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.renamekeys`
- node group: `core-nodes`

## 核心要点

- Documentation for the Rename Keys node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Current Key Name**: The current name of the key you want to rename.
- **New Key Name**: The new name you want to assign to the key.

## 常用选项线索

- The **Regular Expression** you'd like to use.
- **Replace With**: Enter the new name you want to assign to the key(s) that match the **Regular Expression**.
- You can also choose these Regex-specific options:
- **Case Insensitive**: Set whether the regular expression should match case (turned off) or be case insensitive (turned on).
- **Max Depth**: Enter the maximum depth to replace keys, using `-1` for unlimited and `0` for top-level only.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

