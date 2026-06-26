---
name: repo-json-generator
description: Convert Git repository code to structured JSON instructions for AI agents. Fetches code from Git repositories (GitHub, GitLab, etc.), generates structured JSON instructions for accurate code updates and processing. Platform-agnostic tool for AI agent workflows.
metadata: { "openclaw": {"requires": { "bins": ["python3", "git"], "env":["GITHUB_TOKEN"]},"primaryEnv":"GITHUB_TOKEN" } }
---

# Repo JSON Generator

Convert Git repository code to structured JSON instructions for AI agents and automation tools.

This tool fetches code from Git repositories (GitHub, GitLab, Bitbucket, etc.) and generates **structured JSON instructions** that can be consumed by any AI agent or automation system for accurate code processing and updates.

**Version 3.0.0 - Modular Architecture (Latest)**
- ✅ **NEW**: Modular codebase architecture for better maintainability
- ✅ `info` command now includes complete file content in JSON output
- ✅ Unified `--no-instructions` parameter across all commands
- ✅ Consistent terminal output - always shows summary information
- ✅ Flexible file output - full formatted or pure JSON format
- ✅ `info` command supports `--filter` and `--exclude` parameters for file filtering

---

# 🏗️ Architecture Overview (v3.0.0)

## Modular Structure

The codebase has been restructured from a single monolithic script into a modular architecture:

```
scripts/
├── generator.py          # Main entry point (CLI router)
├── core/
│   ├── constants.py                # Shared constants and configuration
│   ├── temp_manager.py             # Cross-platform temp directory management
│   ├── circuit_breaker.py          # Circuit breaker & retry mechanism
│   └── security.py                 # Sensitive information protection
├── git/
│   └── repository.py               # Git repository operations
├── processors/
│   ├── file_processor.py           # File reading and filtering
│   └── instruction_gen.py          # JSON instruction generation
└── output/
    └── streaming.py                # Streaming/chunked output
```

## Module Dependencies

```
core/ (no dependencies)
  ↓
git/ (depends on core)
  ↓
processors/ (depends on core, git)
  ↓
output/ (depends on processors)
  ↓
generator.py (depends on all modules)
```

## Benefits

- **Maintainability**: Each module can be updated independently
- **Testability**: Modules can be tested in isolation
- **Reusability**: Core components can be reused in other projects
- **Readability**: Smaller, focused files are easier to understand

---

# 🔄 AI Agent Integration Architecture

## Overview

This tool (`generator`) generates structured JSON from Git repositories that can be consumed by **any AI agent or automation system**:

```
┌─────────────────────┐         ┌──────────────────────┐
│  repo-json-         │  JSON   │  AI Agent /          │
│  generator          │ ──────> │  Automation System   │
│                     │  Data   │                      │
│  1. Fetch from      │         │  2. Process Code     │
│     Git Repo        │         │     Update Files     │
│  3. Generate JSON   │         │  3. Execute Actions  │
│     Instructions    │         │                      │
└─────────────────────┘         └──────────────────────┘
```

## Why Structured JSON?

| Aspect | Natural Language | Structured JSON |
|--------|------------------|-----------------|
| **Accuracy** | 70-80% | 90-95% |
| **File Completeness** | May miss files | Guaranteed by JSON structure |
| **Control** | Hard to verify | Easy to validate before processing |
| **Batch Processing** | Difficult | Built-in support |
| **Best For** | Simple queries | Full sync, large updates |

## Integration Workflow

### Standard Flow

```
User Request
    ↓
"Generate JSON from Git repo" / "Convert code to JSON"
    ↓
Step 1: generator
    ├─ Clone repository from Git
    ├─ Read all code files
    ├─ Generate structured JSON instructions
    └─ Output: JSON data with file contents
    ↓
Step 2: Your AI Agent / System
    ├─ Receive JSON instructions
    ├─ Parse file list and contents
    ├─ Create/overwrite each file
    └─ Output: Updated file list for verification
    ↓
Complete! Code processed by AI agent
```

### Trigger Scenarios

**Scenario 1: Direct Code Conversion**
```
User says: "Convert repo to JSON" or "Generate code instructions"
    ↓
generator is triggered
    ↓
Generates JSON structured template
    ↓
Pass JSON to AI agent for execution
```

**Scenario 2: Large Codebase - Batch Processing**
```
User says: "Convert entire project to JSON" or "Generate batch JSON"
    ↓
generator detects large codebase (>50 files)
    ↓
Automatically splits into batches:
    ├─ Batch 1: Configuration files (*.json, *.yaml, *.toml)
    ├─ Batch 2: Frontend code (src/*.vue, src/*.js)
    └─ Batch 3: Backend code (api/*.py, models/*.py)
    ↓
Each batch sent to AI agent sequentially
```

**Scenario 3: Incremental Update**
```
User says: "只更新改动的文件" or "Sync only changed files"
    ↓
generator uses sync command with specific commit
    ├─ Get changed files from commit
    └─ Generate JSON for only modified files
    ↓
Send to AI agent
```

---

# 🔄 Two-Skill Collaboration Architecture

## Overview

This skill (`generator`) **works together with** `miaoda-app-builder` in a **two-step workflow**:

```
┌─────────────────────┐         ┌──────────────────────┐
│  repo-json-         │  JSON   │  miaoda-app-         │
│  generator          │ ──────> │  builder             │
│                     │  Code   │                      │
│  1. Fetch from      │  Data   │  2. Update Code      │
│     Git             │         │     via Chat API     │
│  3. Generate JSON   │         │  3. Create/Overwrite │
│     Instructions    │         │     Files            │
└─────────────────────┘         └──────────────────────┘
```

## Why Two Skills?

| Aspect | Using Only `miaoda-app-builder` | Two-Skill Collaboration |
|--------|--------------------------------|------------------------|
| **Accuracy** | 70-80% (natural language) | 90-95% (structured JSON) |
| **File Completeness** | May miss files | Guaranteed by JSON structure |
| **Control** | Hard to verify | Easy to validate before sync |
| **Batch Processing** | Difficult | Built-in support |
| **Best For** | Small edits, UI tweaks | Full sync, large updates |

## Collaboration Workflow

### Standard Flow

```
User Request
    ↓
"Sync code from GitHub" / "Update with latest code"
    ↓
Step 1: generator
    ├─ Clone repository from Git
    ├─ Read all code files
    ├─ Generate structured JSON instructions
    └─ Output: JSON data with file contents
    ↓
Step 2: miaoda-app-builder
    ├─ Receive JSON instructions via chat
    ├─ Parse file list and contents
    ├─ Create/overwrite each file
    └─ Output: Updated file list for verification
    ↓
Complete! Code synced to Miaoda platform
```

### Trigger Scenarios

**Scenario 1: Direct Sync Command**
```
User says: "用秒哒更新代码" or "Sync code from GitHub"
    ↓
generator is triggered
    ↓
Generates JSON structured template
    ↓
Pass JSON to miaoda-app-builder for execution
```

**Scenario 2: Large Codebase - Batch Processing**
```
User says: "同步整个项目代码" or "Update entire project"
    ↓
generator detects large codebase (>50 files)
    ↓
Automatically splits into batches:
    ├─ Batch 1: Configuration files (*.json, *.yaml, *.toml)
    ├─ Batch 2: Frontend code (src/*.vue, src/*.js)
    └─ Batch 3: Backend code (api/*.py, models/*.py)
    ↓
Each batch sent to miaoda-app-builder sequentially
```

**Scenario 3: Incremental Update**
```
User says: "只更新改动的文件" or "Sync only changed files"
    ↓
generator uses sync command with commit filter
    ├─ Find specific commit with changed files
    └─ Generate JSON for only those files
    ↓
Send to miaoda-app-builder
```

---

# Structured JSON Template Format

## Standard Template

When `generator` processes code from a Git repository, it generates the following JSON structure:

```
{
  "action": "CREATE_OR_UPDATE_FILES",
  "description": "Please create or update all files in the project according to the following JSON data",
  "source": {
    "repository": "https://github.com/username/repo",
    "branch": "main",
    "commit": "abc123def456"
  },
  "summary": {
    "files_changed": 3,
    "total_additions": 131,
    "total_deletions": 98,
    "files": [
      {
        "path": "src/file.ts",
        "status": "modified",
        "additions": 10,
        "deletions": 5
      }
    ]
  },
  "rules": [
    "1. MUST update ALL files in the files array - no exceptions",
    "2. MUST copy content EXACTLY as-is - no modifications, no reformatting, no 'improvements'",
    "3. MUST preserve ALL whitespace, newlines, indentation, and comments exactly",
    "4. MUST use EXACT file paths from path field - no path transformation",
    "5. If file exists: overwrite completely (NOT merge)",
    "6. If file does not exist: create it",
    "7. After updating: output complete list of all updated files (format: 1. /path/to/file)",
    "8. DO NOT ask for confirmation - just execute",
    "9. DO NOT use Git commands - file operations only",
    "10. DO NOT skip any file for any reason"
  ],
  "files": [
    {
      "path": "package.json",
      "status": "modified",
      "additions": 2,
      "deletions": 1,
      "changes": [
        { "type": "addition", "line": 5, "content": "..." }
      ],
      "action": "CREATE_OR_OVERWRITE",
      "content": "{\n  \"name\": \"my-app\",\n  ...\n}"
    },
    {
      "path": "src/App.vue",
      "status": "added",
      "additions": 50,
      "deletions": 0,
      "changes": [
        { "type": "addition", "line": 50, "content": "..." }
      ],
      "action": "CREATE_OR_OVERWRITE",
      "content": "<template>\n  ...\n</template>"
    }
  ]
}
```

## Template Components

| Field | Type | Description |
|-------|------|-------------|
| `action` | String | Always "CREATE_OR_UPDATE_FILES" |
| `description` | String | Human-readable instruction |
| `source` | Object | Git source information for traceability |
| `source.repository` | String | Repository URL |
| `source.branch` | String | Git branch name |
| `source.commit` | String | Commit hash |
| `summary` | Object | Change statistics and file list |
| `summary.files_changed` | Number | Total number of changed files |
| `summary.total_additions` | Number | Total lines added |
| `summary.total_deletions` | Number | Total lines deleted |
| `summary.files` | Array | List of changed files with stats |
| `rules` | Array | Execution rules that AI agent must follow |
| `files` | Array | List of files to update |
| `files[].path` | String | Relative file path |
| `files[].status` | String | File status: "added", "modified", or "deleted" |
| `files[].additions` | Number | Lines added in this file |
| `files[].deletions` | Number | Lines deleted in this file |
| `files[].changes` | Array | Detailed diff information (optional) |
| `files[].action` | String | Always "CREATE_OR_OVERWRITE" |
| `files[].content` | String | Complete file content |

## Batch Template Example

For large projects, JSON is split into multiple batches:

**Batch 1: Configuration**
```
{
  "action": "CREATE_OR_UPDATE_FILES",
  "batch": "1/3",
  "description": "Batch 1: Configuration files",
  "files": [
    {"path": "package.json", "action": "CREATE_OR_OVERWRITE", "content": "..."},
    {"path": "tsconfig.json", "action": "CREATE_OR_OVERWRITE", "content": "..."}
  ]
}
```

**Batch 2: Frontend**
```
{
  "action": "CREATE_OR_UPDATE_FILES",
  "batch": "2/3",
  "description": "Batch 2: Frontend source code",
  "files": [
    {"path": "src/App.vue", "action": "CREATE_OR_OVERWRITE", "content": "..."},
    {"path": "src/components/Header.vue", "action": "CREATE_OR_OVERWRITE", "content": "..."}
  ]
}
```

---

# ⚠️ Security & Safety Considerations

## Generated Instructions

This tool intentionally generates imperative instructions in the JSON output for downstream AI agents. This is by design to ensure accurate code synchronization. However:

- **User Responsibility**: Users should ensure that the generated JSON does not carry more authority than their actual intent
- **Review Required**: Always review the generated JSON, especially file lists, action fields, and rules, before passing to other AI agents
- **Downstream Impact**: Downstream AI agents may treat the generated repository JSON as instructions that must be strictly followed

## Repository Content Trust

**Treat Repository Content as Untrusted Data**: 
- Repository file contents are directly placed into the generated JSON
- Files may contain prompt text that could influence downstream AI agents
- Instruct downstream agents to treat file content as data, not instructions
- Review unusual repository files before use

## Credential Security

**GitHub Token Best Practices**:
- Use minimal, read-only tokens scoped to specific repositories
- Tokens are passed via environment variables only
- Tokens are never stored in files or logs
- Token only exists in memory during execution
- Automatically redacted from all output

**Note**: This skill requires sensitive GitHub credentials. Verify publisher, package identifier, and version history before installation or use.

---

# 🔒 Security Mechanisms

## Overview

This tool implements comprehensive security mechanisms to protect sensitive information when working with Git repositories.

## Security Features

### 1. Token Management

**Public Repositories**: No token required, direct clone

**Private Repositories**: Set `GITHUB_TOKEN` environment variable

```bash
export GITHUB_TOKEN="ghp_your_token"
```

**Token Requirements:**
- Only needs `repo` read permission
- Format: `ghp_*`, `gho_*`, `ghu_*`, `ghs_*, or `ghr_*`
- Never store in code or files

**Automatic Detection:**
- Public repos: Direct clone without token
- Private repos: Automatic token injection
- Token only exists in memory during execution

### 2. Sensitive Information Protection

**Automatic Redaction:**
All sensitive data is automatically detected and masked:
- GitHub Tokens: `ghp_*` → `<GITHUB_TOKEN>`
- Slack Tokens: `xox[baprs]-*` → `<SLACK_TOKEN>`
- API Keys: `AIza*` → `<GOOGLE_API_KEY>`
- Passwords: `password=xxx` → `password=<REDACTED>`

**URL Credential Removal:**
```
Input:  https://x-access-token:ghp_abc123@github.com/user/repo.git
Output: https://github.com/user/repo.git
```

Applied to: JSON output, terminal summaries, logs, error messages

### 3. Secure Git Operations

**Non-Interactive Mode:**
```bash
GIT_ASKPASS=echo          # Prevent password prompts
GIT_TERMINAL_PROMPT=0     # Disable terminal prompt
```

**Token Security:**
- ✅ Token passed via URL (not in command-line arguments)
- ✅ Not visible in process list
- ✅ Only exists in memory during execution

### 4. Temporary File Security

**Auto-Cleanup:**
- All temporary directories deleted after execution
- No sensitive data remains on disk
- UUID-based unique names prevent conflicts

**Temporary Locations (Cross-Platform):**

| Platform | Location | Format |
|----------|----------|--------|
| **macOS/Linux** | `/tmp/github-<uuid>/` | `/tmp/github-a1b2c3d4/` |
| **Windows** | `%TEMP%\github-<uuid>\` | `C:\Users\<user>\AppData\Local\Temp\github-a1b2c3d4\` |

**Cleanup Mechanisms:**
- Context manager (`with temp_directory()`)
- `atexit` handler for guaranteed cleanup
- Signal handlers (`SIGTERM`, `SIGINT`)

### 5. Secure Logging & Errors

All log output and error messages are automatically sanitized:

```python
# All sensitive data automatically redacted
logger.info("Cloning with token:", token)  # Shows: <GITHUB_TOKEN>
```

## Security Best Practices

### ✅ DO:

1. Use environment variables for tokens
2. Use minimal permissions (read-only)
3. Rotate tokens regularly
4. Verify output doesn't contain tokens
5. Use .gitignore for sensitive files

### ❌ DON'T:

1. Never hardcode tokens in code
2. Never log token values
3. Never store tokens in plain text files
4. Never commit tokens to Git

## Troubleshooting

### Token Not Working

```bash
# 1. Verify token is set
echo $GITHUB_TOKEN

# 2. Check permissions (GitHub → Settings → Developer settings)

# 3. Test manually
git ls-remote https://x-access-token:$GITHUB_TOKEN@github.com/user/repo.git
```

### Permission Denied

```bash
# Ensure non-interactive mode
export GIT_TERMINAL_PROMPT=0
```

---

# 📁 Temporary Clone Locations

When this tool runs, it temporarily clones repositories to process code. All directories are automatically cleaned up after execution.

## Clone Paths (Cross-Platform)

The tool uses system temporary directory via `tempfile.gettempdir()`:

| Platform | Location | Format |
|----------|----------|--------|
| **macOS/Linux** | `/tmp/github-<uuid>/` | `/tmp/github-a1b2c3d4/` |
| **Windows** | `%TEMP%\github-<uuid>\` | `C:\Users\<user>\AppData\Local\Temp\github-a1b2c3d4\` |

## Quick Notes

- ✅ **Auto-cleanup**: All temporary directories are removed after script finishes
- ✅ **Unique names**: UUID-based directory names prevent conflicts
- ✅ **Security**: No sensitive data remains on disk after execution
- ✅ **Guaranteed cleanup**: Uses context manager, atexit handler, and signal handlers

## Cleanup Mechanisms

1. **Context Manager**: `with temp_directory()` ensures cleanup on exit
2. **Atexit Handler**: Registered to clean up on normal program exit
3. **Signal Handlers**: Catches `SIGTERM` and `SIGINT` for cleanup on interruption

---

# How to Trigger Code Generation

## User Commands

When users say any of the following, trigger `generator`:

### Chinese Commands
- "生成 JSON 指令"
- "转换代码为 JSON"
- "从 Git 仓库生成指令"
- "批量生成代码指令"
- "导出代码到 JSON"
- "查看 commit 信息"
- "获取代码变更"

### English Commands
- "Generate JSON instructions"
- "Convert code to JSON"
- "Generate from Git repository"
- "Batch generate code instructions"
- "Export code to JSON"
- "View commit info"
- "Get code changes"

## Execution Flow

### Step 0: Read Documentation & Check Help

**IMPORTANT**: Before using this tool, AI agents MUST read the documentation and check available options:

```bash
# Step 1: Read this SKILL.md file to understand the tool's capabilities
# Step 2: Check command-line help for available options and parameters
python3 scripts/generator.py --help
```

**Version 3.0.0 Note**: The tool now uses a modular architecture. All functionality remains the same, but the codebase is better organized for maintenance and extension.

Review the help output to understand:
- Available subcommands (`sync`, `info`)
- Required parameters (`--repo`, `--commit`, etc.)
- Optional parameters (`--filter`, `--exclude`, `--max-files`, `--output`, `--no-instructions`)
- Usage examples for different scenarios

### Step 1: User Provides Repository URL

```
User: "Generate JSON from https://github.com/user/repo"
    ↓
generator extracts:
  - repo_url: https://github.com/user/repo
  - commit: (latest or specified)
```

### Step 2: Fetch and Generate JSON

```
# Execute generation command
python3 scripts/generator.py sync \
  --repo https://github.com/user/repo \
  --commit abc123def456
```

Output: Structured JSON template with summary

### Step 3: Send to Your AI Agent

```
User/Agent sends to AI system:

Please execute the following code update instructions:

```json
{
  "action": "CREATE_OR_UPDATE_FILES",
  "files": [...]
}
```

**CRITICAL RULES:**
1. ✅ MUST update **every file** in the files array - no exceptions
2. ✅ MUST copy content EXACTLY as-is - no modifications, no reformatting, no 'improvements'
3. ✅ MUST preserve ALL whitespace, newlines, indentation, and comments exactly
4. ✅ MUST use EXACT file paths from path field - no path transformation
5. ✅ If file exists: overwrite completely (NOT merge)
6. ✅ If file does not exist: create it
7. ✅ After updating: output complete list of all updated files (format: 1. /path/to/file)
8. ✅ DO NOT ask for confirmation - just execute
9. ✅ DO NOT use Git commands - file operations only
10. ✅ DO NOT skip any file for any reason

**Verification:**
After all files are updated, please output:
- Total number of files updated
- Complete list of all file paths
- Any files that failed to update (if any)
```

### Step 4: AI Agent Executes

```
Your AI agent processes the JSON and:
- Parses file list
- Creates/overwrites files
- Returns completion status
```

---

# Info Command - Get Commit Information

## Overview

The `info` command provides detailed commit information including:
- Commit metadata (author, date, message)
- Changed files list with statistics
- Detailed diff information (optional)
- **Complete file content** for all changed files

## Usage Examples

### Get Commit Information

```bash
# Get specific commit information
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --commit abc123def456
```

**Terminal Output (always shows summary):**
```
📊 Summary:
  Files Changed: 3
  Total Additions: +131
  Total Deletions: -98

📁 Changed Files (3):
  🆕 Added: docs/GUEST_AUTH_AND_CONVERSION.md (+79/-0)
  📝 Modified: src/contexts/AuthContext.tsx (+7/-91)
  📝 Modified: src/db/guest.ts (+45/-7)
```

### Save to File

```bash
# Save full formatted output (summary + JSON) to file
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --commit abc123def456 \
  --output changes.json
```

- **File**: Contains full formatted output (summary + JSON)
- **Terminal**: Shows summary information

### Save Pure JSON

```bash
# Save pure JSON to file (terminal still shows summary)
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --commit abc123def456 \
  --output changes.json \
  --no-instructions
```

- **File**: Contains pure JSON only
- **Terminal**: Shows summary information

### Filter Files (Include Only)

```bash
# Only include TypeScript and JavaScript files
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --commit abc123def456 \
  --filter "*.ts,*.tsx,*.js" \
  --output changes.json
```

- **Effect**: Only files matching the patterns are included in the output
- **Terminal**: Shows filtered file count and list

### Exclude Files

```bash
# Exclude documentation and test files
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --commit abc123def456 \
  --exclude "*.md,*.txt,**/test/**,**/spec/**" \
  --output changes.json
```

- **Effect**: Files matching the patterns are excluded from the output
- **Terminal**: Shows ⏭️ indicator for filtered out files

### Combine Include and Exclude Filters

```bash
# Include Python files but exclude test files
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --commit abc123def456 \
  --filter "*.py" \
  --exclude "*.test.py,*.spec.py" \
  --output changes.json
```

- **Effect**: First applies include filter, then applies exclude filter
- **Use Case**: Focus on source code while excluding tests, mocks, etc.

## JSON Structure

The `info` command generates a comprehensive JSON structure:

```json
{
  "action": "CREATE_OR_UPDATE_FILES",
  "description": "Please create or update all files...",
  "source": {
    "repository": "https://github.com/user/repo",
    "branch": "main",
    "commit": "abc123def456"
  },
  "summary": {
    "files_changed": 3,
    "total_additions": 131,
    "total_deletions": 98,
    "files": [
      {
        "path": "src/file.ts",
        "status": "modified",
        "additions": 10,
        "deletions": 5
      }
    ]
  },
  "rules": [...],
  "files": [
    {
      "path": "src/file.ts",
      "status": "modified",
      "additions": 10,
      "deletions": 5,
      "changes": [
        { "type": "deletion", "line": 10, "content": "old code" },
        { "type": "addition", "line": 10, "content": "new code" }
      ],
      "content": "// Complete file content here..."
    }
  ]
}
```

## Output Behavior Summary

| Scenario | Terminal | File |
|----------|----------|------|
| No `--output` | Shows summary | Not saved |
| With `--output` | Shows summary | Full formatted (summary + JSON) |
| `--output` + `--no-instructions` | Shows summary | Pure JSON only |

**Key Point**: Terminal **always** displays summary information in all scenarios.

## Filter Syntax

The `--filter` and `--exclude` parameters support various pattern formats:

| Pattern | Description | Example |
|---------|-------------|---------|
| `*.ext` | Match by extension | `*.py`, `*.js`, `*.md` |
| `path/*` | Match all files in directory | `src/*`, `docs/*` |
| `path/*.ext` | Match specific extension in directory | `src/*.py`, `test/*.js` |
| Multiple patterns | Comma-separated | `*.py,*.js,*.ts` |

**Filtering Priority:**
1. Include filter (`--filter`) is applied first
2. Exclude filter (`--exclude`) is applied second
3. If both are specified, files must match include AND not match exclude

---

# How to Trigger Code Sync

## User Commands

When users say any of the following, trigger `generator`:

### Chinese Commands
- "用秒哒更新代码"
- "同步 GitHub 代码"
- "从 GitHub 拉取代码"
- "更新项目代码"
- "同步整个项目"
- "只更新改动的文件"
- "批量同步代码"

### English Commands
- "Sync code from GitHub"
- "Update with latest code"
- "Pull code from GitHub"
- "Sync my repository"
- "Update entire project"
- "Sync only changed files"
- "Batch sync code"

## Execution Flow

### Step 1: User Provides Repository URL

```
User: "用秒哒更新代码，仓库地址是 https://github.com/user/repo"
    ↓
generator extracts:
  - repo_url: https://github.com/user/repo
  - app_id: (from current context)
  - context_id: (from current context)
```

### Step 2: Fetch and Generate JSON

```bash
# Execute generation command
python3 scripts/generator.py sync \
  --repo https://github.com/user/repo \
  --commit abc123def456
```

Output: Structured JSON template

### Step 3: Send to miaoda-app-builder

```
User/Agent sends to miaoda-app-builder chat:

Please execute the following code update instructions:

```json
{
  "action": "UPDATE_ALL_FILES",
  "files": [...]
}
```

Important rules:
- Update every file in the files array
- Match content exactly as specified in content field
- Do not modify, alter, or skip any code
- Output complete list of all updated files when done
```

### Step 4: miaoda-app-builder Executes

```bash
# miaoda-app-builder processes via chat API
python3 scripts/miaoda_api.py chat \
  --text "<JSON instructions from Step 3>" \
  --app-id <app_id> \
  --context-id <context_id>
```

---

# Batch Processing Strategy

## Automatic Splitting

When codebase exceeds thresholds, `generator` automatically suggests batch processing:

### Split Criteria

| Condition | Action |
|-----------|--------|
| Files > 50 | Recommend splitting |
| Total size > 5MB | Recommend splitting |
| Mixed file types | Split by category |

### Recommended Batch Categories

**Priority 1: Configuration Files** (Must sync first)
```bash
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --filter "*.json,*.yaml,*.yml,*.toml,*.env,package.json,requirements.txt" \
  --max-files 20 \
  --output batch1_config.json
```

**Priority 2: Frontend Code**
```bash
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --filter "src/*.vue,src/*.js,src/*.jsx,src/*.ts,src/*.tsx,src/*.css,src/*.scss,src/*.html" \
  --max-files 30 \
  --output batch2_frontend.json
```

**Priority 3: Backend Code**
```bash
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --filter "api/*.py,models/*.py,controllers/*.py,services/*.py,utils/*.py" \
  --max-files 30 \
  --output batch3_backend.json
```

**Priority 4: Documentation & Others**
```bash
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --filter "*.md,*.txt,README*,docs/*" \
  --max-files 10 \
  --output batch4_docs.json
```

### Batch Execution Order

1. **Send Batch 1** to AI agent
2. **Wait for completion** and verify file list
3. **Send Batch 2** to AI agent
4. **Repeat** until all batches complete
5. **Final verification** - check all files synced

---

# Workflow Examples

## Example 1: Simple JSON Generation (Public Repository)

```bash
# Step 0: Check help to understand available options
python3 scripts/generator.py --help

# Step 1: Use generator to fetch code
export GITHUB_TOKEN="ghp_your_token"
python3 scripts/generator.py sync \
  --repo https://github.com/username/my-project \
  --commit abc123def456

# Step 2: Copy the JSON output
# [Output contains structured JSON template]

# Step 3: Send JSON to your AI agent
# Pass the JSON to your AI agent/automation tool
```

---

## Example 2: Large Project with Batches

```bash
# Step 0: Check help first
python3 scripts/generator.py --help

# Batch 1: Configuration
python3 scripts/generator.py sync \
  --repo https://github.com/username/large-project \
  --filter "*.json,*.yaml,*.toml,*.env" \
  --max-files 20 \
  --output batch1.json

# Send to AI agent
# Process batch1.json with your AI system

# Wait for completion, then Batch 2: Frontend
python3 scripts/generator.py sync \
  --repo https://github.com/username/large-project \
  --filter "src/*.vue,src/*.js,src/*.css" \
  --max-files 30 \
  --output batch2.json

# Send to AI agent
# Process batch2.json with your AI system

# Batch 3: Backend
python3 scripts/generator.py sync \
  --repo https://github.com/username/large-project \
  --filter "api/*.py,models/*.py" \
  --max-files 30 \
  --output batch3.json

# Send to AI agent
# Process batch3.json with your AI system
```

---

# AI Agent Integration Guide

## Message Format for AI Agents

When sending JSON to an AI agent, use this format:

```
Please execute the following code update instructions:

```json
{
  "action": "UPDATE_ALL_FILES",
  "files": [...]
}
```

**CRITICAL RULES:**
1. ✅ You must update **every file** in the files array
2. ✅ File content must match the `content` field **exactly**
3. ✅ Do not modify, alter, optimize, or reformat any code
4. ✅ Create file if it doesn't exist, completely overwrite if it exists
5. ✅ Do not skip any file from the list
6. ✅ Preserve the exact file structure and paths
7. ✅ After updating, output a **complete list** of all updated files for verification

**Verification:**
After all files are updated, please output:
- Total number of files updated
- Complete list of all file paths
- Any files that failed to update (if any)
```

## Verification After Processing

After AI agent completes:

1. **Check file count**: Compare with original JSON `files.length`
2. **Verify file list**: All paths should match
3. **Review application**: Test the updated code
4. **Test functionality**: Run key features
5. **Deploy if successful**: Follow your deployment process

---

# Error Handling & Optimization

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Files missing after sync | AI skipped some files | Use JSON template with strict rules |
| Code modified/altered | AI tried to "improve" code | Emphasize "DO NOT MODIFY" in rules |
| Sync incomplete | Too many files at once | Use batch processing |
| Token limit exceeded | JSON too large | Split into smaller batches |
| Private repo access denied | Missing token | Provide GITHUB_TOKEN |

## Optimization Strategies

### 1. Prioritize Critical Files
```bash
# Sync config files first (affects entire app)
--filter "package.json,requirements.txt,*.yaml,*.toml"
```

### 2. Use Commit Hashes for Reproducibility
```bash
# Pin to specific commit
--commit abc123def456
```

### 3. Exclude Unnecessary Files
```bash
# Only sync source code, skip docs/tests
--filter "src/*,api/*,models/*"
```

### 4. Parallel Batch Processing (Advanced)
For independent batches, you can prepare all JSON files first, then send sequentially:

```bash
# Prepare all batches
python3 scripts/generator.py sync --repo <url> --filter "*.json" --output batch1.json
python3 scripts/generator.py sync --repo <url> --filter "src/*.vue" --output batch2.json
python3 scripts/generator.py sync --repo <url> --filter "api/*.py" --output batch3.json

# Send to AI agent one by one
# (Must wait for each to complete before sending next)
```

---

# Limitations & Workarounds

## Current Constraints

1. **File Limit**: Recommended <50 files per batch (AI processing limits)
2. **File Size**: Individual files >100KB may cause issues
3. **Binary Files**: Not supported (images, fonts, executables)
4. **No Direct Upload**: Must go through miaoda-app-builder chat API
5. **AI Accuracy**: ~90-95% with JSON instructions (vs 70-80% with natural language)

## Best Practices

✅ **DO:**
- Use structured JSON templates (this skill's output)
- Batch large projects by file type
- Verify file count after each sync
- Use specific commit hashes for reproducibility
- Sync configuration files first

❌ **DON'T:**
- Send >50 files in one batch
- Include binary files in sync
- Skip verification step
- Use natural language for code updates (use JSON instead)
- Modify JSON content before sending to miaoda-app-builder

---
