## Tools

OmO injects 40+ tools into agents. Tools are grouped by function.

### Core file tools

| Tool | Description |
|------|-------------|
| read | Read file contents with optional line offset/limit |
| write | Write/overwrite file contents |
| edit | Exact string replacement in files |
| grep | Search file contents using regex |
| glob | Find files by glob pattern |
| bash | Execute shell commands with optional timeout and workdir |

### LSP tools

| Tool | Description |
|------|-------------|
| lsp_goto_definition | Jump to where a symbol is defined |
| lsp_find_references | Find all usages of a symbol across workspace |
| lsp_symbols | Get symbols from file or search workspace |
| lsp_diagnostics | Get errors/warnings before building |
| lsp_prepare_rename | Check if rename is valid |
| lsp_rename | Rename symbol across entire workspace |

### AST-Grep tools

| Tool | Description |
|------|-------------|
| ast_grep_search | Search code patterns using AST-aware matching (25 languages) |
| ast_grep_replace | Replace code patterns with AST-aware rewriting (dry-run by default) |

### Delegation tools

| Tool | Description |
|------|-------------|
| task | Spawn agent task with category or direct agent selection |
| background_output | Get output from background task |
| background_cancel | Cancel running background tasks |

### Visual tools

| Tool | Description |
|------|-------------|
| look_at | Analyze media files (PDFs, images, diagrams) |

### Skill tools

| Tool | Description |
|------|-------------|
| skill | Load a skill to get detailed instructions |
| skill_mcp | Invoke MCP server operations from skill-embedded MCPs |
| slashcommand | Load a skill or execute a command |

### Session tools

| Tool | Description |
|------|-------------|
| session_list | List all OpenCode sessions |
| session_read | Read messages from a session |
| session_search | Search across session messages |
| session_info | Get session metadata |

### Task management tools

| Tool | Description |
|------|-------------|
| todowrite | Create/update structured task list |
| todoread | Read current todo list |

### Interactive tools

| Tool | Description |
|------|-------------|
| interactive_bash | Tmux-based interaction for TUI apps (vim, htop, etc.) |

### Web tools

| Tool | Description |
|------|-------------|
| webfetch | Fetch and convert URL content |
| question | Ask user questions with multiple choice |

### MCP-provided tools

| Tool | Source MCP | Description |
|------|-----------|-------------|
| websearch_web_search_exa | websearch | Web search via Exa |
| context7_resolve-library-id | context7 | Resolve library to Context7 ID |
| context7_query-docs | context7 | Query library documentation |
| grep_app_searchGitHub | grep_app | Search code across GitHub repos |

### GitHub tools (via octocode MCP)

| Tool | Description |
|------|-------------|
| githubSearchCode | Search code patterns across GitHub |
| githubGetFileContent | Read file content from GitHub repos |
| githubViewRepoStructure | Display repo directory structure |
| githubSearchRepositories | Search GitHub repositories |
| githubSearchPullRequests | Search and read pull requests |

### Tool restrictions

You can restrict which tools an agent or category has access to:

```json
{
  "agents": {
    "oracle": {
      "tools": ["read", "grep", "glob", "lsp_diagnostics"]
    }
  }
}
```
