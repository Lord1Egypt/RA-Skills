---
name: port-manager
description: "Port Manager - Track and manage system port usage. Use when: (1) Port conflict when installing software, (2) Check port usage, (3) Release occupied ports, (4) List all recorded service ports"
metadata:
  {"openclaw": {"emoji": "🔌"}}
---

# Port Manager Skill

Intelligently manage system port usage and avoid conflicts.

## Features

### 1. Record Port (--record)
Record a port when starting a service:
```
Port record <service_name> <port>
Example: port record postgres 5432
```

### 2. Query Port (--query)
Check usage of a specific port:
```
Port query 5432
```

### 3. List All Ports (--list)
Show all recorded services and ports:
```
Port list
```

### 4. Free Port (--free)
Release an occupied port (terminate the process):
```
Port free 5432
```

### 5. Check and Resolve Conflicts (--check)
Check if a port is occupied, and ask user if they want to free it:
```
Port check 5432
```

### 6. Auto Port Allocation (--allocate)
When port is occupied, automatically allocate an available port:
```
Port allocate <service_name> [preferred_port]
```

## File Location

- Port records: `~/.openclaw/workspace/.port-manager/ports.json`

## Usage Scenarios

1. **Check before installing software**
   - Check port 5432 before installing PostgreSQL
   - If occupied, ask user whether to free it

2. **Service startup recording**
   - Record ports like 2375, 5432 when starting Docker
   - Quickly see which services should run after restart

3. **Port conflict resolution**
   - Two services fighting for the same port
   - Auto-assign new port or free old port

## Command Examples

```bash
# Record ports
port record mysql 3306
port record redis 6379
port record postgres 5432

# List all
port list

# Check port
port check 8080

# Free port
port free 5432

# Auto allocate
port allocate nginx 80
```

## Implementation

Use `lsof` and `netstat` to check ports:
```bash
# Check port usage
lsof -i :5432

# Kill process
kill $(lsof -t -i :5432)
```
