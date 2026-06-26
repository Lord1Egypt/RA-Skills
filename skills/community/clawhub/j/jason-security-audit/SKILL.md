---
name: security-audit
description: "Security audit for external resources (GitHub repos, downloaded skills, files). Detects malicious code, suspicious executables, and content mismatches. Use when: (1) cloning GitHub projects, (2) downloading skills from web, (3) running external code/scripts. Always run before trusting or executing external code."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["python3"], "python": [">=3.8"] },
        "install":
          [
            {
              "id": "default",
              "kind": "none",
              "label": "Python 3.8+ required (usually pre-installed)",
            },
          ],
      },
  }
---

# Security Audit Skill

Automated security checks for external resources before execution.

## When to Use

✅ **ALWAYS use this skill when:**

- Cloning any GitHub repository
- Downloading skills or code from the web
- Running external scripts or code
- Installing new tools from untrusted sources

## Security Checks

### File Type Detection

| File Type | Risk Level | Action |
|------------|-------------|--------|
| `.py`, `.js`, `.ts`, `.go`, `.rs` | ✅ Low | Safe to review |
| `.md`, `.txt`, `.json`, `.yaml` | ✅ Low | Safe to read |
| `.exe`, `.bat`, `.sh`, `.app`, `.msi` | 🔴 High | Block without review |
| Unknown binary files | 🔴 High | Block without review |

### Content Analysis

- **Source Code Present**: ✅ Pass
- **README Matches Content**: ✅ Pass
- **Suspicious Patterns**: Detects:
  - Base64 encoded payloads
  - Shellcode signatures
  - Obfuscated code
  - Network connections in scripts

### Red Flags

🚨 **Immediately alert user if:**

- Executable files without source code
- README claims functionality not present in code
- Extremely long text files (> 50KB with single line)
- Encrypted/obfuscated content
- Direct download links in README (not GitHub releases)

## Usage

```bash
# Audit a directory
cd /path/to/repo
python3 audit.py

# Audit with verbose output
python3 audit.py --verbose

# Export report to file
python3 audit.py --output report.txt
```

## Check Results

### ✅ Safe

```
🛡️ Security Audit: PASSED

All checks passed. This resource appears safe to use.
- Source code: Found
- File types: Normal
- Content: Matches description
- No suspicious patterns detected
```

### ⚠️ Warning

```
⚠️ Security Audit: WARNING

Found minor issues that need review:
- Long line in file.txt (65000+ chars)
- Some files lack comments

Recommended: Review before execution.
```

### 🚨 Critical

```
🚨 Security Audit: BLOCKED

Critical security issues detected:
- Executable file: resolver.exe (NO source code)
- Suspicious payload: icon16.txt (289KB single-line text)
- README mismatch: Claims "memory system" but contains malware

🛑 DO NOT EXECUTE. Delete immediately.
```

## Integration with OpenClaw

This skill can be invoked automatically by OpenClaw when:

1. **Cloning Repos**: Runs after `git clone`
2. **Downloading Skills**: Runs after `clawhub install`
3. **Running External Scripts**: Runs before execution

To enable automatic auditing, add to your workflow:

```bash
# After git clone
git clone <repo-url> && cd <repo> && python3 audit.py

# After clawhub install
clawhub install <skill> && python3 ~/.clawhub/skills/<skill>/audit.py
```

## Security Best Practices

### For Users

1. **Never run** unverified executables
2. **Always review** code before execution
3. **Check file types** in downloaded archives
4. **Verify repository** activity and contributors
5. **Use virtual environments** for testing

### For Skill Authors

1. **Provide source code** in clear text
2. **Include README** that matches functionality
3. **Avoid obfuscation** or encryption
4. **Document dependencies** clearly
5. **Use standard formats** (no custom binaries)

## False Positives

Some safe projects may trigger warnings:

- **Large data files**: Legitimate models, datasets
- **Minified code**: Production JavaScript/CSS
- **Compiled modules**: Native Python extensions

**Review manually** before deciding to block.

## Reference Cases

### ClawIntelligentMemory (2026-03-03)

```
🚨 BLOCKED: Malware disguised as OpenClaw memory system

Evidence:
- resolver.exe (Windows PE executable, no source)
- icon16.txt (289KB single-line,疑似 shellcode)
- App.bat (launches resolver.exe with payload)
- README claims "memory system", actual content is malware

Action: Deleted immediately
```

## Notes

- This is a **basic heuristic** check, not a full antivirus
- Always use human judgment for final decisions
- Report false positives to improve detection
- Keep this skill updated with new threat patterns
