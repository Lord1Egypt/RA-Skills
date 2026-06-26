# Permissions Reference Guide

## OpenClaw Tool Permissions

### File Operations
| Tool | Permission | Risk | Description |
|------|------------|------|-------------|
| `read` | file read | LOW | Read files within accessible paths |
| `write` | file write | MEDIUM | Create/overwrite files |
| `edit` | file write | MEDIUM | Modify existing files |
| `exec` | command | HIGH | Execute shell commands |
| `canvas` | display | LOW | Render/display content |

### Network Operations
| Tool | Permission | Risk | Description |
|------|------------|------|-------------|
| `web_fetch` | network | LOW | HTTP GET requests |
| `web_search` | network | LOW | Search queries |
| `browser` | browser | MEDIUM | Browser automation |
| `message` | message | MEDIUM | Send messages via channels |

### System Operations
| Tool | Permission | Risk | Description |
|------|------------|------|-------------|
| `cron` | schedule | MEDIUM | Schedule tasks |
| `gateway` | admin | HIGH | Gateway configuration |
| `nodes` | hardware | MEDIUM | Device control |

## Skill Permission Risks

### Standard Skills (LOW Risk)
- Read workspace files
- Write to workspace files
- Execute within project scope
- Web search and fetch

### Agentic Skills (MEDIUM Risk)
- Execute shell commands
- File operations outside workspace
- Scheduling and cron
- Device interactions

### System-Level Skills (HIGH Risk)
- Gateway configuration changes
- Node pairing and control
- Plugin installation
- System updates

## Skill Manifest Fields

```yaml
permissions:
  - read  # File read access
  - write # File write access
  - exec  # Shell command execution
  - network  # HTTP requests
  - cron # Scheduled tasks
```

## Auditing Questions

1. **Does the skill need ALL the permissions it requests?**
2. **Can it operate with fewer permissions?**
3. **Are the permissions scoped appropriately?**
4. **Is the permission request documented in SKILL.md?**
5. **Could the permissions be used maliciously?**

## When to Block a Skill

- Requests exec without justification
- Accesses credentials without need
- Phones home to unknown servers
- Attempts privilege escalation
- Contains obfuscated code
- Hardcoded secrets or keys
