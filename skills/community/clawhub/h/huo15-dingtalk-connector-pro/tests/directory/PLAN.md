# directory（目录助手）测试方案

## 1. 目的与覆盖范围

`tests/directory` 覆盖目录助手功能，包括对等节点（peers）和群组（groups）的列表、过滤和实时查询。

主要覆盖（以测试文件实际引用为准）：

- **listDingtalkDirectoryPeers**：列出对等节点并规范化 ID
- **listDingtalkDirectoryGroups**：列出群组并去重
- **listDingtalkDirectoryPeersLive**：实时列出对等节点（回退到静态列表）
- **listDingtalkDirectoryGroupsLive**：实时列出群组（回退到静态列表）

## 2. 用例表（覆盖现有测试）

### 2.1 listDingtalkDirectoryPeers

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | 从 allowFrom 列出节点并规范化 ID | 正确解析 `user:a`、`dingtalk:user:b` 格式，去重并忽略 `*` 通配符 |

### 2.2 listDingtalkDirectoryPeers（带过滤）

| 序号 | 场景 | 期望 |
|------|------|------|
| 2 | 按查询和限制过滤 | 返回匹配查询且数量不超过 limit 的节点 |

### 2.3 listDingtalkDirectoryGroups

| 序号 | 场景 | 期望 |
|------|------|------|
| 3 | 从 groups 和 groupAllowFrom 列出群组并去重 | 合并两个来源，去重并忽略 `*` 通配符 |

### 2.4 实时列表函数

| 序号 | 场景 | 期望 |
|------|------|------|
| 4 | live list 函数回退到静态列表 | 返回与静态列表相同的结果 |

## 3. 预期正确输出与潜在错误

- **正确**：ID 格式规范化正确（去除前缀和空格）；通配符 `*` 被正确忽略；去重逻辑有效；查询和限制过滤正确；实时函数正确回退。
- **潜在错误原因**：ID 格式解析规则不完整；去重逻辑未考虑大小写；通配符处理不当导致意外匹配；查询过滤逻辑不正确。
