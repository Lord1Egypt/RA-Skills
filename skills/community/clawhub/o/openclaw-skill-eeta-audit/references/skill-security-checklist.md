# OpenClaw Skill Security Checklist

> **Comprehensive Security Evaluation for AI Agent Skills** — Focused on identifying security vulnerabilities, data leakage risks, and permission abuses in OpenClaw Skills.

## Security Philosophy

OpenClaw Skills operate with system-level access (file system, network, shell commands), making security non-negotiable. This checklist provides a structured approach to security vetting.

**Core Principles**:
1. **Principle of Least Privilege** - Skills should only request necessary access
2. **Defense in Depth** - Multiple layers of security validation
3. **Transparency** - All security risks must be disclosed
4. **Zero Trust** - Verify everything, trust nothing by default

---

## Security Zones

### Zone 1: Pre-Installation Check (Critical)

**When**: Before installing any skill

**Duration**: 2-5 minutes

**Purpose**: Identify show-stopping security issues

---

#### T04.1: Command Injection Vulnerabilities

**Check**: Scan for dangerous patterns in `SKILL.md` and `scripts/`

**Dangerous Patterns**:
```bash
# Shell command execution
exec()
eval()
subprocess.run(shell=True)
os.system()
child_process.execSync()
```

**Example Vulnerability**:
```python
# ❌ DANGEROUS - User input in exec
user_url = input("Enter URL: ")
os.system(f"curl {user_url}")  # Command injection!
```

**Example Fix**:
```python
# ✅ SAFE - Use subprocess with args
import subprocess
user_url = input("Enter URL: ")
subprocess.run(["curl", user_url], check=True)  # Safe
```

**Scoring**:
- **Pass (10)**: No dangerous patterns found
- **Fail (0)**: Command injection vulnerability detected

**Action**: Fix vulnerability before installation

---

#### T04.2: Data Leakage Risks

**Check**: Examine how skill handles sensitive data

**Risks**:
- Hardcoded API keys, passwords, tokens
- Logging sensitive information
- Unencrypted data transmission
- Sensitive data in error messages

**Example Vulnerability**:
```yaml
# ❌ DANGEROUS - Hardcoded credentials
api_key: "sk-proj-abc123..."
database_url: "postgresql://user:pass123@..."
```

**Example Fix**:
```yaml
# ✅ SAFE - Environment variables
api_key: "${OPENAI_API_KEY}"
database_url: "${DATABASE_URL}"
```

**Scoring**:
- **Pass (10)**: No data leakage risks
- **Fail (0)**: Sensitive data exposed

**Action**: Remove all hardcoded secrets, use environment variables

---

#### T04.3: Path Traversal Vulnerabilities

**Check**: Validate file path handling

**Dangerous Patterns**:
```python
# ❌ DANGEROUS - Unvalidated paths
user_path = input("Enter file path: ")
with open(user_path, 'r') as f:
    content = f.read()  # Could read /etc/passwd!
```

**Example Fix**:
```python
# ✅ SAFE - Validate and sanitize
import os
from pathlib import Path

SAFE_DIR = "/app/data"
user_path = input("Enter filename: ")

full_path = (Path(SAFE_DIR) / user_path).resolve()
if not str(full_path).startswith(SAFE_DIR):
    raise ValueError("Invalid path")

with open(full_path, 'r') as f:
    content = f.read()
```

**Scoring**:
- **Pass (10)**: Path traversal protection in place
- **Fail (0)**: Path traversal vulnerability

**Action**: Implement path validation

---

#### T04.4: Permission Overreach

**Check**: Validate requested permissions vs. actual needs

**Permission Types**:
- **File System**: Read, Write, Execute
- **Network**: HTTP, TCP, UDP
- **Shell**: Command execution
- **System**: Process control, system info

**Example Overreach**:
```yaml
# ❌ OVERREACH - Skill only needs to read files
permissions:
  filesystem: "read+write+execute"  # Too broad!
```

**Example Fix**:
```yaml
# ✅ MINIMAL - Only what's needed
permissions:
  filesystem: "read"
```

**Scoring**:
- **Pass (10)**: Minimal, justified permissions
- **Partial (5)**: Some overreach
- **Fail (0)**: Excessive or dangerous permissions

**Action**: Restrict permissions to minimum required

---

### Zone 2: Gating Mechanism Check

**When**: After pre-installation check, before activation

**Duration**: 1-2 minutes

**Purpose**: Ensure skill only activates when safe

---

#### T04.5: Tool Availability Check (bins)

**Check**: Verify required tools exist before activation

**Example**:
```yaml
gating:
  bins:
    - ffmpeg  # Required for video processing
    - imagemagick  # Required for image conversion
```

**Validation**:
```bash
# Check if required tools exist
which ffmpeg
which imagemagick
```

**Scoring**:
- **Pass (10)**: All required tools checked and validated
- **Partial (5)**: Some tools unchecked
- **Fail (0)**: No tool validation

**Action**: Add gating for all required external tools

---

#### T04.6: Environment Variable Check (env)

**Check**: Verify required environment variables are set

**Example**:
```yaml
gating:
  env:
    - OPENAI_API_KEY
    - DATABASE_URL
```

**Scoring**:
- **Pass (10)**: All required env vars validated
- **Partial (5)**: Some env vars unchecked
- **Fail (0)**: No env var validation

**Action**: Add gating for all required environment variables

---

#### T04.7: OS Compatibility Check (os)

**Check**: Verify skill works on target OS

**Example**:
```yaml
gating:
  os:
    - "darwin"    # macOS
    - "linux"
    # "windows"  # Excluded - not supported
```

**Scoring**:
- **Pass (10)**: OS compatibility clearly defined and checked
- **Partial (5)**: Basic OS check
- **Fail (0)**: No OS compatibility check

**Action**: Add OS gating if skill has platform dependencies

---

### Zone 3: Runtime Security Check

**When**: During skill execution

**Duration**: Ongoing

**Purpose**: Monitor security during operation

---

#### T04.8: Input Validation

**Check**: All user inputs are validated and sanitized

**Input Types to Validate**:
- File paths
- URLs
- Shell commands
- JSON/XML data
- User-provided code

**Example Validation**:
```python
def validate_url(url: str) -> str:
    """Validate and sanitize URL input"""
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    
    # Only allow http/https
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Only HTTP/HTTPS URLs allowed")
    
    # Block localhost/internal IPs
    if parsed.hostname in ['localhost', '127.0.0.1', '::1']:
        raise ValueError("Internal hosts not allowed")
    
    return url
```

**Scoring**:
- **Pass (10)**: Comprehensive input validation
- **Partial (5)**: Basic validation
- **Fail (0)**: No input validation

**Action**: Add validation for all user inputs

---

#### T04.9: Error Message Safety

**Check**: Error messages don't leak sensitive information

**Dangerous**:
```python
# ❌ DANGEROUS - Leaks file structure
try:
    with open(user_file, 'r') as f:
        data = f.read()
except Exception as e:
    print(f"Error reading file: {e}")  # Leaks path!
    # Output: Error reading file: [Errno 2] No such file: '/etc/passwd'
```

**Safe**:
```python
# ✅ SAFE - Generic error
try:
    with open(user_file, 'r') as f:
        data = f.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Access denied")
except Exception as e:
    print("Error reading file")
    logger.error(f"Error: {e}")  # Log detailed error, show generic to user
```

**Scoring**:
- **Pass (10)**: Safe, generic error messages
- **Partial (5)**: Some information leakage
- **Fail (0)**: Detailed error messages to users

**Action**: Sanitize all error messages shown to users

---

#### T04.10: Resource Cleanup

**Check**: Proper cleanup of resources (files, connections, processes)

**Example**:
```python
# ✅ GOOD - Proper cleanup with context manager
def process_file(filename: str) -> str:
    with open(filename, 'r') as f:  # Auto-closes
        data = f.read()
    return data

# ✅ GOOD - Explicit cleanup
def fetch_data(url: str) -> str:
    import requests
    session = requests.Session()
    try:
        response = session.get(url, timeout=30)
        return response.text
    finally:
        session.close()  # Ensure cleanup
```

**Scoring**:
- **Pass (10)**: All resources properly cleaned up
- **Partial (5)**: Some cleanup issues
- **Fail (0)**: Resource leaks

**Action**: Ensure proper cleanup using context managers or finally blocks

---

### Zone 4: Dependency Security

**When**: Installation and update

**Duration**: 3-5 minutes

**Purpose**: Verify dependencies are secure

---

#### T04.11: Dependency Vulnerability Scan

**Check**: Scan for known vulnerabilities in dependencies

**Tools**:
```bash
# Python
pip-audit
safety check

# Node.js
npm audit
yarn audit

# Go
go mod verify
gosec ./...

# Rust
cargo audit
```

**Scoring**:
- **Pass (10)**: No vulnerabilities
- **Partial (5)**: Minor vulnerabilities, fixable
- **Fail (0)**: Critical or high vulnerabilities

**Action**: Update or replace vulnerable dependencies

---

#### T04.12: Dependency Source Verification

**Check**: Verify dependencies come from trusted sources

**Trusted Sources**:
- Official package registries (PyPI, npm, crates.io)
- Official GitHub repositories with verified signatures
- Vendor-controlled package managers

**Untrusted Sources**:
- Random GitHub repos without verification
- Unofficial mirrors
- Direct download links without checksums

**Scoring**:
- **Pass (10)**: All dependencies from trusted sources
- **Partial (5)**: Some from questionable sources
- **Fail (0)**: Dependencies from untrusted sources

**Action**: Replace with trusted alternatives or vendor

---

### Zone 5: Advanced Security Checks

**When**: For high-risk or production skills

**Duration**: 10-20 minutes

**Purpose**: Deep security analysis

---

#### T04.13: Code Obfuscation Check

**Check**: Identify obfuscated or suspicious code

**Warning Signs**:
- Base64-encoded strings in code
- Compressed/minified code
- Unusual character encoding
- Anti-debugging techniques

**Example Suspicious Code**:
```python
# ❌ SUSPICIOUS - Base64 encoded
import base64
cmd = base64.b64decode("Y3VybCBodHRwOi8vZXZpbC5jb20v...").decode()
os.system(cmd)  # What is this doing?
```

**Scoring**:
- **Pass (10)**: No obfuscation
- **Fail (0)**: Obfuscated or suspicious code found

**Action**: Demand explanation or reject skill

---

#### T04.14: Network Communication Audit

**Check**: Audit all network communications

**What to Check**:
- All HTTP/HTTPS endpoints (are they legitimate?)
- Data in transit (is it encrypted?)
- Certificate validation (is it bypassed?)
- Data exfiltration risks

**Example Check**:
```python
# ❌ DANGEROUS - Certificate validation disabled
import requests
requests.get("https://example.com", verify=False)  # No SSL verification!

# ✅ SAFE - Proper certificate validation
requests.get("https://example.com", verify=True)
```

**Scoring**:
- **Pass (10)**: All network communications secure
- **Partial (5)**: Some insecure communications
- **Fail (0)**: Multiple security issues

**Action**: Fix all network security issues

---

#### T04.15: File Access Audit

**Check**: Audit all file system access

**What to Check**:
- Files read (are they user data or system files?)
- Files written (where are they going?)
- File permissions (are they appropriate?)
- Temporary file cleanup

**Example Check**:
```python
# ❌ DANGEROUS - Could read any file
def read_user_file(path: str) -> str:
    with open(path, 'r') as f:  # No validation!
        return f.read()

# ✅ SAFE - Restricted to safe directory
def read_user_file(filename: str) -> str:
    safe_dir = os.path.expanduser("~/skill-data")
    full_path = os.path.join(safe_dir, filename)
    
    # Validate path
    if not os.path.abspath(full_path).startswith(safe_dir):
        raise PermissionError("Access denied")
    
    with open(full_path, 'r') as f:
        return f.read()
```

**Scoring**:
- **Pass (10)**: File access properly restricted
- **Partial (5)**: Some unrestricted access
- **Fail (0)**: Unrestricted file system access

**Action**: Restrict file access to necessary directories

---

## Security Score Calculation

**Zone 1 (Critical)**: 50% weight
- T04.1: Command Injection (15%)
- T04.2: Data Leakage (15%)
- T04.3: Path Traversal (10%)
- T04.4: Permission Overreach (10%)

**Zone 2 (Gating)**: 20% weight
- T04.5: Tool Check (7%)
- T04.6: Env Check (7%)
- T04.7: OS Check (6%)

**Zone 3 (Runtime)**: 15% weight
- T04.8: Input Validation (5%)
- T04.9: Error Messages (5%)
- T04.10: Resource Cleanup (5%)

**Zone 4 (Dependencies)**: 10% weight
- T04.11: Vulnerability Scan (6%)
- T04.12: Source Verification (4%)

**Zone 5 (Advanced)**: 5% weight
- T04.13: Obfuscation (2%)
- T04.14: Network Audit (2%)
- T04.15: File Access (1%)

**Total Security Score** = Sum of all zone scores

**Rating**:
- 90-100: Secure
- 75-89: Mostly Secure
- 60-74: Caution
- 40-59: Risky
- 0-39: Dangerous

---

## Security Action Matrix

| Score | Action | Installation |
|-------|--------|-------------|
| 90-100 | None | ✅ Approve |
| 75-89 | Review and fix minor issues | ⚠️ Conditional |
| 60-74 | Fix critical issues before use | ❌ Block until fixed |
| 40-59 | Significant security concerns | ❌ Reject |
| 0-39 | Critical security vulnerabilities | ❌ Reject and report |

---

## Automated Security Scanning

Integrate with security tools for automated checks:

```bash
# Python skill security scan
python -m bandit -r scripts/
python -m safety check

# Node.js skill security scan
npm audit --audit-level=high
npx eslint scripts/ --plugin security

# General checks
grep -r "eval\|exec\|subprocess.*shell" scripts/
grep -r "os.system\|child_process.exec" scripts/
```

---

## Security Disclosure Template

If security issues are found, use this template to report:

```markdown
## Security Issue Report for [Skill Name]

### Severity: [Critical/High/Medium/Low]

### Issue Description
[Brief description of the security vulnerability]

### Affected Code
```python/ yaml/ bash
[Relevant code snippet]
```

### Proof of Concept
[Steps to reproduce the vulnerability]

### Impact
[What could happen if exploited?]

### Recommended Fix
```python/ yaml/ bash
[Secure implementation]
```

### Additional Notes
[Any other relevant information]
```

---

## Best Practices Summary

1. **Never** trust user input - always validate
2. **Never** hardcode secrets - use environment variables
3. **Always** use parameterized queries - prevent injection
4. **Always** validate file paths - prevent traversal
5. **Always** request minimal permissions - principle of least privilege
6. **Always** sanitize error messages - prevent information leakage
7. **Always** implement proper gating - check dependencies
8. **Always** scan dependencies - update regularly
9. **Always** use HTTPS - encrypt in transit
10. **Always** review code - manual security review

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [OpenClaw Security Guidelines](https://hello-claw.com/cn/adopt/chapter5/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
