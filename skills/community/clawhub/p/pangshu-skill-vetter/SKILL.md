---
name: skill-vetter
description: Security vetting for agent skills before installation. Scans skill code for dangerous Bash commands, sensitive file access, network exfiltration, obfuscated code, and other security risks. Triggers automatically before any skill install, update, or when user asks to "vet" or "check" a skill's security.
---

# Skill Vetter

Security scanner that analyzes skill code before installation.

## When to Use

- **Before any skill installation** via ClawHub or manual
- **Before any skill update** (even trusted skills)
- When user asks: "vet this skill", "check security", "scan before install"
- When installing skills from unknown sources

## Security Checks (Priority Order)

### 🔴 Critical (Block Install)
| Check | Pattern | Action |
|-------|---------|--------|
| Disk wipe | `rm -rf /`, `rm -rf ~`, `dd if=.*of=/dev/sdX` | BLOCK |
| Fork bomb | `:(){ :\|:& };:`, `fork()` loop | BLOCK |
| Format | `mkfs`, `newfs`, `umount -f` | BLOCK |
| SSH key deletion | `rm.*\.ssh/`, `ssh-keygen.*-D` | BLOCK |
| System takeover | `chmod 777.*shadow`, `/etc/passwd` edit | BLOCK |

### 🟡 Medium (Warn + Allow)
| Check | Pattern | Action |
|-------|---------|--------|
| Dangerous rm | `rm -rf [a-z]+\` (recursive without targets) | WARN |
| Network exfil | base64 remote exfil, `curl.*\|.*sh` | WARN |
| Credential access | `.env`, `~/.aws/`, API key patterns | WARN |
| Suspicious encoding | Obfuscated JavaScript, encoded commands | WARN |
| High-privilege | `sudo`, `chmod 777`, `setfacl` | WARN |
| Unknown network | Non-standard ports, suspicious domains | WARN |

### 🔵 Info (Log Only)
| Check | Pattern |
|-------|---------|
| File write | Writes outside skill directory |
| Permission change | Any chmod |
| New file creation | File creation in system paths |

## Usage

### Automatic Vetting (via Hook)

When OpenClaw hooks are configured, the vetter runs automatically:

```bash
# Configure in OpenClaw settings
skill_vetter:
  enabled: true
  auto_block: true   # Block critical issues
  warn_only: false    # false = block criticals
```

### Manual Vetting

```bash
python3 ~/.openclaw/skills/skill-vetter/scripts/vetter.py \
    scan ~/.openclaw/skills/my-skill
```

### Output Format

```
╔══════════════════════════════════════════════════╗
║ 🛡️ Skill Security Vetting Report                  ║
╠══════════════════════════════════════════════════╣
║ Skill: my-skill                                   ║
║ Scan Time: 2026-04-06 07:21:00                   ║
║                                                          ║
║ 🔴 CRITICAL: 0  🟡 WARNING: 2  🔵 INFO: 1            ║
╠══════════════════════════════════════════════════╣
║ Findings:                                              ║
║   (see actual scan output for details)                 ║
╠══════════════════════════════════════════════════╣
║ Verdict: ⚠️ INSTALL WITH CAUTION                       ║
╚══════════════════════════════════════════════════╝
```

## Integration

For automatic pre-install vetting, this skill should be invoked by the OpenClaw skill installation hook. The hook configuration:

```yaml
# In OpenClaw config
hooks:
  pre_skill_install:
    - name: skill-vetter
      action: scan_then_block
      block_on_critical: true
```

## Verdict Logic

| Severity | Count | Verdict |
|----------|-------|---------|
| 🔴 Critical | > 0 | 🚫 BLOCK INSTALL |
| 🟡 Warning | > 3 | ⚠️ WARN + CONFIRM |
| 🟡 Warning | ≤ 3 | ✅ INSTALL WITH CAUTION |
| Only 🔵 Info | Any | ✅ CLEAR TO INSTALL |

## Implementation

The scanner is in `scripts/vetter.py`. Key functions:
- `scan_skill(skill_path)` - Main entry point
- `check_dangerous_commands(content)` - Bash pattern matching
- `check_sensitive_access(content)` - File/credential patterns
- `check_network_activity(content)` - Exfil indicators
- `check_obfuscation(content)` - Obfuscated code detection
- `generate_report(findings)` - Formatted output
