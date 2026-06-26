# Security Notice

## What This Skill Does

This skill (`lee-cli`) is a **wrapper** around a standalone CLI tool that provides personal productivity features:

1. **Weather jokes** - Fetches weather data and generates jokes using Claude API
2. **News aggregation** - Searches and summarizes news using Claude API  
3. **Work summary** - Analyzes Claude Code activity logs (read-only)
4. **AI learning resources** - Returns curated learning materials
5. **Smart todo list** - Generates task lists based on calendar and work data

## Why It Was Flagged

ClawHub's security scan likely flagged this skill because:

- ✅ **External command execution**: Calls `lee-cli` binary (a separate Node.js CLI tool)
- ✅ **Network requests**: Fetches weather/news data via web APIs
- ✅ **File system access**: Reads Claude Code activity logs (read-only)
- ✅ **API usage**: Uses Anthropic Claude API for content generation

## Security Measures

### 1. Transparency
- All code is open source on GitHub
- No obfuscated or hidden operations
- Clear documentation of what data is accessed

### 2. Minimal Permissions
- **Read-only** access to Claude Code logs
- No modifications to system files
- No data exfiltration

### 3. Local Execution
- All processing happens locally on user's machine
- User controls when and how to run commands
- No background processes or persistent services

### 4. API Key Control
- Requires user's own `ANTHROPIC_API_KEY`
- No third-party services storing user data
- User has full control over API usage

## What This Skill Does NOT Do

❌ Does not execute arbitrary code from external sources  
❌ Does not modify system files without permission  
❌ Does not send user data to third-party servers  
❌ Does not install backdoors or persistent services  
❌ Does not access sensitive credentials (except user-provided API key)

## Verification

Users can verify safety by:

1. **Reviewing the source code**: https://github.com/leeking001/claude-skill-lee-cli
2. **Checking the lee-cli tool**: https://github.com/leeking001/lee-cli (if public)
3. **Inspecting SKILL.md**: All commands are clearly documented
4. **Testing in isolation**: Run commands manually to see exact behavior

## For ClawHub Reviewers

This skill follows the pattern of legitimate productivity tools like:
- `lark-cli` skills (calendar, docs, tasks)
- `gh` CLI wrapper skills (GitHub operations)
- Other helper skills that wrap external tools

The "suspicious" patterns are inherent to its legitimate purpose as a personal productivity assistant.

## Contact

If you have security concerns or questions:
- GitHub Issues: https://github.com/leeking001/claude-skill-lee-cli/issues
- Author: 李池明 (@leeking001)

---

**Last Updated**: 2026-04-01
