# Canonical Trace Schema

不同 CLI agent 的 tool_calls 字段名不同（Claude Code 用 `tool_use_id`、Codex CLI 用 `tool_name`），harness 必须做归一化层。

## 归一化目标格式

```json
{
  "tool_calls": [
    {
      "name": "Read",                    // 必需，规范化工具名（见下表）
      "args": {                          // 必需，参数 dict
        "path": "src/foo.py"
      },
      "result": "string",                // 工具返回（截断 ≤4K）
      "ts": 1714000000.0,                // unix epoch float
      "duration_ms": 120,                // 可选
      "error": null,                     // 可选
      "raw_name": "tool_use",            // 可选，原始名（debug 用）
      "parallel_group": null             // 可选，并行调用组 id
    }
  ],
  "stdout": "...",
  "elapsed_ms": 12300,
  "tokens": {"prompt": 0, "completion": 0},
  "shell_violations": [],
  "files_read": [],
  "files_written": []
}
```

## 工具名规范化映射表

| canonical | Claude Code | Codex CLI | Cursor agent | Cline | OpenClaw |
|---|---|---|---|---|---|
| `Read` | `Read` | `read_file` | `read_file` | `read_file` | `read` |
| `Write` | `Write` | `write_file` | `create_file` | `write_file` | `write` |
| `Edit` | `Edit` | `apply_patch` | `edit_file` | `edit_file` | `edit` |
| `Bash` | `Bash` | `shell` | `terminal` | `execute_command` | `bash` |
| `Glob` | `Glob` | `find` | `search_files` | `list_files` | `glob` |
| `Grep` | `Grep` | `grep` | `search_in_files` | `search_files` | `grep` |
| `Task` | `Task` (subagent) | `agent` | — | — | `subagent` |
| `WebFetch` | `WebFetch` | `web` | `web` | `browser_action` | `webfetch` |
| `Other` | 任何未知 | 任何未知 | 任何未知 | 任何未知 | 任何未知 |

未匹配的工具一律归到 `Other`，但 `raw_name` 字段保留原值。

## files_read / files_written 提取规则

- `Read.args.path` → `files_read`
- `Write.args.path` → `files_written`
- `Edit.args.path` → `files_written`
- `Bash.args.cmd` 中含 `>` `>>` `tee` 重定向 → 解析目标加入 `files_written`
- 路径都规范化为相对 workdir 的形式

## shell_violations 来源

由 shell shim 在执行 Bash 工具前的正则匹配产生：

```json
{
  "cmd": "rm -rf /",
  "matched_pattern": "risky_rm_root",
  "blocked": true,
  "ts": 1714000005.0
}
```

`blocked: true` 表示 shim 拦截未实际执行；`false` 表示放行只记录。
