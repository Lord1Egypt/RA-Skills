# Security Documentation - OSNK Trainer Skill

## Overview
This document provides full transparency about the executable shell script (`run.sh`) included in this skill package.

## Script Purpose
`run.sh` is a **simple bash command handler** that processes user natural language commands and routes them to appropriate functions within OpenClaw. It does NOT:
- Execute arbitrary code from external sources
- Download or run unverified executables
- Modify system files outside the workspace
- Access network resources except for optional GitHub fallbacks
- Collect or transmit user data

## What run.sh Does

### Core Functions:
1. **Path Detection**: Automatically detects OpenClaw workspace directory
2. **Command Routing**: Parses user commands and calls appropriate handlers
3. **Question Retrieval**: Fetches questions from local files or optional GitHub backup
4. **Statistics Management**: Stores performance stats locally in JSON format

### Data Storage:
All data is stored **locally** in your workspace:
- `$WORKSPACE/memory/osnk-stats.json` - Performance statistics
- `$WORKSPACE/memory/osnk-progress.json` - Learning progress tracking  
- `$WORKSPACE/memory/osnk-config.json` - User configuration (optional)

### Network Access:
The script only accesses GitHub (`raw.githubusercontent.com`) as a **fallback** when:
- Local question bank files are missing
- Workspace knowledge folder is empty

No other external network requests are made.

## Security Guarantees

### ✅ Safe Operations:
- Only reads markdown files (.md) containing question text
- Writes JSON stats to user's own workspace memory folder
- Uses standard POSIX commands (grep, cat, find, head)
- No sudo/root privileges required
- Runs entirely in sandboxed OpenClaw environment

### ❌ No Dangerous Patterns:
- NO `eval` of user input
- NO dynamic code generation
- NO execution of downloaded content
- NO file system modification outside workspace
- NO environment variable injection vulnerabilities
- NO buffer overflow risks (bash string handling)

## Code Review Summary

### Permission Requirements:
```
Read:  $WORKSPACE/memory/*.json
Write: $WORKSPACE/memory/*.json
Execute: Standard bash built-in commands only
```

### External Dependencies:
| Resource | Purpose | Required? |
|----------|---------|-----------|
| `githubusercontent.com/jrrqd/osnk-question-bank` | Fallback question bank | Optional (only if local files missing) |

## For ClawHub Security Team

If you need additional information or would like to review specific portions of the code:

1. **Full source available at**: `/home/justradr/.npm-global/lib/node_modules/openclaw/skills/osnk-trainer/run.sh`
2. **Test installation**: Install in isolated environment and verify behavior matches documentation
3. **Network monitoring**: Only outbound HTTPS to GitHub, no other connections

## Contact & Verification

This skill was created by @jrrqd for Indonesian Olympiad in Informatics training purposes. Questions or security concerns can be directed through ClawHub support channels.

---

_Last updated: 2026-04-05_
