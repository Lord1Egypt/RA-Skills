# 🛡️ OpenClaw Security Audit Skill

Automatic security checking for external resources before execution.

## Overview

This skill provides automated security audits for:
- GitHub repositories cloned locally
- Skills downloaded from the web
- External scripts and code
- Any untrusted code before execution

## Why This Matters

Malicious actors often disguise malware as legitimate software:
- Fake "tools" that contain trojans
- README claims that don't match actual code
- Executables bundled with suspicious payloads
- Shellcode hidden in text files

This skill catches these patterns **before** you run them.

## Features

### 🔍 File Type Detection
- Identifies high-risk executables (.exe, .bat, .sh, .app)
- Recognizes safe source code (Python, JavaScript, Rust, etc.)
- Flags unknown binary files

### 📄 Content Analysis
- Detects suspicious patterns (base64, shellcode, obfuscation)
- Checks for extremely long single-line files (shellcode payloads)
- Validates README descriptions match actual code

### 🚨 Risk Scoring
- **CRITICAL**: Block immediately - likely malware
- **WARNING**: Review manually - suspicious but not clearly malicious
- **SAFE**: No concerns - normal project structure

## Quick Start

### 1. Install

```bash
# Copy to your skills directory
cp -r security-audit ~/.nvm/versions/node/v22.16.0/lib/node_modules/openclaw/skills/

# Make script executable
chmod +x ~/.nvm/versions/node/v22.16.0/lib/node_modules/openclaw/skills/security-audit/audit.py
```

### 2. Use

```bash
# Audit current directory
python3 audit.py

# Audit with verbose output
python3 audit.py --verbose

# Save report to file
python3 audit.py --output report.txt
```

### 3. Automatic Integration

Add to your workflow after git clone:

```bash
git clone https://github.com/user/repo.git && \
cd repo && \
python3 /path/to/audit.py
```

## Security Checks

### High-Risk File Types

| Extension | Risk | Example |
|-----------|-------|---------|
| `.exe`, `.bat`, `.cmd` | 🔴 Critical | Windows malware |
| `.sh`, `.ps1`, `.vbs` | 🔴 Critical | Script malware |
| `.app`, `.dmg`, `.pkg` | 🔴 Critical | macOS trojans |
| `.dll`, `.so`, `.dylib` | 🔴 Critical | Malicious libraries |

### Safe Source Code

✅ These are safe to review:
- `.py` (Python)
- `.js`, `.ts` (JavaScript/TypeScript)
- `.go` (Go)
- `.rs` (Rust)
- `.java`, `.c`, `.cpp` (Compiled languages)

### Suspicious Patterns

Detects:
- Long base64 strings (>100 chars)
- Shellcode signatures
- `eval()` and `exec()` with long payloads
- Dynamic imports from untrusted sources
- Malware keywords

## Output Examples

### ✅ Safe Project

```
🔍 Scanning: /path/to/project

🛡️ Security Audit: PASSED
==================================================

📊 Summary:
   Total files scanned: 15
   Source code files: 8
   High-risk files: 0
   Suspicious patterns: 0

✅ Source Code Found:
   - main.py
   - utils.js
   - Cargo.toml
   ... and 5 more

==================================================

✅ Safe to Use
Recommendation: No immediate concerns
```

### 🚨 Malware Detected

```
🔍 Scanning: /path/to/suspicious-repo

🚨 Security Audit: BLOCKED
==================================================

📊 Summary:
   Total files scanned: 4
   Source code files: 0
   High-risk files: 1
   Suspicious patterns: 2

🚨 High-Risk Files (Executable):
   - /path/to/suspicious-repo/resolver.exe

🚨 Large Single-Line Files (Potential Shellcode):
   - /path/to/suspicious-repo/icon16.txt

⚠️ Suspicious Patterns Found:
   Pattern: shellcode
     - /path/to/suspicious-repo/icon16.txt:1
   Pattern: [a-zA-Z0-9+/]{100,}={0,2}
     - /path/to/suspicious-repo/icon16.txt:1

🚨 README Mismatch: Claims AI/memory features but no source code found

==================================================

🛑 DO NOT EXECUTE
Recommendation: Delete immediately - this appears to be malware
```

## Real-World Examples

### ClawIntelligentMemory (2026-03-03)

**Claimed**: OpenClaw three-layer memory system

**Actual**: Windows malware

```
🚨 BLOCKED: Malware disguised as OpenClaw memory system

Evidence:
- resolver.exe (Windows PE executable, no source)
- icon16.txt (289KB single-line,疑似 shellcode)
- App.bat (launches resolver.exe with payload)
- README claims "memory system", actual content is malware
```

**Action**: Deleted immediately

## Best Practices

### For Users

1. **Always audit** before running external code
2. **Never trust** executables without source code
3. **Review source** even if audit passes
4. **Use virtual environments** for testing
5. **Check repository** activity and contributors

### For Skill Authors

1. **Provide source code** in clear text
2. **Include accurate README** descriptions
3. **Avoid obfuscation** or minification
4. **Document dependencies** clearly
5. **Use standard file formats**

## Limitations

- **Heuristic-based**: Not a full antivirus replacement
- **False positives**: Large datasets, minified code
- **No runtime analysis**: Only static code analysis
- **Manual review needed**: Final decision requires human judgment

## Contributing

To improve detection:

1. Add new suspicious patterns to `SUSPICIOUS_PATTERNS`
2. Add high-risk extensions to `HIGH_RISK_EXTENSIONS`
3. Tune thresholds in `check_single_line_large_file()`
4. Report false positives to improve heuristics

## License

MIT License - Free to use and modify

## Support

For questions or issues:
- Check `SKILL.md` for detailed usage
- Report bugs to your OpenClaw configuration
- Update patterns for new threats
