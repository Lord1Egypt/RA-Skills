# Security Policy

## Overview

This project provides a CLI integration for the Knowfun.io API. It's designed for educational content generation and follows security best practices.

## Legitimate Use

This tool is an **official integration** for the Knowfun.io API platform:
- **Purpose**: Generate educational content (courses, posters, games, films)
- **Authorization**: Requires valid API key from https://knowfun.io/api-platform
- **Scope**: Only interacts with authorized Knowfun.io API endpoints

## Why This Triggers Security Scans

Automated security scanners may flag this code because:

1. **Child Process Execution** - `spawn('bash', ...)` is detected
   - **False Positive**: Script path is hardcoded, not user-controlled
   - See: knowfun.js line 30

2. **Shell Script with curl** - External API calls detected
   - **False Positive**: Only calls official api.knowfun.io endpoints
   - See: scripts/knowfun-cli.sh

3. **Environment Variable for Secrets** - API key from env var
   - **Industry Standard**: This is the recommended secure practice

## Security Guarantees

✅ **No Arbitrary Code Execution**
- Script paths are hardcoded (not user-controlled)
- No eval(), exec(), or dynamic imports
- User input is only used as API parameters

✅ **No Sensitive Data Exposure**
- API keys only sent to official Knowfun.io endpoints (https://api.knowfun.io)
- No logging of credentials
- .gitignore prevents committing secrets

✅ **Input Validation**
- Task types validated (course/poster/game/film only)
- URLs validated before sending to API
- JSON properly escaped in bash script

✅ **Principle of Least Privilege**
- Only accesses what's needed for API calls
- No root/admin privileges required
- No system-level operations

## How to Verify This is Safe

```bash
# 1. Verify only Knowfun.io API is called
grep -r "https://api.knowfun.io" scripts/

# 2. Check no dangerous commands exist
grep -E "(rm -rf|dd if|mkfs|shutdown|reboot|eval)" scripts/
# Should return nothing

# 3. Review the simple architecture
# - knowfun.js: 38 lines, just calls knowfun-cli.sh
# - knowfun-cli.sh: API client using curl
# - No complex dependencies, no obfuscation
```

## Architecture

```
User Command
    ↓
knowfun.js (Node.js)
    ↓
scripts/knowfun-cli.sh (Bash)
    ↓
curl → https://api.knowfun.io
```

## Reporting Security Issues

If you discover a genuine security vulnerability:
- Email: support@knowfun.io
- Include: description, steps to reproduce, potential impact

## License & Contact

- **License**: MIT (fully open source)
- **Official Site**: https://knowfun.io
- **GitHub**: https://github.com/MindStarAI/KnowFun-Skills
