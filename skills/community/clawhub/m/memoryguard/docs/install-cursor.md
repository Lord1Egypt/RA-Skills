# Install MemoryGuard for Cursor

This guide connects [Cursor](https://cursor.com) to the MemoryGuard MCP memory
backend.

## Prerequisites

- **Python 3.10+** on your PATH (`python --version`)
- **Cursor** installed and working
- MemoryGuard cloned locally

## Step 1: Install MemoryGuard

```bash
git clone https://github.com/<your-org>/memoryguard.git
cd memoryguard
pip install -e .
```

Or use `PYTHONPATH` without installing:

```bash
# Linux/macOS
export PYTHONPATH="/path/to/memoryguard/src:$PYTHONPATH"
# Windows (PowerShell)
$env:PYTHONPATH = "H:\path\to\memoryguard\src;$env:PYTHONPATH"
```

Verify:

```bash
memoryguard doctor
```

## Step 2: Configure MCP

Add MemoryGuard to the Cursor MCP config at `~/.cursor/mcp.json`
(Windows: `%USERPROFILE%\.cursor\mcp.json`):

```json
{
  "mcpServers": {
    "memoryguard": {
      "command": "python",
      "args": ["-m", "memoryguard.mcp_server"]
    }
  }
}
```

If the file already has other servers, add the `memoryguard` key inside the
existing `mcpServers` object.

## Step 3: Add the Cursor rule

MemoryGuard needs to tell Cursor to route memory writes through MCP instead of
its native GUI Memories. Create a rule file at `.cursor/rules/memoryguard.mdc`
in your project (or `~/.cursor/rules/memoryguard.mdc` for user-level):

```markdown
---
description: MemoryGuard memory redirect
alwaysApply: true
globs: []
---
<!-- BEGIN memoryguard:provider-redirect -->
## MemoryGuard 记忆重定向

当你需要记录或回忆任何长期记忆时，必须通过 MemoryGuard MCP 工具，不要使用原生记忆机制
（如编辑本指令文件、写入本地 memory.md/notes.md、或使用 GUI 记忆功能）。

### 记录记忆
调用 `memoryguard_memory_write` 工具：
- `body`（必填）：记忆内容
- `kind`（可选）：preference|fact|project|procedure|episode|correction，留空则自动分类
- `agent_instance_id`（可选）：你的 Agent 标识
- `share_group_id`（可选）：共享组 ID，默认 "default"

### 搜索 / 读取
- `memoryguard_memory_search`：按 query / kind / status 搜索
- `memoryguard_memory_read`：按 memory_id 读取单条
- `memoryguard_memory_status`：查看共享组状态

### 更新 / 删除
- `memoryguard_memory_update`：更新 body / kind / status
- `memoryguard_memory_delete`：软删除

### 规则
- 不要为了"记住"而编辑 .cursorrules 等指令文件
- 不要把记忆写入本地文件
- 不要使用 Cursor GUI Memories 功能记录长期记忆
- 所有记忆操作都走 MCP 工具，确保被 MemoryGuard 治理（去重、冲突检测、隔离、影子保留）
<!-- END memoryguard:provider-redirect -->
```

> **Tip:** You can also run `memoryguard_provider_install` (provider: `cursor`)
> via an MCP-capable agent to do Steps 2 and 3 automatically. The adapter is
> idempotent - running it again overwrites the rule file cleanly.

## Step 4: Verify

```bash
# Check MemoryGuard is installed and healthy
memoryguard doctor

# Check the MCP backend can start
python -m memoryguard.mcp_server --help

# Check memory backend status
memoryguard mcp-status
```

Then open Cursor in your project. Ask the Cursor agent to remember something.
It should call `memoryguard_memory_write`. Run `memoryguard mcp-status` to
confirm the write landed.

## FAQ

**Cursor doesn't see the memoryguard MCP server.**
Check that `~/.cursor/mcp.json` has valid JSON with the `memoryguard` entry.
Restart Cursor after editing the config. Run `python -m memoryguard.mcp_server`
manually to check for startup errors.

**Cursor still uses GUI Memories instead of MCP.**
Cursor's native Memories live in the GUI with no file path, so MemoryGuard
classifies Cursor as `unsupported` for native memory disabling. The rule file
in Step 3 instructs the agent to use MCP instead, but you may need to avoid
using the GUI Memories feature manually.

**Project-level vs user-level rule?**
Project-level `.cursor/rules/memoryguard.mdc` applies to one project.
User-level `~/.cursor/rules/memoryguard.mdc` applies everywhere. Use
project-level if you only want MemoryGuard in specific projects.

**Windows: `python` not found.**
Use `py` instead of `python` in the config, or ensure Python is on your PATH.
