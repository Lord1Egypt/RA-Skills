# Compatibility

## Supported Client

当前 skill 包要求 PixCake 客户端版本：

- `9.0.0` 及以上

## Treat As Version Mismatch

出现以下任一信号时，优先按“客户端版本过旧”或“客户端与 skill 包版本不匹配”处理：

- PixCake app 已启动，但 `mcporter --config ~/.openclaw/workspace/config/mcporter.json list pixcake --json` 仍无法拿到可用 server
- `mcporter --config ~/.openclaw/workspace/config/mcporter.json list pixcake --json` 缺少当前场景必需工具
- `mcporter --config ~/.openclaw/workspace/config/mcporter.json call pixcake.<tool_name> ...` 返回 `tool not found`、`unknown tool`、`method not found`

## Required Response

第一响应应为：

- 提示用户升级到 PixCake 客户端 `9.0.0` 或更高版本
- 升级后仍无法处理，再联系工作人员或客服支持

## Retry Policy

- 默认不重试
- 只有用户明确要求时，最多做一次简短重试
- 一次重试后仍失败，就回到升级建议

## Do Not Lead With

不要把以下建议作为第一响应：

- “再等几秒试试”
- “先重启一下客户端”
- “我再帮你切一个 MCP 命令路径看看”
- “我连续重试几次”
- “我猜另一个工具名再试试”
