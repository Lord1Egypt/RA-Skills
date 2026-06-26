---
name: jpeng-code-executor
description: "Safe code execution in sandboxed environments. Supports Python, JavaScript, Bash, and more with resource limits and timeout controls."
version: "1.0.0"
author: "jpeng"
tags: ["code", "execution", "sandbox", "python", "javascript"]
---

# Code Executor

Execute code safely in sandboxed environments with resource limits.

## When to Use

- User wants to run code snippets
- Test code before deployment
- Execute scripts with security constraints
- Run untrusted code safely

## Features

- **Multi-language support**: Python, JavaScript, Bash, Ruby, Go
- **Resource limits**: CPU, memory, execution time
- **Network isolation**: Optional network access
- **File system isolation**: Temporary sandbox directory

## Usage

### Execute Python

```bash
python3 scripts/execute.py \
  --language python \
  --code "print('Hello, World!')" \
  --timeout 10
```

### Execute from file

```bash
python3 scripts/execute.py \
  --language python \
  --file ./script.py \
  --timeout 30 \
  --memory 256
```

### Execute JavaScript

```bash
python3 scripts/execute.py \
  --language javascript \
  --code "console.log(2 + 2)"
```

### With input

```bash
python3 scripts/execute.py \
  --language python \
  --code "x = input(); print(f'You said: {x}')" \
  --input "Hello"
```

## Output

```json
{
  "success": true,
  "stdout": "Hello, World!\n",
  "stderr": "",
  "exit_code": 0,
  "execution_time_ms": 42
}
```

## Safety

- Default timeout: 30 seconds
- Default memory limit: 512MB
- No network access by default
- Output limited to 1MB
