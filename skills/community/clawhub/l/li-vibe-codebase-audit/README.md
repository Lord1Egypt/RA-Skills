# 🔒 Vibe Codebase Audit Skill

Multi-agent security auditing for AI-generated codebases.

## 📦 Installation

### For OpenCode

```bash
# Skill is already installed at:
# ~/.config/opencode/skills/li_vibe_codebase-audit/
```

### For Hermes

```bash
# Add to Hermes plugins directory
cp -r ~/.config/opencode/skills/li_vibe_codebase-audit /path/to/hermes/plugins/
```

### For OpenClaw

```python
# Import directly in your OpenClaw workflow
import sys
sys.path.append('~/.config/opencode/skills/li_vibe_codebase-audit')
from vibe_audit_tools import vibe_audit_scan, vibe_audit_full
```

## 🚀 Quick Start

### Tool 1: Automated Scan

```python
# Fast local security scan
result = vibe_audit_scan("/path/to/project")
print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']}/100")
```

### Tool 2: Multi-Model AI Audit

```python
# Set OpenRouter API key first
import os
os.environ['OPENROUTER_API_KEY'] = 'sk-or-v1-...'

# Run multi-model consensus audit
result = vibe_audit_multi_model("/path/to/project")
print(f"Private Data Found: {result['private_data_found']}")
print(f"Safe to Publish: {result['consensus_publish_recommendation']}")
```

### Tool 3: Complete Workflow

```python
# Automated scan + multi-model audit
result = vibe_audit_full("/path/to/project")
print(f"Safe to Publish: {result['workflow_recommendation']['safe_to_publish']}")
for fix in result.get('fix_suggestions', []):
    print(f"Fix: {fix['suggestion']}")
```

## 🛠️ Available Tools

| Tool | Speed | Accuracy | Best For |
|------|-------|----------|----------|
| `vibe_audit_scan` | Fast (seconds) | Pattern-based | Quick checks, CI/CD |
| `vibe_audit_multi_model` | Slower (minutes) | AI-powered | Pre-publish validation |
| `vibe_audit_full` | Comprehensive | Both methods | Complete workflow |

## 📋 What It Detects

- ✅ API keys and secrets
- ✅ Personal data (emails, phones, paths)
- ✅ Security vulnerabilities
- ✅ Obsidian vault references
- ✅ Code quality issues

## 🔧 Configuration

```bash
# Required for multi-model audit
export OPENROUTER_API_KEY="sk-or-v1-..."

# Optional
export VIBE_AUDIT_VERBOSE=true
export VIBE_AUDIT_MAX_FILE_SIZE=1000000
```

## 📖 Documentation

See `SKILL.md` for comprehensive documentation.

## 🤝 Supported Agents

- ✅ OpenCode (native skill)
- ✅ Hermes (plugin)
- ✅ OpenClaw (module)
- ✅ Generic MCP clients

## 📜 License

MIT License
