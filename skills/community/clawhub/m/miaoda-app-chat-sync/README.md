# Repo JSON Generator
[![Version](https://img.shields.io/badge/version-3.2.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Convert Git repository code to structured JSON instructions for AI agents and automation tools.

## 📋 Overview

**Repo JSON Generator** fetches code from Git repositories (GitHub, GitLab, Bitbucket, etc.) and generates **structured JSON instructions** that can be consumed by any AI agent or automation system for accurate code processing and updates.

### Key Features

- ✅ **High Accuracy**: 90-95% accuracy with structured JSON (vs 70-80% with natural language)
- ✅ **Modular Architecture**: Clean, maintainable codebase with independent modules
- ✅ **Batch Processing**: Automatic splitting for large projects (>50 files)
- ✅ **File Filtering**: Include/exclude files by pattern (`--filter`, `--exclude`)
- ✅ **Multiple Commands**: `sync` for code sync, `info` for commit information
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux
- ✅ **Zero Dependencies**: Only requires Python 3.8+ and Git
- ✅ **Security Features**: Includes token protection, automatic cleanup, and sensitive data redaction

### Why Structured JSON?

| Aspect | Natural Language | Structured JSON |
|--------|------------------|-----------------|
| **Accuracy** | 70-80% | 90-95% |
| **File Completeness** | May miss files | Guaranteed by JSON structure |
| **Control** | Hard to verify | Easy to validate before processing |
| **Batch Processing** | Difficult | Built-in support |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Git** (installed and in PATH)
- **GitHub Token** (for private repositories, optional)

### Installation

No installation required! Just clone or download this repository.

```bash
# Clone or download this repository
cd miaoda-app-chat-sync
```

### Basic Usage

#### 1. Generate JSON Instructions (Sync Command)

```bash
# Basic sync - generate JSON for entire repository
python3 scripts/generator.py sync \
  --repo https://github.com/username/my-project \
  --branch main \
  --commit abc123def456
```

#### 2. Get Commit Information (Info Command)

```bash
# Get detailed commit information with file contents
python3 scripts/generator.py info \
  --repo https://github.com/username/my-project \
  --branch main \
  --commit abc123def456
```

#### 3. Check Help

```bash
# View all available commands and options
python3 scripts/generator.py --help
```

---

## 📖 Command Reference

### `sync` Command

Generate structured JSON instructions for code synchronization.

#### Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--repo` | Git repository URL | `https://github.com/user/repo` |
| `--branch` | Branch name (required) | `main`, `master`, `develop` |
| `--commit` | Commit hash (optional, defaults to latest) | `abc123def456` |

#### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--filter` | Include only files matching patterns | All files |
| `--exclude` | Exclude files matching patterns | None |
| `--max-files` | Maximum number of files to process | 50 |
| `--output` | Save output to file | Terminal only |
| `--no-instructions` | Output pure JSON (no formatted instructions) | Show instructions |

#### Examples

```bash
# Sync specific files (Python and JavaScript)
python3 scripts/generator.py sync \
  --repo https://github.com/user/repo \
  --branch main \
  --filter "*.py,*.js" \
  --max-files 30 \
  --output sync_output.json

# Exclude test and documentation files
python3 scripts/generator.py sync \
  --repo https://github.com/user/repo \
  --branch main \
  --exclude "*.md,test/*,docs/*" \
  --output sync_output.json
```

---

### `info` Command

Get detailed commit information including changed files and their contents.

#### Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--repo` | Git repository URL | `https://github.com/user/repo` |
| `--branch` | Branch name (required) | `main`, `master`, `develop` |

#### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--commit` | Specific commit hash | Latest commit |
| `--filter` | Include only files matching patterns | All files |
| `--exclude` | Exclude files matching patterns | None |
| `--output` | Save output to file | Terminal only |
| `--no-instructions` | Save pure JSON to file | Formatted output |

#### Examples

```
# Get commit info with full file contents
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --branch main \
  --commit abc123def456

# Save to file (formatted output)
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --branch main \
  --commit abc123def456 \
  --output changes.json

# Save pure JSON only
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --branch main \
  --commit abc123def456 \
  --output changes.json \
  --no-instructions

# Filter specific file types
python3 scripts/generator.py info \
  --repo https://github.com/user/repo \
  --branch main \
  --commit abc123def456 \
  --filter "*.ts,*.tsx" \
  --output changes.json
```

#### Output Behavior

| Scenario | Terminal | File |
|----------|----------|------|
| No `--output` | Shows summary | Not saved |
| With `--output` | Shows summary | Full formatted (summary + JSON) |
| `--output` + `--no-instructions` | Shows summary | Pure JSON only |

**Note**: Terminal **always** displays summary information in all scenarios.

---

## 🏗️ Architecture (v3.2.0)

### Modular Structure

```
scripts/
├── generator.py              # Main entry point (CLI router)
├── core/
│   ├── constants.py          # Shared constants and configuration
│   ├── temp_manager.py       # Cross-platform temp directory management
│   ├── circuit_breaker.py    # Circuit breaker & retry mechanism
│   ├── security.py           # Sensitive information protection
│   └── prompts.py            # Prompt configuration management
├── git/
│   └── repository.py         # Git repository operations
└── processors/
    ├── file_processor.py     # File reading and filtering
    └── instruction_gen.py    # JSON instruction generation
```

### Module Dependencies

```
core/ (no dependencies)
  ↓
git/ (depends on core)
  ↓
processors/ (depends on core, git)
  ↓
generator.py (depends on all modules)
```

### Architecture Improvements in v3.2.0

- **Removed streaming.py**: Stream output module removed as it was unused
- **Simplified dependencies**: Cleaner module structure with only actively used components
- **Enhanced maintainability**: Reduced code complexity by ~320 lines of dead code

### Benefits

- **Maintainability**: Each module can be updated independently
- **Testability**: Modules can be tested in isolation
- **Reusability**: Core components can be reused in other projects
- **Readability**: Smaller, focused files are easier to understand

---

## 🔄 AI Agent Integration

### Workflow

```
User Request
    ↓
"Generate JSON from Git repo"
    ↓
Step 1: repo-json-generator
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

### JSON Template Format

``json
{
  "action": "CREATE_OR_UPDATE_FILES",
  "description": "Please create or update all files...",
  "source": {
    "repository": "https://github.com/username/repo",
    "branch": "main",
    "commit": "abc123def456"
  },
  "summary": {
    "files_changed": 3,
    "total_additions": 131,
    "total_deletions": 98,
    "files": [...]
  },
  "rules": [
    "1. MUST update ALL files in the files array",
    "2. MUST copy content EXACTLY as-is",
    "3. MUST preserve ALL whitespace and formatting"
  ],
  "files": [
    {
      "path": "src/file.ts",
      "status": "modified",
      "action": "CREATE_OR_OVERWRITE",
      "content": "// File content..."
    }
  ]
}
```

### Integration with Miaoda Platform

This tool works together with `miaoda-app-builder` in a two-step workflow:

1. **repo-json-generator**: Fetches code and generates JSON instructions
2. **miaoda-app-builder**: Receives JSON and updates code via Chat API

See [SKILL.md](SKILL.md) for detailed integration guides.

---

## 📦 Batch Processing

### Automatic Splitting

When codebase exceeds thresholds, the tool automatically suggests batch processing:

| Condition | Action |
|-----------|--------|
| Files > 50 | Recommend splitting |
| Total size > 5MB | Recommend splitting |
| Mixed file types | Split by category |

### Recommended Batch Strategy

```
# Batch 1: Configuration files
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --branch main \
  --filter "*.json,*.yaml,*.toml" \
  --max-files 20 \
  --output batch1_config.json

# Batch 2: Frontend code
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --branch main \
  --filter "src/*.vue,src/*.js,src/*.ts" \
  --max-files 30 \
  --output batch2_frontend.json

# Batch 3: Backend code
python3 scripts/generator.py sync \
  --repo <repo_url> \
  --branch main \
  --filter "api/*.py,models/*.py" \
  --max-files 30 \
  --output batch3_backend.json
```

### Execution Order

1. Send Batch 1 to AI agent
2. Wait for completion and verify file list
3. Send Batch 2 to AI agent
4. Repeat until all batches complete
5. Final verification - check all files synced

---

## 🔒 Security & Configuration

#### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token (for private repos) | Optional |

**⚠️ Security Note**: This tool requires GitHub credentials for private repositories. Use minimal read-only tokens scoped to specific repositories only.

### Token Setup

**Public Repositories** (No Token Required):
```bash
python3 scripts/generator.py sync --repo https://github.com/user/public-repo
```

**Private Repositories** (Token Required):
```bash
# Step 1: Create token (GitHub → Settings → Developer settings → Personal access tokens)
# Step 2: Set environment variable
export GITHUB_TOKEN="ghp_your_token"
# Step 3: Use the tool
python3 scripts/generator.py sync --repo https://github.com/user/private-repo
```

**Token Requirements:**
- Only needs `repo` read permission
- Format: `ghp_*`, `gho_*`, `ghu_*`, `ghs_*, or `ghr_*`

### Security Mechanisms

**1. Automatic Token Detection**
- Public repos: Direct clone without token
- Private repos: Automatic token injection
- Non-GitHub repos: Token not applied

**2. Sensitive Information Redaction**
All sensitive data automatically detected and masked:
- GitHub Tokens: `ghp_*` → `<GITHUB_TOKEN>`
- API Keys, Passwords, Bearer Tokens: Auto-redacted

**3. URL Credential Removal**
All URLs in output automatically cleaned:
```
Input:  https://x-access-token:ghp_abc123@github.com/user/repo.git
Output: https://github.com/user/repo.git
```

**4. Secure Git Operations**
- Non-interactive mode (`GIT_TERMINAL_PROMPT=0`)
- Token via URL (not in command-line args)
- Not visible in process list

**5. Temporary File Security (Cross-Platform)**
- Auto-cleanup after execution
- No sensitive data remains on disk
- UUID-based unique directory names

**Temporary Locations:**
| Platform | Location | Example |
|----------|----------|---------|
| macOS/Linux | `/tmp/github-<uuid>/` | `/tmp/github-a1b2c3d4/` |
| Windows | `%TEMP%\github-<uuid>\` | `C:\Users\user\AppData\Local\Temp\github-a1b2c3d4\` |

**Cleanup Mechanisms:**
- Context manager (`with temp_directory()`)
- `atexit` handler for guaranteed cleanup
- Signal handlers (`SIGTERM`, `SIGINT`)

---

## 📁 Temporary Files

### Clone Locations (Cross-Platform)

The tool uses system temporary directory with UUID-based names:

| Platform | Location | Example |
|----------|----------|---------|
| **macOS/Linux** | `/tmp/github-<uuid>/` | `/tmp/github-a1b2c3d4/` |
| **Windows** | `%TEMP%\github-<uuid>\` | `C:\Users\<user>\AppData\Local\Temp\github-a1b2c3d4\` |

### Quick Notes

- ✅ **Auto-cleanup**: All temporary directories are removed after script finishes
- ✅ **Unique names**: UUID-based directory names prevent conflicts
- ✅ **Security**: No sensitive data remains on disk after execution
- ✅ **Guaranteed cleanup**: Uses context manager, atexit handler, and signal handlers

---

## ⚠️ Limitations & Constraints

### Current Constraints

| Constraint | Limit | Recommendation |
|------------|-------|----------------|
| Files per batch | <50 files | Use batch processing for larger projects |
| Individual file size | <100KB | Split very large files |
| Binary files | Not supported | Exclude images, fonts, executables |
| AI accuracy | ~90-95% | Always verify after sync |

### Best Practices

✅ **DO:**
- Use structured JSON templates (this tool's output)
- Batch large projects by file type
- Verify file count after each sync
- Use specific commit hashes for reproducibility
- Sync configuration files first

❌ **DON'T:**
- Send >50 files in one batch
- Include binary files in sync
- Skip verification step
- Use natural language for code updates (use JSON instead)
- Modify JSON content before sending to AI agent

---

## ⚠️ Important Security Considerations

### Generated JSON Instructions

**Review Before Use**: The JSON output generated by this tool contains instruction rules that downstream AI agents may interpret as authoritative commands. Always review the generated JSON before passing it to other AI agents or automation systems, especially:

- File lists and paths
- Action fields (`CREATE_OR_UPDATE_FILES`, etc.)
- Rules array contents
- File contents (may contain sensitive data)

### Repository Source Verification

**Trust Your Sources**: This tool fetches code from Git repositories. Only use trusted repository URLs and verify commit hashes when reproducibility is important.

### Downstream Agent Behavior

**AI Agent Interpretation**: When the generated JSON is processed by downstream AI agents, they may:
- Create or overwrite files based on the JSON instructions
- Interpret rules as strict requirements
- Process repository content that could contain prompt injection attempts

**Best Practices**:
1. Always review generated JSON before execution
2. Use specific commit hashes for reproducibility
3. Verify file lists and content before sending to downstream agents
4. Maintain backups or version control for rollback capability
5. Treat repository content as untrusted data

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Files missing after sync | AI skipped some files | Use JSON template with strict rules |
| Code modified/altered | AI tried to "improve" code | Emphasize "DO NOT MODIFY" in rules |
| Sync incomplete | Too many files at once | Use batch processing |
| Token limit exceeded | JSON too large | Split into smaller batches |
| Private repo access denied | Missing token | Provide GITHUB_TOKEN |

---

## 📚 Documentation

- **[SKILL.md](SKILL.md)**: Comprehensive skill documentation with integration guides
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and changes
- **CLI Help**: Run `python3 scripts/generator.py --help` for command reference

---

## 📝 License

This project is part of the Miaoda ecosystem. See project documentation for license information.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Read the SKILL.md documentation
2. Follow the modular architecture
3. Test your changes thoroughly
4. Update documentation if needed
5. Submit a pull request

---

**Version**: 3.2.0  
**Last Updated**: 2026-04-30  
**Python Version**: 3.8+  
**Dependencies**: Python Standard Library + Git