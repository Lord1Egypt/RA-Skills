
# CHANGELOG

## [DEPRECATED - SECURITY RISKS] - 2026-03-28

### ?? DEPRECATION NOTICE

**This skill has been DEPRECATED due to security risks.**

Please use **skill-creator-guide** instead (located in ~/.openclaw/workspace/skills/skill-creator-guide/)

### Security Issues Found

The original skill-creator has **undeclared security risks**:

1. **External Dependency (Not Documented)**
   - Requires 'claude' CLI tool installed on system
   - Registry metadata does not list this requirement
   - Fails silently if CLI not available

2. **External API Calls**
   - Scripts (run_eval.py, improve_description.py) send skill content, test prompts, and evaluation data to external Claude services
   - Data sent under your configured Claude/Anthropic session
   - No control over what data is transmitted

3. **Credential Usage**
   - Uses your Claude/Anthropic session credentials
   - Inherits any API keys or tokens configured for 'claude' CLI
   - No way to use with dry-run mode or mock credentials

4. **File System Pollution**
   - Creates temporary files under .claude/commands in project root
   - Deletes them afterwards, but modifies project directory
   - Risk of conflicts with existing .claude directories

5. **Undeclared Behavior**
   - Registry metadata doesn't mention:
     - 'claude' CLI requirement
     - Python environment requirement
     - Subprocess execution
     - Network/API calls
     - Credential usage
     - Temporary file creation

### Why It's Unsafe for OpenClaw

This skill was designed for Claude.ai's environment where:
- Users have 'claude' CLI installed
- Users are authenticated with Anthropic
- External Claude services are trusted

When ported to OpenClaw, these assumptions break:
- OpenClaw users may not have 'claude' CLI
- Sending skill data to external services is unexpected
- Credential exposure is a security risk
- File system writes outside skill directory are inappropriate

### Recommended Alternative

**Use skill-creator-guide instead:**
- ? OpenClaw-native (no external dependencies)
- ? No API calls or credential usage
- ? No file system writes outside skill directory
- ? Documentation-only (no code execution)
- ? 100% safe to use

### Installation of Safe Version

`powershell
# Safe version is already in your workspace
# Location: ~/.openclaw/workspace/skills/skill-creator-guide/

# It includes:
# - SKILL.md (OpenClaw-native guide)
# - CHANGELOG.md (version history)
# - README.md (security notice)
`

### If You Must Use This Version (Not Recommended)

**Proceed with extreme caution:**

1. **Inspect Code First**
   `powershell
   # Read all Python scripts
   Get-Content ~/.openclaw/skills/skill-creator/scripts/*.py
   `

2. **Run in Isolated Environment**
   - Use isolated VM or container
   - Block network access during testing
   - Use mock 'claude' binary for dry-runs

3. **Review Data Being Sent**
   - Check run_eval.py - what skill content is sent?
   - Check improve_description.py - what evaluation data is sent?
   - Ensure no secrets or sensitive data included

4. **Backup Your Environment**
   - Backup existing .claude directory before use
   - Or run in separate workspace

### Original Source

Rewritten for OpenClaw

### Migration Path

To migrate from this deprecated version to skill-creator-guide:

1. Stop using any Python scripts from this skill
2. Use skill-creator-guide's SKILL.md for reference
3. Follow OpenClaw-native skill creation patterns
4. No code execution required - just documentation

---

**STATUS: DEPRECATED - DO NOT USE FOR NEW PROJECTS**

---


