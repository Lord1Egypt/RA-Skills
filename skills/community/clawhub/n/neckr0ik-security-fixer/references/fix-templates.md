# Fix Templates

Complete library of code fix templates for security vulnerabilities.

## Secrets

### Template: API Key to Environment Variable

**Before:**
```python
api_key = "sk-abc123def456..."
```

**After:**
```python
import os

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable required")
```

### Template: Database Password to Environment Variable

**Before:**
```python
db_password = "MySecret123!"
db_uri = f"postgresql://user:{db_password}@localhost/db"
```

**After:**
```python
import os

db_password = os.environ.get("DB_PASSWORD")
if not db_password:
    raise ValueError("DB_PASSWORD environment variable required")

db_uri = f"postgresql://user:{db_password}@localhost/db"
```

### Template: .env.example

```
# Environment Variables
# Copy to .env and fill in your values

OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
DB_PASSWORD=your-password-here
```

---

## Shell Injection

### Template: os.system to subprocess

**Before:**
```python
import os
os.system(f"convert {filename} output.png")
```

**After:**
```python
import subprocess
from pathlib import Path

def safe_convert(input_file: str, output_file: str) -> str:
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    result = subprocess.run(
        ["convert", str(input_path), str(output_file)],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout
```

### Template: subprocess with shell=True

**Before:**
```python
subprocess.run(f"ls {directory}", shell=True, capture_output=True)
```

**After:**
```python
subprocess.run(["ls", directory], shell=False, capture_output=True)
```

### Template: User Input Sanitization for Shell

**Before:**
```python
import os
os.system(f"echo {user_input}")
```

**After:**
```python
import subprocess
import shlex

safe_input = shlex.quote(user_input)
subprocess.run(["echo", safe_input], shell=False)
```

---

## Code Execution

### Template: eval/exec to Safe Alternatives

**Before:**
```python
result = eval(user_expression)
```

**After (Option 1 - Allowlisted operations):**
```python
ALLOWED_OPS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b if b != 0 else None,
}

parts = user_expression.split()
if len(parts) == 3 and parts[0] in ALLOWED_OPS:
    op = parts[0]
    a, b = float(parts[1]), float(parts[2])
    result = ALLOWED_OPS[op](a, b)
else:
    raise ValueError("Invalid expression")
```

**After (Option 2 - ast.literal_eval for literals):**
```python
import ast

try:
    result = ast.literal_eval(user_input)  # Only evaluates literals
except (ValueError, SyntaxError) as e:
    raise ValueError(f"Invalid input: {e}")
```

---

## Prompt Injection

### Template: User Input Sanitization for Prompts

**Before:**
```python
system_prompt = f"You are a helpful assistant. User says: {user_input}"
```

**After:**
```python
import re

def sanitize_for_prompt(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input for safe inclusion in prompts.
    Removes potentially dangerous characters.
    """
    # Remove special characters that could be used for injection
    sanitized = re.sub(r'[<>\{\}\[\]\\]', '', text)
    # Limit length
    return sanitized[:max_length]

system_prompt = "You are a helpful assistant."
user_message = sanitize_for_prompt(user_input)
```

### Template: Structured Prompt Separation

**Before:**
```python
prompt = f"System: You are helpful.\nUser: {user_input}\nRespond:"
```

**After:**
```python
def create_safe_prompt(user_input: str) -> list[dict]:
    """Create structured prompt with sanitized user input."""
    sanitized = sanitize_for_prompt(user_input)
    
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": sanitized}
    ]

messages = create_safe_prompt(user_input)
```

---

## Path Traversal

### Template: Safe File Path Handling

**Before:**
```python
filename = request.args.get("file")
with open(f"/data/{filename}") as f:
    content = f.read()
```

**After:**
```python
from pathlib import Path
import re

BASE_DIR = Path("/data").resolve()

def safe_path(user_input: str) -> Path:
    """
    Create a safe file path from user input.
    Prevents path traversal attacks.
    """
    # Sanitize filename
    safe_name = re.sub(r'[^\w.-]', '_', Path(user_input).name)
    
    # Build full path
    full_path = (BASE_DIR / safe_name).resolve()
    
    # Verify path is within BASE_DIR
    try:
        full_path.relative_to(BASE_DIR)
    except ValueError:
        raise ValueError(f"Path traversal detected: {user_input}")
    
    return full_path

def read_user_file(filename: str) -> str:
    """Safely read a file from user input."""
    path = safe_path(filename)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    return path.read_text()

# Usage
try:
    content = read_user_file(request.args.get("file", ""))
except (ValueError, FileNotFoundError) as e:
    return {"error": str(e)}, 400
```

---

## Dependencies

### Template: Pin Dependencies

**requirements.txt - Before:**
```
requests
flask
numpy
```

**requirements.txt - After:**
```
requests==2.31.0
flask==3.0.0
numpy==1.26.0
```

**package.json - Before:**
```json
{
  "dependencies": {
    "lodash": "^4.17.0",
    "express": "*"
  }
}
```

**package.json - After:**
```json
{
  "dependencies": {
    "lodash": "4.17.21",
    "express": "4.18.2"
  }
}
```

---

## Network Access

### Template: Domain Allowlisting

**Before:**
```python
import requests
response = requests.get(user_provided_url)
```

**After:**
```python
import requests
from urllib.parse import urlparse

ALLOWED_DOMAINS = [
    "api.openai.com",
    "api.anthropic.com",
    "github.com",
    "api.github.com",
]

def safe_request(url: str, **kwargs) -> requests.Response:
    """Make HTTP request only to allowed domains."""
    parsed = urlparse(url)
    
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain not allowed: {parsed.netloc}")
    
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS allowed")
    
    return requests.get(url, **kwargs)
```

---

## Complete Safe Patterns

### Template: Safe Config Loader

```python
import os
from pathlib import Path
from typing import Any

class SafeConfig:
    """Safe configuration loader with environment variable support."""
    
    def __init__(self, prefix: str = "APP_"):
        self.prefix = prefix
        self._config = {}
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                config_key = key[len(self.prefix):].lower()
                self._config[config_key] = value
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """Get configuration value."""
        value = self._config.get(key.lower(), default)
        
        if required and value is None:
            raise ValueError(f"Required config missing: {self.prefix}{key.upper()}")
        
        return value
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer."""
        value = self.get(key)
        return int(value) if value else default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean."""
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

# Usage
config = SafeConfig("MYAPP_")
api_key = config.get("api_key", required=True)
debug = config.get_bool("debug", default=False)
```

### Template: Safe File Operations

```python
from pathlib import Path
import shutil
import tempfile
from typing import Union

class SafeFileOps:
    """Safe file operations with path validation."""
    
    def __init__(self, base_dir: Union[str, Path]):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def _validate_path(self, path: Union[str, Path]) -> Path:
        """Validate and resolve path within base directory."""
        full_path = (self.base_dir / path).resolve()
        
        try:
            full_path.relative_to(self.base_dir)
        except ValueError:
            raise ValueError(f"Path traversal detected: {path}")
        
        return full_path
    
    def read(self, path: Union[str, Path]) -> str:
        """Safely read a file."""
        safe_path = self._validate_path(path)
        
        if not safe_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        return safe_path.read_text()
    
    def write(self, path: Union[str, Path], content: str) -> None:
        """Safely write to a file."""
        safe_path = self._validate_path(path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.write_text(content)
    
    def delete(self, path: Union[str, Path]) -> None:
        """Safely delete a file."""
        safe_path = self._validate_path(path)
        
        if safe_path.is_file():
            safe_path.unlink()
        elif safe_path.is_dir():
            shutil.rmtree(safe_path)

# Usage
files = SafeFileOps("/data/app")
content = files.read("config.json")
files.write("output.txt", "Hello, World!")
```