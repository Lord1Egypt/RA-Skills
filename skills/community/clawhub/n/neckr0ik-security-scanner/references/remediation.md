# Security Remediation Guide

How to fix common security vulnerabilities found by skill-security-audit.

## Quick Reference

| Vulnerability | Severity | Quick Fix |
|--------------|----------|-----------|
| Hardcoded Secret | Critical | Use environment variables |
| Shell Injection | Critical | Use subprocess without shell=True |
| Code Execution | Critical | Never use eval/exec with user input |
| Prompt Injection | High | Sanitize user input before prompts |
| Path Traversal | High | Use pathlib and validate paths |
| Unpinned Dependency | Medium | Pin all dependency versions |

---

## Remediation by Vulnerability Type

### 1. Hardcoded Secrets

**Problem:** API keys, passwords, tokens embedded in code.

**Solution:** Environment variables with secure defaults.

```python
# BEFORE (vulnerable)
api_key = "sk-abc123def456..."
password = "MySecret123!"

# AFTER (secure)
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable required")

# Or with default for development only
api_key = os.environ.get("OPENAI_API_KEY", "sk-dev-key-local-only")
```

**Best Practices:**
- Use `.env` files for local development
- Add `.env` to `.gitignore`
- Provide `.env.example` with placeholder values
- Use secrets managers for production (AWS Secrets Manager, HashiCorp Vault)

---

### 2. Shell Injection

**Problem:** User input passed to shell commands.

**Solution:** Use subprocess with shell=False and proper argument handling.

```python
# BEFORE (vulnerable)
import os
filename = user_input
os.system(f"convert {filename} output.png")

# AFTER (secure)
import subprocess
from pathlib import Path

def safe_convert(input_file, output_file):
    # Validate input
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Use subprocess with shell=False (default)
    result = subprocess.run(
        ["convert", str(input_path), str(output_file)],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout
```

**When shell=True is needed:**
```python
import shlex

# Use shlex.quote() to escape user input
safe_input = shlex.quote(user_input)
subprocess.run(f"echo {safe_input}", shell=True)
```

---

### 3. Code Execution (eval/exec)

**Problem:** Dynamic code execution from strings.

**Solution:** Never use eval/exec with untrusted input. Use safe alternatives.

```python
# BEFORE (vulnerable)
user_code = request.form.get("code")
result = eval(user_code)  # NEVER DO THIS

# AFTER - Use ast.literal_eval for safe parsing
import ast
user_data = '{"key": "value"}'
data = ast.literal_eval(user_data)  # Safe for literals only

# AFTER - Use allowlisted operations
ALLOWED_OPS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
}

operation = request.form.get("operation")
if operation in ALLOWED_OPS:
    result = ALLOWED_OPS[operation](a, b)
else:
    raise ValueError(f"Unknown operation: {operation}")
```

---

### 4. Prompt Injection

**Problem:** User input interpolated into AI prompts without sanitization.

**Solution:** Sanitize input and use structured prompt patterns.

```python
# BEFORE (vulnerable)
system_prompt = f"You are a helpful assistant. User says: {user_input}"

# AFTER (secure)
import re

def sanitize_for_prompt(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    # Remove special characters that could be used for injection
    sanitized = re.sub(r'[<>\{\}\[\]\\]', '', text)
    # Limit length
    return sanitized[:1000]

# Use separate context blocks
system_prompt = "You are a helpful assistant."
user_context = sanitize_for_prompt(user_input)
user_message = f"User query: {user_context}"

# Or use OpenAI's message format
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": sanitize_for_prompt(user_input)}
]
```

---

### 5. Path Traversal

**Problem:** User input used in file paths without validation.

**Solution:** Use pathlib and validate paths stay within bounds.

```python
# BEFORE (vulnerable)
filename = request.args.get("file")
with open(f"/data/{filename}") as f:
    content = f.read()

# AFTER (secure)
from pathlib import Path
import re

BASE_DIR = Path("/data").resolve()

def safe_read_file(filename: str) -> str:
    # Sanitize filename
    safe_name = re.sub(r'[^\w.-]', '_', Path(filename).name)
    
    # Build full path
    full_path = (BASE_DIR / safe_name).resolve()
    
    # Verify path is within BASE_DIR
    try:
        full_path.relative_to(BASE_DIR)
    except ValueError:
        raise ValueError(f"Path traversal detected: {filename}")
    
    # Read file
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    return full_path.read_text()
```

---

### 6. Unpinned Dependencies

**Problem:** Dependencies without fixed versions can change unexpectedly.

**Solution:** Pin all versions in requirements.txt and package.json.

```bash
# requirements.txt - BEFORE (vulnerable)
requests
flask
numpy

# requirements.txt - AFTER (secure)
requests==2.31.0
flask==3.0.0
numpy==1.26.0
```

```json
// package.json - BEFORE (vulnerable)
{
  "dependencies": {
    "lodash": "^4.17.0",
    "express": "*"
  }
}

// package.json - AFTER (secure)
{
  "dependencies": {
    "lodash": "4.17.21",
    "express": "4.18.2"
  }
}
```

**Generate pinned requirements:**
```bash
pip freeze > requirements.txt
pip-compile requirements.in --output-file requirements.txt
```

---

## Security Checklist for Skill Authors

Before publishing a skill to ClawHub:

- [ ] No hardcoded secrets in any file
- [ ] No API keys in SKILL.md or documentation
- [ ] All shell commands use subprocess without shell=True
- [ ] No eval/exec with user input
- [ ] User input is sanitized before prompts
- [ ] File paths are validated against path traversal
- [ ] All dependencies are pinned to specific versions
- [ ] .env.example provided with placeholder values
- [ ] .gitignore includes .env and secrets
- [ ] Network requests only to allowlisted domains
- [ ] Run `skill-security-audit audit ./skill/` and fix all issues

---

## Testing Your Fixes

After remediating vulnerabilities, re-run the audit:

```bash
# Test the skill
python scripts/audit.py ./my-skill/

# Expected: "✅ PASSED" with no critical or high issues
```

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)