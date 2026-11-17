# Install MemoryGuard for Codex

This guide connects [Codex CLI](https://github.com/openai/codex) to the
MemoryGuard MCP memory backend.

## Prerequisites

- **Python 3.10+** on your PATH (`python --version`)
- **Codex CLI** installed and working
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

Add MemoryGuard to your Codex MCP config at `~/.codex/config.toml`
(Windows: `%USERPROFILE%\.codex\config.toml`):

```toml
[mcp_servers.memoryguard]
command = "python"
args = ["-m", "memoryguard.mcp_server"]
```

If the file already has other MCP servers, just append the section above.

## Step 3: Add the AGENTS.md instruction

MemoryGuard needs to tell Codex to route memory writes through MCP instead of
its native memory. Add this to your `AGENTS.md` - either the project-level
file (`./AGENTS.md`) or the user-level file (`~/.codex/AGENTS.md`):

```markdown
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
- 不要为了"记住"而编辑 AGENTS.md 等指令文件
- 不要把记忆写入本地文件
- 所有记忆操作都走 MCP 工具，确保被 MemoryGuard 治理（去重、冲突检测、隔离、影子保留）
<!-- END memoryguard:provider-redirect -->
```

> **Tip:** You can also run `memoryguard_provider_install` (provider: `codex`)
> via an MCP-capable agent to do Steps 2 and 3 automatically. The adapter is
> idempotent - running it again updates the config without duplicating.

## Step 4: Verify

```bash
# Check MemoryGuard is installed and healthy
memoryguard doctor

# Check the MCP backend can start
python -m memoryguard.mcp_server --help

# Check memory backend status
memoryguard mcp-status
```

Then start a Codex session in your project. Ask Codex to remember something.
It should call `memoryguard_memory_write`. Run `memoryguard mcp-status` to
confirm the write landed.

## FAQ

**Codex doesn't see the memoryguard MCP server.**
Check that `~/.codex/config.toml` has the `[mcp_servers.memoryguard]` section
and that `python -m memoryguard.mcp_server` runs without errors.

**Codex still writes to AGENTS.md instead of MCP.**
Make sure the instruction snippet in Step 3 is in the AGENTS.md file Codex
actually reads (project-level `./AGENTS.md` takes precedence). Restart the
Codex session after editing.

**Can I use a project-level config instead of user-level?**
Codex reads `~/.codex/config.toml` for MCP servers. The AGENTS.md instruction
can be project-level (`./AGENTS.md`) or user-level
(`~/.codex/AGENTS.md`).

**Windows: `python` not found.**
Use `py` instead of `python` in the config, or ensure Python is on your PATH.
