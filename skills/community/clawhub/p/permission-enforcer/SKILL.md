# Permission Enforcer

统一权限中间层 —— 集中管理文件写入、bash 执行、MCP 工具等权限判断。

## 配置文件

`~/.openclaw/workspace/policy/enforcer-policy.json`

## 规则类型

| Action | Scope/Pattern | Effect | 说明 |
|--------|--------------|--------|------|
| `file_write` | `workspace` | allow | 允许写入 workspace 内文件 |
| `file_write` | `outside_workspace` | deny | 禁止写入 workspace 外 |
| `file_write` | `openclaw_core` | prompt | 修改核心文件需确认 |
| `bash` | `rm -rf /` 等 | deny | 禁止危险删除命令 |
| `bash` | `curl`, `wget` | prompt | 网络下载需确认 |
| `bash` | `sudo` | prompt | sudo 需确认 |
| `mcp` | `write_file` | prompt | MCP 文件写入需确认 |

## 使用

```javascript
import { checkPermission } from './permission-enforcer.mjs';

const result = await checkPermission('file_write', '/Users/andy51/.openclaw/workspace/test.txt');
// result: { allowed: true } | { allowed: false, reason: '...' } | { prompt: true, message: '...' }
```
