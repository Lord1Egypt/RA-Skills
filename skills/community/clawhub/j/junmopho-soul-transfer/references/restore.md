# Agent Clone - Restore Reference

## Complete Restore Procedure

### Step 1: Prepare

1. Ensure OpenClaw is installed on the new environment
2. Know the location of your backup archive

### Step 2: Verify Backup (Optional but Recommended)

```bash
openclaw backup verify /path/to/backup.tar.gz
```

If verification fails, do not proceed with restore.

### Step 3: Stop Gateway

```bash
openclaw gateway stop
```

Or if that doesn't work:
```bash
kill $(pgrep openclaw-gateway)
```

### Step 4: Safety Backup Current State

```bash
mv ~/.openclaw ~/.openclaw-backup-$(date +%Y%m%d)
```

### Step 5: Extract Backup

```bash
tar -xzf /path/to/backup.tar.gz -C ~
```

### Step 6: Handle Environment-Specific Paths

If restoring to a different environment type:

```bash
# Find the extracted openclaw directory
find ~ -name "openclaw.json" 2>/dev/null

# Move to correct location for this environment
mv ~/.openclaw ~/.openclaw-temp
mkdir ~/.openclaw
mv ~/.openclaw-temp/* ~/.openclaw/
```

### Step 7: Reinstall npm Dependencies

```bash
cd ~/workspace  # or wherever workspace is
npm install
```

### Step 8: Restart Gateway

```bash
openclaw gateway start
```

Or restart the service:
```bash
systemctl restart openclaw
```

### Step 9: Verify

Ask the agent:
- "Do you know who you are?"
- "What is my name?"
- "What were we working on?"

## Rollback Procedure

If something goes wrong:

```bash
# Stop gateway
openclaw gateway stop

# Remove failed restore
rm -rf ~/.openclaw

# Restore safety backup
mv ~/.openclaw-backup-YYYYMMDD ~/.openclaw

# Restart gateway
openclaw gateway start
```

## Cross-Environment Restore Notes

### Docker → Native Linux
- Extract to ~/ (home directory)
- May need to reinstall Docker volume mounts

### Native Linux → Docker
- Extract to /home/app/
- Adjust workspace path in openclaw.json

### Any → 飞牛 NAS
- Extract to /vol1/@apphome/*/data/
- May need to use 飞牛 app center for restart

## What Gets Overwritten

When restoring, these directories are replaced:
- `~/.openclaw/` — Complete config and credentials
- `~/workspace/` — All workspace files including skills and memory

## What Needs Reconfiguration

After restore, you may need to:
1. Restart the gateway (always)
2. Re-authenticate some channels (WeChat, Telegram)
3. Reinstall npm packages in workspace
4. Update paths in openclaw.json if environment changed

## Verification Checklist

- [ ] Gateway is running
- [ ] `openclaw status` shows all channels
- [ ] `openclaw skills list` shows all skills
- [ ] Agent responds to questions about owner
- [ ] Memory files are readable
- [ ] QMD search works
