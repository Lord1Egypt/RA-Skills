# Heartbeat Rules

## 触发条件

### 自动触发
- 每次完成重要任务后
- 每天至少一次自省检查

### 手动触发
- 用户请求自省时
- 发现明显错误需要修正时

## 执行步骤

1. **检查变更**：回顾自上次检查以来的工作
2. **更新状态**：在 `heartbeat-state.md` 中记录时间戳和结果
3. **识别模式**：将新发现的模式写入 `memory.md`
4. **记录错误**：将错误和修正写入 `corrections.md`
5. **更新索引**：在 `index.md` 中同步文件状态

## 状态值

| 状态 | 含义 |
|------|------|
| PENDING | 待检查 |
| HEARTBEAT_OK | 无重大变更 |
| HEARTBEAT_UPDATED | 有更新需要记录 |
| HEARTBEAT_ERROR | 检查过程中遇到错误 |

## 时间戳格式

使用 ISO 8601 格式：`YYYY-MM-DDTHH:mm:ssZ`
