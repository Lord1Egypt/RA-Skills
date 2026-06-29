# 需求管理模块

当用户请求管理需求时，调用本模块。

---

## 1. 查看需求列表

### 查看所有需求

```
1. 读取 {project}/.myknowledge/PROJECT-STATUS.md 或 ~/MyKnowledge/global/PROJECT-STATUS.md
2. 读取每个需求的 README.md 获取优先级和标签
3. 按优先级排序（P0→P1→P2→P3），同优先级按时间倒序
4. 格式化输出：

## 需求列表

### 活跃需求
| 优先级 | ID | 标题 | 标签 | 状态 | 创建时间 |
|--------|----|------|------|------|----------|
| P0 | REQ-001 | 登录崩溃修复 | 前端,bug | In Progress | 2026-06-10 |
| P1 | REQ-003 | 仪表盘重构 | 前端 | Created | 2026-06-11 |
| P2 | REQ-002 | 导出PDF | 后端 | Review | 2026-06-09 |

### 已完成
| 优先级 | ID | 标题 | 标签 | 完成时间 |
|--------|----|------|------|----------|
| P1 | REQ-XXX | xxx | 标签 | 2026-06-09 |
```

### 查看特定需求

```
用户：查看 REQ-001
1. 读取 requirements/REQ-001/README.md
2. 显示完整需求信息
```

---

## 2. 更新需求状态

### 支持的状态流转

```
Created → In Progress → Review → Done
Created → Cancelled
```

### 操作流程

```
1. 确认需求 ID 和目标状态
2. 读取当前需求 README.md
3. 更新"状态"字段
4. 在"变更记录"表格追加新记录
5. 更新 PROJECT-STATUS.md 中的需求列表
6. 更新 requirements/README.md 需求索引（同步状态变更）
```

### 示例

```
用户：更新 REQ-001 状态为 In Progress

AI：✅ 已更新 REQ-001 状态：Created → In Progress

📝 已自动记录会话：
| 时间 | 摘要 | 涉及 |
| 15:30 | 状态变更为 In Progress | REQ-001 |
```

---

## 3. 更新需求内容

### 可更新的字段

- 需求描述
- 验收标准
- 相关资源
- 备注

### 操作流程

```
1. 确认需求 ID 和要更新的字段
2. 读取当前需求 README.md
3. 更新对应字段
4. 在"变更记录"表格追加新记录
```

---

## 4. 归档需求

### 归档已完成需求

```
1. 确认需求 ID
2. 将需求目录从 requirements/ 移动到 archive/
3. 更新 PROJECT-STATUS.md（从活跃需求移到已完成）
4. 更新 requirements/README.md 需求索引（移除已归档项）
5. 在需求 README.md 追加归档记录
```

### 批量归档

```
用户：归档所有已完成的需求

AI：✅ 已归档 3 个需求：
- REQ-001
- REQ-002
- REQ-003
```

---

## 5. 删除需求

### 删除（谨慎使用）

```
1. 确认需求 ID
2. 确认用户知道这是不可逆操作
3. 删除需求目录
4. 更新 PROJECT-STATUS.md
5. 更新 requirements/README.md 需求索引（移除已删除项）
```

---

## 自然语言示例

| 用户输入 | AI 响应 |
|----------|---------|
| 查看所有需求 | 列出 PROJECT-STATUS.md 中的需求 |
| REQ-001 进展如何？ | 显示 REQ-001 详情 |
| 把 REQ-001 改成 In Progress | 更新状态并记录 |
| 归档 REQ-001 | 移动到 archive/ |
| REQ-001 的描述不对 | 询问新的描述内容并更新 |

---

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| 需求不存在 | 检查 ID 是否正确，列出可用需求 |
| 状态流转无效 | 按以下格式提示： |
| | ⚠️ 状态流转无效：{当前状态} → {目标状态} |
| | |
| | MyKnowledge 支持的状态流转： |
| |   • Created → In Progress |
| |   • In Progress → Review |
| |   • In Progress → Cancelled |
| |   • Review → Done |
| |   • Review → In Progress（退回修改） |
| | |
| | 你可以： |
| |  1 — 查看需求当前状态 |
| |  2 — 选择有效的状态重新更新 |
| |  回复数字即可 |
| 文件损坏 | 建议删除重建或使用其他需求 |
