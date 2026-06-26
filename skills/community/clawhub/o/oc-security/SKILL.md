---
name: security
description: Security analysis and vulnerability detection. Scans code for security issues, checks dependencies, and provides remediation advice.
---

# Security - Security Analysis

安全分析工具，扫描代码漏洞、检查依赖、提供修复建议。

**Version**: 1.1  
**Features**: 漏洞扫描、依赖检查、密钥检测、安全建议、C/C++ 支持 (NEW)

---

## Quick Start

### 1. 扫描代码

```bash
# 扫描单个文件
python3 scripts/main.py scan --file src/main.py

# 扫描整个项目
python3 scripts/main.py scan --dir src/
```

### 2. 检查依赖

```bash
# 检查依赖漏洞
python3 scripts/main.py deps --requirements requirements.txt

# 检查 package.json
python3 scripts/main.py deps --package-json package.json
```

### 3. 检测密钥泄露

```bash
# 扫描密钥泄露
python3 scripts/main.py secrets --dir .
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `scan` | 安全扫描 | `scan --file src.py` |
| `deps` | 依赖检查 | `deps --requirements req.txt` |
| `secrets` | 密钥检测 | `secrets --dir .` |

---

## 安全扫描

```bash
$ python3 scripts/main.py scan --file src/auth.py

🔒 Security Scan Results
=========================

File: src/auth.py
Issues found: 2

🔴 Critical:
  Line 34: Hardcoded password
    password = "admin123"  # ← Move to environment variable
  
  CWE-798: Use of Hard-coded Credentials

🟡 Medium:
  Line 67: SQL injection risk
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
  
  CWE-89: SQL Injection
  Fix: Use parameterized queries

✅ No secrets detected
```

---

## 依赖检查

```bash
$ python3 scripts/main.py deps --requirements requirements.txt

📦 Dependency Check
===================

Checked: 15 packages
Issues: 2

🔴 CVE-2023-1234: requests < 2.31.0
   Severity: High
   Fix: pip install requests>=2.31.0

🟡 CVE-2023-5678: flask < 2.3.0
   Severity: Medium
   Fix: pip install flask>=2.3.0

✅ All other dependencies up to date
```

---

## 密钥检测

```bash
$ python3 scripts/main.py secrets --dir .

🔑 Secret Detection
===================

Scanned: 45 files
Secrets found: 1

🔴 .env (line 3):
   AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
   
   Type: AWS Secret Access Key
   Action: Move to secrets manager or environment variable

⚠️  Remember to rotate exposed credentials!
```

---

## 检测规则

### 代码漏洞

| 规则 | 严重度 | CWE |
|------|--------|-----|
| Hardcoded credentials | 🔴 Critical | CWE-798 |
| SQL injection | 🔴 Critical | CWE-89 |
| Command injection | 🔴 Critical | CWE-78 |
| Path traversal | 🔴 Critical | CWE-22 |
| Insecure crypto | 🟡 Medium | CWE-327 |
| Weak random | 🟡 Medium | CWE-338 |
| Debug mode enabled | 🟡 Medium | CWE-489 |

### 密钥模式

| 类型 | 检测 |
|------|------|
| API Keys | ✅ |
| AWS Credentials | ✅ |
| Database URLs | ✅ |
| Private Keys | ✅ |
| JWT Secrets | ✅ |
| Passwords in code | ✅ |

---

## Configuration

`.security.json`:

```json
{
  "severity_threshold": "medium",
  "ignore_paths": [
    "tests/**",
    "vendor/**"
  ],
  "ignore_rules": [
    "debug-mode-in-production"
  ],
  "custom_patterns": {
    "company_api_key": "COMPANY_[A-Z0-9]{32}"
  }
}
```

---

## CI/CD 集成

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Scan Code
        run: python3 skills/security/scripts/main.py scan --dir src/
      
      - name: Check Dependencies
        run: python3 skills/security/scripts/main.py deps --requirements requirements.txt
      
      - name: Detect Secrets
        run: python3 skills/security/scripts/main.py secrets --dir .
```

---

## Files

```
skills/security/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── scanner.py              # 漏洞扫描器
    └── rules/                  # 检测规则
        ├── python.yml
        └── javascript.yml
```

---

## Roadmap

- [x] Basic vulnerability detection
- [x] Secret detection
- [x] Dependency checking
- [ ] SAST integration
- [ ] DAST support
