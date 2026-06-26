---
name: papermc-ai-ops
version: 2.0.1
description: Manage PaperMC Minecraft servers through safe, controlled interfaces. Use for server lifecycle management, backups, plugin operations, and health monitoring with backup-first safety policy.
license: MIT
---

# PaperMC Server AI Operations

AI-managed PaperMC Minecraft server operations with safety-first approach.

## When to Use This Skill

Use this skill when you need to:
- Manage PaperMC server lifecycle (status, logs, restart)
- Create backups (world, plugins, PaperMC jar)
- Install or update plugins safely
- Update PaperMC server version
- Monitor server health and diagnose issues
- **Intelligent plugin upgrades with risk assessment** (NEW in v2.0)

## Requirements

- Linux system with systemd
- Java 21+ (Zulu JDK recommended for ARM)
- Python 3.10+
- PaperMC server installation

## Quick Start

### 1. Configure

Edit paths in the scripts:
```python
# In manage_server.py, plugin_manager.py, update_paper.py
SERVER_DIR = Path("/path/to/your/papermc-server")
```

### 2. Check Status

```bash
python3 manage_server.py status
```

### 3. Create Backup

```bash
python3 manage_server.py backup
```

## Core Scripts

### manage_server.py

Server lifecycle management:
```bash
python3 manage_server.py status          # Service status
python3 manage_server.py logs -n 50      # View logs
python3 manage_server.py backup          # Backup world
python3 manage_server.py restart         # Safe restart
```

### plugin_manager.py

Plugin operations:
```bash
python3 plugin_manager.py list                           # List plugins
python3 plugin_manager.py backup <plugin.jar>           # Backup plugin
python3 plugin_manager.py install-url <url> --filename <name>
```

### update_paper.py

PaperMC updates:
```bash
python3 update_paper.py backup-jar                    # Backup current jar
python3 update_paper.py update-from-url <paper_jar_url>
```

### plugin_upgrade_framework.py (NEW in v2.0)

Intelligent plugin upgrade framework with risk assessment:

```bash
# Upgrade specific plugin (Method 1)
python3 plugin_upgrade_framework.py --plugin ViaVersion --version 5.8.0

# Scan for upgrade candidates (Method 2)
python3 plugin_upgrade_framework.py --method 2 --scan-limit 20

# Run examples
python3 upgrade_examples.py
```

## Safety Rules

### ❌ Never Use Direct Commands
- `kill`, `kill -9`
- `rm -rf`
- `systemctl stop/restart`
- Direct file overwrites

### ✅ Always Use Scripts
All operations go through approved Python scripts.

### 📦 Backup-First Policy
Before ANY risky operation:
1. Run backup command
2. Verify backup created
3. Proceed with change

## Plugin Upgrade Framework (NEW in v2.0)

Based on ViaVersion 5.7.2 → 5.8.0 upgrade experience (2026-03-28), this skill now includes an intelligent plugin upgrade framework.

### Core Upgrade Methods

#### Method 1: Specific Plugin Upgrade
For upgrading a specific plugin with full automation:

```python
from plugin_upgrade_framework import PluginUpgradeFramework

framework = PluginUpgradeFramework()
result = framework.method1_specific_plugin_upgrade("ViaVersion", "5.8.0")
```

#### Method 2: Scan and Assess Upgrades
For periodic maintenance and batch upgrade planning:

```python
result = framework.method2_scan_and_assess_upgrades(limit=20)
```

### Risk Assessment Logic

| Risk Level | Version Jump | Action |
|------------|--------------|--------|
| **Low** | Patch update (x.x.1 → x.x.2) | Recommended upgrade |
| **Medium** | Minor update (x.1.x → x.2.x) | Test before production |
| **High** | Major update (1.x.x → 2.x.x) | Detailed assessment needed |

### Proxy Configuration for Hangar

If you have proxy issues, configure NO_PROXY:

```bash
export NO_PROXY="localhost,127.0.0.1,192.168.8.165,hangar.papermc.io,papermc.io,hangarcdn.papermc.io"
```

### Download URL Pattern

Hangar plugin download URLs follow this pattern:
```
https://hangarcdn.papermc.io/plugins/{plugin}/{plugin}/versions/{version}/PAPER/{plugin}-{version}.jar
```

### Verification Steps After Upgrade

1. Check server logs for errors
2. Verify plugin loaded message
3. Test core functionality
4. Monitor server performance
5. Have rollback plan ready

### ViaVersion Upgrade Experience

See `viaversion_upgrade_report.json` for detailed documentation of the successful ViaVersion 5.7.2 → 5.8.0 upgrade, including:
- Proxy issue resolution
- Risk assessment validation
- Complete upgrade process
- Lessons learned

## Health Monitoring

```bash
bash scripts/health_check.sh
```

Checks:
- Service status
- Log errors
- Plugin count
- Backup age
- Disk space
- Memory usage

## Version Management Strategy

### Balanced Upgrade Strategy
Adopt a balanced approach with 1-version lag for stability.

### Weekly Upgrade Scoring System
```bash
python3 scripts/weekly-upgrade-scorer.py
```

**Scoring Criteria (100 points total):**
1. **PaperMC Stability (30 points)**
   - Official API confirmation
   - Release age (>2 weeks)
   - Security patches included

2. **Plugin Compatibility (40 points)**
   - Core plugins compatibility
   - All plugins compatible
   - Recent plugin updates
   - No critical warnings

3. **Testing & Validation (20 points)**
   - Test environment validation
   - Performance benchmarks
   - Functionality verification

4. **Risk Management (10 points)**
   - Backup readiness
   - Rollback plan tested

### Upgrade Decision Matrix
- **≥ 80 points**: Proceed with upgrade (low risk)
- **60-79 points**: Further evaluation needed
- **< 60 points**: Do not upgrade (high risk)

### Weekly Scanning Procedure
1. **Monday**: Run automated scoring
2. **Review**: Analyze report and scores
3. **Decision**: Human confirmation required for ≥80 scores
4. **Execution**: Scheduled upgrade with full backup

### Emergency Rollback
Trigger conditions:
- Server crash on startup
- TPS consistently below 15
- Critical plugin failures
- Player data corruption

Rollback steps:
1. Stop server immediately
2. Restore from latest backup
3. Revert to previous version
4. Verify and restart

## Directory Structure

```
papermc-server/
├── manage_server.py              # Main control script
├── plugin_manager.py             # Plugin operations
├── update_paper.py               # PaperMC updates
├── plugin_upgrade_framework.py   # Intelligent plugin upgrades (NEW)
├── upgrade_examples.py           # Upgrade usage examples (NEW)
├── viaversion_upgrade_report.json # ViaVersion experience (NEW)
├── backup.sh                     # Backup automation
├── scripts/
│   └── health_check.sh           # Health monitoring
├── docs/
│   ├── architecture.md           # System design
│   ├── changelog.md              # Change history
│   └── Turret_Plugin_User_Manual.md  # Turret plugin guide (NEW)
├── backup/                       # World backups
├── plugin_backup/                # Plugin backups
└── jar_backup/                   # PaperMC jar backups
```

## Workflow Examples

### Daily Health Check
```bash
bash scripts/health_check.sh
```

### Before Plugin Update (Traditional)
```bash
python3 manage_server.py backup
python3 plugin_manager.py backup OldPlugin.jar
python3 plugin_manager.py install-url <new_plugin_url> --filename NewPlugin.jar
python3 manage_server.py restart
python3 manage_server.py status
```

### Intelligent Plugin Upgrade (NEW)
```bash
# Scan for upgrade candidates
python3 plugin_upgrade_framework.py --method 2 --scan-limit 20

# Upgrade specific plugin with risk assessment
python3 plugin_upgrade_framework.py --plugin ViaVersion --version 5.8.0 --auto-restart

# Run batch upgrade planning
python3 upgrade_examples.py
```

### PaperMC Update
```bash
python3 update_paper.py backup-jar
python3 update_paper.py update-from-url <paper_download_url>
python3 manage_server.py restart
python3 manage_server.py status
```

## Configuration

### Environment Variables (.env)
```bash
SERVER_NAME=my-server
SERVER_DIR=/path/to/server
BACKUP_RETENTION=10
```

## Troubleshooting

### Service Won't Start
```bash
python3 manage_server.py logs -n 100
```

### Check Disk Space
```bash
df -h
```

### Verify Java
```bash
java -version
```

## Safety First

This skill enforces operational discipline:
- All actions through controlled interfaces
- Mandatory backups before changes
- No destructive direct commands
- Full traceability

Never bypass the script layer for "quick fixes."

## See Also

- `docs/architecture.md` - System architecture
- `docs/changelog.md` - Version history
- `docs/Turret_Plugin_User_Manual.md` - Complete Turret plugin guide
- `scripts/health_check.sh` - Health monitoring script
- `manage_server.py` - Main control script
- `plugin_manager.py` - Plugin operations
- `update_paper.py` - PaperMC updates
- `plugin_upgrade_framework.py` - Intelligent plugin upgrade framework
- `upgrade_examples.py` - Upgrade usage examples
- `viaversion_upgrade_report.json` - ViaVersion upgrade experience

## License

MIT License - See LICENSE file

---

**Skill Version**: 2.0.0 (Enhanced with Plugin Upgrade Framework)  
**Based on**: v1.0.0 release  
**Experience Source**: ViaVersion 5.7.2 → 5.8.0 Upgrade (2026-03-28)  
**Core Value**: Combines AI-managed safety-first operations with intelligent plugin upgrade capabilities based on real-world experience.  
**ClawHub Slug**: papermc-ai-ops  
**GitHub**: https://github.com/yanxi1024-git/PaperMC-Ai-Agent