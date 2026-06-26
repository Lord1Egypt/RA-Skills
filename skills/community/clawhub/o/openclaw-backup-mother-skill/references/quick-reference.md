# OpenClaw Backup Quick Reference

## Essential Commands

### Backup
```bash
# Config backup
tar -czf openclaw-config-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/config/

# Skills backup  
tar -czf openclaw-skills-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/skills/

# Verify backups
tar -tzf openclaw-*-backup-*.tar.gz | head -3
```

### Restore
```bash
# Restore configs
tar -xzf openclaw-config-backup-*.tar.gz -C ~/

# Restore skills
tar -xzf openclaw-skills-backup-*.tar.gz -C ~/

# Verify restore
ls -la ~/.openclaw/config/ ~/.openclaw/skills/
```

## Common Scenarios

### Scenario 1: Fresh Install
1. Backup everything
2. `sudo apt remove openclaw -y`
3. `curl -sSL https://install.openclaw.ai | bash`
4. Restore backups

### Scenario 2: Migration
1. Backup on old system
2. Transfer backup files
3. Install OpenClaw on new system
4. Restore backups

### Scenario 3: Disaster Recovery
1. Locate latest backups
2. Fresh install OpenClaw
3. Restore from backups
4. Verify functionality

## Safety Tips

1. **Always** create dual backups
2. **Always** verify tar integrity
3. **Never** delete originals until restore verified
4. **Always** test restore on test system first

## File Locations

- **Configs:** `~/.openclaw/config/`
- **Skills:** `~/.openclaw/skills/`
- **Logs:** `~/.openclaw/logs/`
- **Cache:** `~/.openclaw/cache/`

**HELL YEAH, backup ready!** 🎯
