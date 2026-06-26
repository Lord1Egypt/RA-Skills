# PaperMC AI Operations Skill

An OpenClaw Agent skill for managing PaperMC Minecraft servers through safe, controlled interfaces.

**Author:** Andrew  
**Version:** 1.0.0  
**License:** MIT

---

## Overview

This skill enables AI agents to maintain PaperMC servers using approved control scripts rather than direct system commands. It follows operational safety principles:

- ✅ Backup-first policy
- ✅ No direct system commands
- ✅ Controlled interfaces only
- ✅ Full audit trail

## Features

- **Server Lifecycle Management**: Start, stop, restart, status checks
- **Backup Automation**: World, plugin, and jar backups
- **Plugin Management**: Safe install, backup, and inventory
- **Health Monitoring**: Automated health checks
- **Update Management**: Controlled PaperMC updates

## Installation

```bash
# Install via OpenClaw
openclaw skill install papermc-ai-ops

# Or manual installation
git clone https://github.com/YOUR_USERNAME/papermc-ai-ops-skill.git
cd papermc-ai-ops-skill
```

## Requirements

- Linux system with systemd
- Java 21+ (Zulu JDK recommended for ARM)
- Python 3.10+
- PaperMC server installation

## Quick Start

### 1. Configure Your Server

Edit `server.env`:
```bash
SERVER_DIR=/path/to/your/papermc-server
BACKUP_RETENTION=10
```

### 2. Run Health Check

```bash
python3 manage_server.py status
bash scripts/health_check.sh
```

### 3. Create Backup

```bash
python3 manage_server.py backup
```

## Control Scripts

### manage_server.py
Server lifecycle and maintenance:
```bash
python3 manage_server.py status          # Check service status
python3 manage_server.py logs -n 50      # View recent logs
python3 manage_server.py backup          # Create world backup
python3 manage_server.py restart         # Safe restart
```

### plugin_manager.py
Plugin operations:
```bash
python3 plugin_manager.py list                           # List plugins
python3 plugin_manager.py backup <plugin.jar>           # Backup plugin
python3 plugin_manager.py install-url <url> --filename <name>  # Install plugin
```

### update_paper.py
PaperMC updates:
```bash
python3 update_paper.py backup-jar                    # Backup current jar
python3 update_paper.py update-from-url <url>         # Update PaperMC
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
1. Run `manage_server.py backup`
2. Verify backup created
3. Proceed with change

## Directory Structure

```
papermc-server/
├── manage_server.py      # Main control script
├── plugin_manager.py     # Plugin operations
├── update_paper.py       # PaperMC updates
├── scripts/
│   └── health_check.sh   # Health monitoring
├── docs/
│   ├── architecture.md   # System design
│   ├── changelog.md      # Change history
│   └── tasks.md          # Maintenance tasks
├── backup/               # World backups
├── plugin_backup/        # Plugin backups
└── jar_backup/           # PaperMC jar backups
```

## Configuration

### server.env
```bash
# Server settings
SERVER_NAME=my-papermc-server
SERVER_PORT=25565

# Java settings
JAVA_PATH=/usr/bin/java
JAVA_MEMORY_MIN=2G
JAVA_MEMORY_MAX=4G

# Backup settings
BACKUP_DIR=./backup
BACKUP_RETENTION=10
```

## Health Monitoring

Run automated health check:
```bash
bash scripts/health_check.sh
```

Checks include:
- Service status
- Log errors
- Plugin count
- Backup age
- Disk space
- Memory usage

## 🏷️ Version Management

### Version Strategy
- **ClawHub**: Latest stable version only (currently v1.1.0)
- **GitHub**: Full version history with tags and releases
- **Recommendation**: Use ClawHub for latest, GitHub for historical versions

### Version History

#### ClawHub (Latest Only)
- **v1.1.0** (Current): Version management strategy, weekly scoring system, automated assessment tools
- Download: https://clawhub.com/skills/papermc-ai-ops

#### GitHub (Full History)
- **v1.1.0**: Latest features with version management strategy
- **v1.0.0**: Initial release with basic server management
- All versions: https://github.com/yanxi1024-git/PaperMC-Ai-Agent/releases
- Tags: `v1.0.0`, `v1.1.0`

### Balanced Upgrade Strategy
Adopt a balanced approach with 1-version lag for stability.

### Weekly Upgrade Scoring
```bash
python3 scripts/weekly-upgrade-scorer.py
```

**Scoring System (100 points):**
- PaperMC Stability (30 points)
- Plugin Compatibility (40 points)
- Testing Validation (20 points)
- Risk Management (10 points)

**Decision Matrix:**
- **≥ 80 points**: Proceed with upgrade (low risk)
- **60-79 points**: Further evaluation needed
- **< 60 points**: Do not upgrade (high risk)

### Automated Scanning
Weekly automated scans evaluate upgrade readiness:
1. Check PaperMC API for new versions
2. Assess plugin compatibility
3. Calculate risk scores
4. Generate detailed reports

### Emergency Rollback
When issues occur:
1. Stop server immediately
2. Restore from latest backup
3. Revert to previous version
4. Verify and restart

## Maintenance Workflow

### Daily
```bash
# Quick health check
bash scripts/health_check.sh
```

### Before Changes
```bash
# Always backup first
python3 manage_server.py backup
python3 plugin_manager.py backup <plugin>
```

### After Changes
```bash
# Verify service health
python3 manage_server.py restart
python3 manage_server.py status
python3 manage_server.py logs -n 100
```

## Troubleshooting

### Service Won't Start
1. Check logs: `manage_server.py logs -n 100`
2. Verify Java: `java -version`
3. Check port: `netstat -tlnp | grep 25565`

### Plugin Issues
1. Check plugin list: `plugin_manager.py list`
2. Review logs for plugin errors
3. Restore from backup if needed

### Backup Failures
1. Check disk space
2. Verify backup directory permissions
3. Check running processes

## Contributing

1. Fork the repository
2. Create feature branch
3. Follow safety rules
4. Submit pull request

## Support

- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/papermc-ai-ops-skill/issues)
- Discussions: [OpenClaw Discord](https://discord.com/invite/clawd)

## Acknowledgments

- PaperMC team for the excellent server software
- OpenClaw community for AI agent standards
- Andrew for operational discipline principles

---

**Note:** This is an AI operations skill. Always review automated actions and maintain backups.
