---
slug: my-mac-optimizer
displayName: My Mac Optimizer Controller
version: 1.0.0
tags: mac, optimization, utility, system
---

# My Mac Optimizer Controller

This skill allows the AI agent to control the "My Mac Optimizer" application locally on the user's macOS device. 
The application must be running, which starts a local backend server on `http://127.0.0.1:8000`.

## Capabilities mapping

You can control the application and perform actions using standard `curl` commands interacting with the local API.

### 1. System Health & Monitoring
Check the current state of the Mac (CPU, RAM, network, etc.).
```bash
curl http://127.0.0.1:8000/api/performance
curl http://127.0.0.1:8000/api/system
```

### 2. General Optimization (Smart Care)
Free up RAM and perform general background optimization.
```bash
curl -X POST http://127.0.0.1:8000/api/optimize
```

### 3. Junk Cleaning
Scan the system for cache, logs, and trash, and optionally clean them.
```bash
# 1. First, scan to see what can be cleaned
curl http://127.0.0.1:8000/api/scan

# 2. Then, clean the found items (make sure user agrees)
curl -X POST http://127.0.0.1:8000/api/clean
```

### 4. Application Uninstaller
List installed applications and uninstall them seamlessly.
```bash
# List all installed applications
curl http://127.0.0.1:8000/api/apps

# Uninstall a specific application (use the absolute path from the list)
curl -X POST http://127.0.0.1:8000/api/apps/delete \
  -H "Content-Type: application/json" \
  -d '{"path": "/Applications/Example.app"}'
```

### 5. Clutter and Large Files
Identify large files on the user's main hard drive so they can decide if they want to delete them.
```bash
# List large files
curl http://127.0.0.1:8000/api/clutter/large

# Move a file to the Trash
curl -X POST http://127.0.0.1:8000/api/files/delete \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/username/Downloads/large-file.zip"}'
```

---

**Note to Agent:** Always ask the user for confirmation before executing destructive commands such as `/api/apps/delete` or `/api/files/delete`. Optimization and scanning are generally safe to run.
