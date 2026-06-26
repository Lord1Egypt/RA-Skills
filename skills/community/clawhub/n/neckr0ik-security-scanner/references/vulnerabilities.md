# Vulnerability Database

Complete database of security vulnerabilities detected by skill-security-audit.

## Critical Vulnerabilities

### SECRET-001: Hardcoded API Keys

**Pattern:** API key embedded in source code

**Examples:**
```python
# VULNERABLE
api_key = "sk-abc123def456..."
token = "ghp_xxxxxxxxxxxx"
```

**Risk:** Credentials exposed in version control, logs, and distribution.

**Fix:**
```python
# SECURE
import os
api_key = os.environ.get("OPENAI_API_KEY")
```

---

### SECRET-002: Hardcoded Passwords

**Pattern:** Password strings in code or config

**Examples:**
```python
# VULNERABLE
password = "MySecret123!"
db_uri = f"mongodb://user:{password}@localhost"
```

**Risk:** Unauthorized access to databases, services.

**Fix:**
```python
# SECURE
import os
password = os.environ.get("DB_PASSWORD")
```

---

### SECRET-003: Private Keys

**Pattern:** RSA/ECDSA/SSH private keys in code

**Examples:**
```python
# VULNERABLE
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----"""
```

**Risk:** Full compromise of cryptographic identity.

**Fix:** Store keys in secure key management systems (AWS KMS, HashiCorp Vault) or load from protected files.

---

### SHELL-001: os.system() with User Input

**Pattern:** Shell command execution with unsanitized input

**Examples:**
```python
# VULNERABLE
import os
filename = user_input
os.system(f"convert {filename} output.png")
```

**Risk:** Arbitrary command execution.

**Fix:**
```python
# SECURE
import subprocess
import shlex
result = subprocess.run(
    ["convert", shlex.quote(filename), "output.png"],
    capture_output=True,
    shell=False
)
```

---

### SHELL-002: eval() / exec() with User Input

**Pattern:** Dynamic code execution

**Examples:**
```python
# VULNERABLE
user_code = request.form.get("code")
result = eval(user_code)
```

**Risk:** Arbitrary code execution (RCE).

**Fix:** Never use eval/exec with user input. Use ast.literal_eval() for safe parsing, or a sandboxed interpreter.

---

### SHELL-003: subprocess with shell=True

**Pattern:** Shell command injection risk

**Examples:**
```python
# VULNERABLE
subprocess.run(f"ls {user_input}", shell=True)
```

**Risk:** Command injection via shell metacharacters.

**Fix:**
```python
# SECURE
subprocess.run(["ls", user_input], shell=False)
```

---

### NET-001: Requests to Suspicious Domains

**Pattern:** HTTP requests to known malicious/untrusted domains

**Known Suspicious Domains:**
- pastebin.com (exfiltration)
- webhook.site (data collection)
- requestbin.* (data collection)
- ngrok.io (tunneling)
- burpcollaborator (security testing)
- interactsh (security testing)

**Risk:** Data exfiltration, C2 communication.

**Fix:** Remove requests to suspicious domains. Use allowlisting for external requests.

---

## High Vulnerabilities

### PROMPT-001: User Input in System Prompts

**Pattern:** Unsanitized user input interpolated into prompts

**Examples:**
```python
# VULNERABLE
system_prompt = f"You are a helpful assistant. User says: {user_input}"
```

**Risk:** Prompt injection attacks.

**Fix:**
```python
# SECURE
import re
sanitized_input = re.sub(r'[^\w\s.,!?-]', '', user_input)
system_prompt = f"You are a helpful assistant."
user_prompt = sanitized_input
```

---

### PATH-001: Path Traversal

**Pattern:** User input in file paths

**Examples:**
```python
# VULNERABLE
filename = request.args.get("file")
with open(f"/data/{filename}") as f:
    content = f.read()
```

**Risk:** Arbitrary file read/write.

**Fix:**
```python
# SECURE
from pathlib import Path
import re

def safe_path(base_dir, user_input):
    # Sanitize filename
    safe_name = re.sub(r'[^\w.-]', '_', user_input)
    # Resolve and check
    full_path = (Path(base_dir) / safe_name).resolve()
    if not str(full_path).startswith(str(Path(base_dir).resolve())):
        raise ValueError("Path traversal detected")
    return full_path
```

---

### EXEC-001: Dynamic Code Execution

**Pattern:** Code execution from strings

**Examples:**
```python
# VULNERABLE
code = user_input
exec(code)
```

**Risk:** Arbitrary code execution.

**Fix:** Never execute user-provided code. Use allowlisted operations or a sandbox.

---

## Medium Vulnerabilities

### DEP-001: Unpinned Dependencies

**Pattern:** Dependencies without fixed versions

**Examples:**
```
# VULNERABLE (requirements.txt)
requests
flask
numpy

# VULNERABLE (package.json)
"dependencies": {
  "lodash": "^4.17.0",
  "express": "*"
}
```

**Risk:** Breaking changes, supply chain attacks.

**Fix:**
```
# SECURE (requirements.txt)
requests==2.31.0
flask==3.0.0
numpy==1.26.0

# SECURE (package.json)
"dependencies": {
  "lodash": "4.17.21",
  "express": "4.18.2"
}
```

---

### DEP-002: Outdated Dependencies

**Pattern:** Dependencies with known CVEs

**Risk:** Known security vulnerabilities.

**Fix:** Regularly update dependencies. Use tools like `pip-audit`, `npm audit`, `snyk`.

---

### MANIFEST-001: Missing SKILL.md

**Pattern:** Skill without proper manifest

**Risk:** Improper skill registration, missing metadata.

**Fix:** Create SKILL.md with required YAML frontmatter.

---

### MANIFEST-002: Missing Required Fields

**Pattern:** SKILL.md without name or description

**Risk:** Skill won't trigger properly.

**Fix:**
```yaml
---
name: my-skill
description: Clear description of what the skill does
---
```

---

## Low Vulnerabilities

### INFO-001: Debug Code Left In

**Pattern:** Debug prints, test code in production

**Risk:** Information disclosure.

**Fix:** Remove debug statements before publishing.

---

### INFO-002: Verbose Error Messages

**Pattern:** Error messages revealing internal details

**Risk:** Information disclosure.

**Fix:** Use generic error messages for users, log details internally.

---

## Whitelisted Domains

These domains are considered safe for network requests:

- api.openai.com
- api.anthropic.com
- github.com / api.github.com
- pypi.org
- npmjs.com
- clawhub.ai
- openclaw.ai
- localhost / 127.0.0.1