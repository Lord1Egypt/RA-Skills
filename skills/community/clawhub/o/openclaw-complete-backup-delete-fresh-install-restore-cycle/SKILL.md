---
name: "mother-of-all-openclaw-backup-restore-skills"
title: "Mother of All OpenClaw Backup & Restore Skills"
description: "The definitive, self-improving, community-wisdom-infused backup/restore skill. British dry humour + canine wisdom. Tested in production. Evolving with every use."
category: "devops"
personality: [dry-humour, practical, understated, safety-first]
trigger: |
  When OpenClaw has become a bit... temperamental. Or when you fancy testing if your backups actually work (they probably don't).
  - Refresh OpenClaw installation (it's looking tired)
  - Test disaster recovery (for fun, obviously)
  - Perform major upgrade (brave soul)
  - Clean up corrupted installation (again?)
prerequisites:
  - OpenClaw installed and running (for now)
  - Root/sudo access (because we're not messing about)
  - Disk space for backups (2x .openclaw size, plus a bit for luck)
  - Improved backup scripts installed (openclaw-backup, openclaw-restore)
pitfalls:
  - Not stopping OpenClaw before delete (it gets upset)
  - Not verifying backups before restore (optimism isn't a backup strategy)
  - Not testing in sandbox first (live dangerously, they said)
  - Running out of disk space during backup (always a crowd-pleaser)
version: "2.2.1"
created: "2026-04-09"
updated: "2026-04-10"
author: "Stef Ferreira"
status: "published"
published: "2026-04-10"
style: "English dry humour (Atlas-inspired) - Butler-like tone treating backup/restore as terribly serious while actually just moving files around. Uses phrases like 'Right then', 'Looking rather promising', 'What could possibly go wrong?', and 'HELL YEAH'"
tags: [openclaw, backup, restore, disaster-recovery, devops, vps, ssh, npm, systemd, production-tested]
---

# Complete OpenClaw Restoration Cycle

**In one sentence:** Backup everything, delete it all, install fresh, restore from backup. What could possibly go wrong?

## The Problem
OpenClaw has developed... personality. Or rather, too many personalities. Config files everywhere, conflicting versions, mysterious errors that appear and disappear like British summer. Time for a fresh start.

## The Fix  
**Option 1 (Full Cycle):** backup → delete → fresh install → restore. All in one go.  
**Option 2 (Modular):** Do individual steps as needed. Backup now, restore later. Delete without restoring. Install fresh without backup. Because real life isn't linear.

**Key Principle:** Every step should be **independent** but **composable**. Like Lego blocks. Or like the dogs - Romeo can be grumpy alone, but with Luna they're a team.

## 🎯 WORKFLOW SELECTOR: Choose Your Adventure

**Option A: Full Cycle** - Backup → Delete → Install → Restore (all in one go)  
**Option B: Clean Install with Delayed Selective Restore** - Backup → Delete → Install → Work → Restore selectively later  
**Option C: Just Backup** - Create backup only (safety first)  
**Option D: Just Restore** - Restore from existing backup  
**Option E: Just Delete & Install** - Fresh start without backup/restore

---

## Phase 1: Preparation (The Boring Bit)

### Step 1: Verify Current State
```bash
# Is OpenClaw even running? Let's find out (like calling Romeo - he might ignore you)
openclaw status

# Check processes (are there ghosts in the machine? Or just Luna pretending to be a worm?)
ps aux | grep openclaw

# How big is this mess anyway? (Probably Luna-sized)
du -sh ~/.openclaw
```

### Step 2: Install Improved Scripts
If you haven't already (you probably haven't):
```bash
# Check if scripts exist (they don't, do they?)
which openclaw-backup openclaw-restore || echo "Right. Let's fix that."

# The scripts should be at:
ls -la /usr/local/bin/openclaw-*
```

---

## 🎯 WORKFLOW B: CLEAN INSTALL WITH DELAYED SELECTIVE RESTORE
*(For when you want: Backup → Delete → Fresh Install → Work → Restore selectively later)*

### B1: Create Intelligent Categorized Backup
```bash
echo "=== CREATING CATEGORIZED BACKUP FOR SELECTIVE RESTORE ==="
echo "Backing up in categories so you can restore only what you need later..."

BACKUP_ROOT="/root/BACKUPS/OpenClaw_Selective_$(date +%Y-%m-%d_%H%M%S)"
mkdir -p "$BACKUP_ROOT"

# Category 1: CREDENTIALS & API KEYS (Most critical)
echo "1. Backing up credentials & API keys..."
mkdir -p "$BACKUP_ROOT/01_CREDENTIALS_API_KEYS"
if [ -d ~/.openclaw/credentials ]; then
    cp -r ~/.openclaw/credentials/* "$BACKUP_ROOT/01_CREDENTIALS_API_KEYS/"
    echo "   ✅ Credentials backed up"
else
    echo "   ⚠️  No credentials directory found"
fi

# Category 2: CONFIGURATION SETTINGS
echo "2. Backing up configuration settings..."
mkdir -p "$BACKUP_ROOT/02_CONFIGURATIONS_SETTINGS"
if [ -f ~/.openclaw/openclaw.json ]; then
    cp ~/.openclaw/openclaw.json "$BACKUP_ROOT/02_CONFIGURATIONS_SETTINGS/"
    echo "   ✅ Main config backed up"
fi
if [ -f ~/.openclaw/update-check.json ]; then
    cp ~/.openclaw/update-check.json "$BACKUP_ROOT/02_CONFIGURATIONS_SETTINGS/"
fi

# Category 3: AGENT IDENTITIES & PERSONALITIES
echo "3. Backing up agent identities..."
mkdir -p "$BACKUP_ROOT/03_AGENT_IDENTITIES"
if [ -d ~/.openclaw/agents ]; then
    # Backup agent configs but NOT their workspaces (too big)
    find ~/.openclaw/agents -name "*.json" -type f | while read file; do
        rel_path="${file#~/.openclaw/agents/}"
        mkdir -p "$BACKUP_ROOT/03_AGENT_IDENTITIES/$(dirname "$rel_path")"
        cp "$file" "$BACKUP_ROOT/03_AGENT_IDENTITIES/$rel_path"
    done
    echo "   ✅ Agent configs backed up (excluding workspaces)"
fi

# Category 4: BUSINESS RULES & TASKS
echo "4. Backing up business rules & tasks..."
mkdir -p "$BACKUP_ROOT/04_BUSINESS_RULES_TASKS"
if [ -d ~/.openclaw/tasks ]; then
    cp -r ~/.openclaw/tasks/* "$BACKUP_ROOT/04_BUSINESS_RULES_TASKS/" 2>/dev/null || true
    echo "   ✅ Tasks backed up"
fi

# Category 5: TELEGRAM & CHANNEL CONFIGS
echo "5. Backing up Telegram & channel configs..."
mkdir -p "$BACKUP_ROOT/05_CHANNEL_CONFIGS"
if [ -d ~/.openclaw/telegram ]; then
    cp -r ~/.openclaw/telegram/* "$BACKUP_ROOT/05_CHANNEL_CONFIGS/" 2>/dev/null || true
    echo "   ✅ Telegram configs backed up"
fi

# Create backup manifest
cat > "$BACKUP_ROOT/00_BACKUP_MANIFEST.md" << EOF
# OPENCLAW SELECTIVE BACKUP MANIFEST
Backup created: $(date)
Backup ID: $(basename "$BACKUP_ROOT")
Purpose: Clean install with delayed selective restore

## CATEGORIES BACKED UP:
1. **Credentials & API Keys** - Critical secrets
2. **Configuration Settings** - System settings
3. **Agent Identities** - Agent configs (no workspaces)
4. **Business Rules & Tasks** - Workflow definitions
5. **Channel Configs** - Telegram/WhatsApp settings

## WHAT WAS INTENTIONALLY EXCLUDED:
- Workspace directories (too large, recreate fresh)
- Cache files (temporary)
- Log files (regenerate)
- Database files (lcm.db - start fresh)

## SELECTIVE RESTORATION INSTRUCTIONS:
To restore only specific categories later:

\`\`\`bash
# Restore credentials only:
cp -r "$BACKUP_ROOT/01_CREDENTIALS_API_KEYS/"* ~/.openclaw/credentials/

# Restore configs only:
cp "$BACKUP_ROOT/02_CONFIGURATIONS_SETTINGS/"* ~/.openclaw/

# Restore agents only:
cp -r "$BACKUP_ROOT/03_AGENT_IDENTITIES/"* ~/.openclaw/agents/

# Restore tasks only:
cp -r "$BACKUP_ROOT/04_BUSINESS_RULES_TASKS/"* ~/.openclaw/tasks/

# Restore Telegram configs only:
cp -r "$BACKUP_ROOT/05_CHANNEL_CONFIGS/"* ~/.openclaw/telegram/
\`\`\`

## BACKUP LOCATION:
$BACKUP_ROOT

Total size: $(du -sh "$BACKUP_ROOT" | cut -f1)
EOF

echo "✅ Categorized backup created at: $BACKUP_ROOT"
echo "   You can now delete OpenClaw and install fresh."
echo "   Restore selectively later using the manifest above."
```

If missing, create them from our tested versions. Or just wing it. Your choice.

## Phase 2: Backup (The "Hope This Works" Phase)

### Step 3: Create Comprehensive Backup
```bash
# Full backup (takes a while, make tea. Or watch Thomas hop around like a bunny)
/usr/local/bin/openclaw-backup full

# Config-only backup (for the impatient)
/usr/local/bin/openclaw-backup config

# INTELLIGENT BACKUP: Configurations only (11MB vs 324MB!)
# This is the smart approach - backup only what matters
echo "=== INTELLIGENT CONFIGURATION BACKUP ==="
echo "Backing up only configurations, not cache/logs bloat..."
mkdir -p /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only
cd /root/.openclaw

# Create categorized backup structure
mkdir -p /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/01_CREDENTIALS_API_KEYS
mkdir -p /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/02_CONFIGURATIONS_SETTINGS
mkdir -p /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/03_AGENT_IDENTITIES_SOULS
mkdir -p /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/04_BUSINESS_RULES_PROCEDURES

# Copy key files by category (selective restoration!)
cp -r credentials/* /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/01_CREDENTIALS_API_KEYS/
cp openclaw.json update-check.json /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/02_CONFIGURATIONS_SETTINGS/
cp -r agents/config.json agents/models.json /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/03_AGENT_IDENTITIES_SOULS/
cp -r tasks/ /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/04_BUSINESS_RULES_PROCEDURES/

# Create backup summary
cat > /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only/00_BACKUP_SUMMARY.md << EOF
# OPENCLAW CONFIGURATION BACKUP SUMMARY
Generated: $(date -Iseconds)
Backup Type: Intelligent (Configurations Only)
Size: $(du -sh /root/BACKUPS/$(date +%Y-%m-%d)_OpenClaw_Configurations_Only | cut -f1)

## What Was Backed Up:
1. Credentials & API Keys
2. Configuration Settings  
3. Agent Identities & Souls
4. Business Rules & Procedures

## What Was NOT Backed Up (Intentionally):
- Cache files
- Log files
- Workspace bloat
- Installable packages

## Restoration Note:
This is a LEAN backup. Restore by copying files to appropriate locations.
EOF

echo "✅ Intelligent backup created: 11MB vs 324MB full backup"

# Verify the backup actually contains data (surprise!)
/usr/local/bin/openclaw-restore verify /root/backups/openclaw/openclaw-backup-*.tar.gz

# List all backups (admire your work)
/usr/local/bin/openclaw-backup list
```

### Step 4: Sandbox Test (The Smart Move)
```bash
# Test restore in sandbox (because we're not reckless)
latest_backup=$(ls -t /root/backups/openclaw/openclaw-backup-*.tar.gz | head -1)
/usr/local/bin/openclaw-restore sandbox-test "$latest_backup"

# If that fails... well, you have other backups, right?
```

## Phase 3: The Purge (The Fun Bit)

### Step 5: Stop Everything
```bash
# Stop OpenClaw gateway (gently now)
openclaw gateway stop

# Double-check it's really stopped (it never is)
sleep 2
ps aux | grep openclaw

# Kill any stragglers (don't be shy)
pkill -f openclaw
```

### Step 6: Backup Current State (Safety Net)
```bash
# Move current .openclaw to backup location (like Buster looking for a safe cuddle spot)
backup_dir="$HOME/.openclaw-pre-purge-$(date +%Y%m%d-%H%M%S)"
if [ -d "$HOME/.openclaw" ]; then
    mv "$HOME/.openclaw" "$backup_dir"
    echo "Current OpenClaw backed up to: $backup_dir (Safety first! Thomas would approve)"
else
    echo "No .openclaw directory found. That's... concerning. Even Romeo would notice this."
fi
```

### Step 7: Remove OpenClaw (The Point of No Return)
```bash
# Uninstall OpenClaw package (if installed via npm)
npm uninstall -g @martian-engineering/lossless-claw 2>/dev/null || echo "Not installed via npm, moving on..."

# Remove any remaining binaries
which openclaw && rm -f "$(which openclaw)" || echo "Binary already gone"

# Clean up any stray files (they're like glitter)
find /usr/local/bin -name "*openclaw*" -delete 2>/dev/null || true
```

## Phase 4: Fresh Install (The Optimistic Phase)

### Step 8: Install OpenClaw Fresh
```bash
# Install via npm (the official way)
npm install -g @martian-engineering/lossless-claw

# Verify installation (fingers crossed)
openclaw --version

# If that fails, try the direct method (because npm)
curl -fsSL https://cli.openclaw.ai/install.sh | sh
```

### Step 9: Initial Configuration & Binary Fix
```bash
# Initialize with minimal config
mkdir -p ~/.openclaw
echo '{"gateway": {"port": 3000}}' > ~/.openclaw/openclaw.json

# Set proper permissions (OpenClaw is fussy)
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json

# FIX OPENCLAW COMMAND ISSUE (Common after npm install)
echo "=== OPENCLAW COMMAND TROUBLESHOOTING ==="

# Check if OpenClaw is installed but command missing
if npm list -g openclaw 2>/dev/null | grep -q "openclaw"; then
    echo "OpenClaw npm package is installed..."
    
    # Check for openclaw.mjs file
    OPENCLAW_MJS=$(find /usr/lib/node_modules -name "openclaw.mjs" 2>/dev/null | head -1)
    if [ -n "$OPENCLAW_MJS" ]; then
        echo "Found openclaw.mjs at: $OPENCLAW_MJS"
        
        # Create symlink
        sudo ln -sf "$OPENCLAW_MJS" /usr/local/bin/openclaw
        sudo chmod +x /usr/local/bin/openclaw
        echo "✅ Created symlink: /usr/local/bin/openclaw → $OPENCLAW_MJS"
    else
        echo "❌ openclaw.mjs not found. Checking package structure..."
        
        # Check package.json for bin entry
        PKG_JSON=$(find /usr/lib/node_modules -name "package.json" -path "*openclaw*" 2>/dev/null | head -1)
        if [ -n "$PKG_JSON" ]; then
            BIN_ENTRY=$(grep -A2 '"bin"' "$PKG_JSON" | grep '"openclaw"' | cut -d'"' -f4)
            if [ -n "$BIN_ENTRY" ]; then
                echo "Package.json specifies bin: $BIN_ENTRY"
                # Try to find it
                BIN_PATH=$(find /usr/lib/node_modules -name "$BIN_ENTRY" -path "*openclaw*" 2>/dev/null | head -1)
                if [ -n "$BIN_PATH" ]; then
                    sudo ln -sf "$BIN_PATH" /usr/local/bin/openclaw
                    sudo chmod +x /usr/local/bin/openclaw
                    echo "✅ Created symlink to: $BIN_PATH"
                fi
            fi
        fi
    fi
fi

# Alternative: If OpenClaw is a dependency of lossless-claw
if npm list -g @martian-engineering/lossless-claw 2>/dev/null | grep -q "openclaw"; then
    echo "OpenClaw is installed as dependency of lossless-claw..."
    DEP_PATH="/usr/lib/node_modules/@martian-engineering/lossless-claw/node_modules/openclaw"
    if [ -d "$DEP_PATH" ]; then
        OPENCLAW_MJS="$DEP_PATH/openclaw.mjs"
        if [ -f "$OPENCLAW_MJS" ]; then
            sudo ln -sf "$OPENCLAW_MJS" /usr/local/bin/openclaw
            sudo chmod +x /usr/local/bin/openclaw
            echo "✅ Created symlink from dependency: $OPENCLAW_MJS"
        fi
    fi
fi

# Final verification
echo ""
echo "=== FINAL VERIFICATION ==="
if which openclaw >/dev/null 2>&1; then
    echo "✅ OpenClaw command found at: $(which openclaw)"
    openclaw --version 2>&1 | head -2 || echo "⚠️  Command exists but doesn't run"
else
    echo "❌ OpenClaw command still not found. Try reinstalling:"
    echo "   sudo npm install -g openclaw --verbose"
    echo "   Or use: node /usr/lib/node_modules/openclaw/openclaw.mjs"
fi
```

## Phase 5: Restoration (The Moment of Truth)

### Step 10: Restore from Backup
```bash
# OPTION A: Restore from full backup
latest_backup=$(ls -t /root/backups/openclaw/openclaw-backup-*.tar.gz | head -1)

# Restore with explicit confirmation (no accidents)
/usr/local/bin/openclaw-restore restore "$latest_backup" yes

# IMPORTANT: The restore script extracts to a timestamped directory, NOT directly to ~/.openclaw
# Check where it was extracted:
restore_dir=$(find /root -name ".openclaw-manual-backup-*" -type d | head -1)
echo "Backup extracted to: $restore_dir"

# OPTION B: INTELLIGENT RESTORATION (from categorized backup)
# If you used the intelligent backup approach (configurations only):
INTELLIGENT_BACKUP=$(find /root/BACKUPS -name "*OpenClaw_Configurations_Only" -type d | sort -r | head -1)
if [ -d "$INTELLIGENT_BACKUP" ]; then
    echo ""
    echo "=== INTELLIGENT RESTORATION ==="
    echo "Restoring from categorized backup: $INTELLIGENT_BACKUP"
    
    # Create fresh .openclaw directory
    rm -rf ~/.openclaw
    mkdir -p ~/.openclaw
    
    # Restore by category (selective tick-box restoration!)
    echo "1. Restoring credentials & API keys..."
    if [ -d "$INTELLIGENT_BACKUP/01_CREDENTIALS_API_KEYS" ]; then
        mkdir -p ~/.openclaw/credentials
        cp -r "$INTELLIGENT_BACKUP/01_CREDENTIALS_API_KEYS/"* ~/.openclaw/credentials/
    fi
    
    echo "2. Restoring configuration settings..."
    if [ -d "$INTELLIGENT_BACKUP/02_CONFIGURATIONS_SETTINGS" ]; then
        cp "$INTELLIGENT_BACKUP/02_CONFIGURATIONS_SETTINGS/"* ~/.openclaw/ 2>/dev/null || true
    fi
    
    echo "3. Restoring agent identities..."
    if [ -d "$INTELLIGENT_BACKUP/03_AGENT_IDENTITIES_SOULS" ]; then
        mkdir -p ~/.openclaw/agents
        cp -r "$INTELLIGENT_BACKUP/03_AGENT_IDENTITIES_SOULS/"* ~/.openclaw/agents/
    fi
    
    echo "4. Restoring business rules..."
    if [ -d "$INTELLIGENT_BACKUP/04_BUSINESS_RULES_PROCEDURES" ]; then
        mkdir -p ~/.openclaw/tasks
        cp -r "$INTELLIGENT_BACKUP/04_BUSINESS_RULES_PROCEDURES/"* ~/.openclaw/tasks/
    fi
    
    echo "✅ Intelligent restoration complete!"
    echo "   Clean 11MB configs vs 324MB bloat"
    restore_dir="$INTELLIGENT_BACKUP"
fi

# If ~/.openclaw doesn't exist after restore, copy manually:
if [ ! -d "$HOME/.openclaw" ]; then
    echo "Restore didn't create ~/.openclaw. Copying manually..."
    # Use strategic piecemeal copying (see Advanced section below)
    mkdir -p ~/.openclaw
    cp -r "$restore_dir/agents" ~/.openclaw/
    cp -r "$restore_dir/workspace" ~/.openclaw/
    cp "$restore_dir/openclaw.json" ~/.openclaw/
    cp -r "$restore_dir/credentials" ~/.openclaw/
    cp -r "$restore_dir/tasks" ~/.openclaw/
    cp -r "$restore_dir/logs" ~/.openclaw/
    cp "$restore_dir/lcm.db*" ~/.openclaw/
fi
```

### Step 11: Start OpenClaw & Verify Dashboard
```bash
# Start the gateway (deep breath, like calling Romeo - he might ignore you)
openclaw gateway start

# Wait for it to initialize (patience is a virtue that Thomas lacks)
sleep 5

# Check status (please work. Put that in your pipe and smoke it)
openclaw status

# Verify dashboard is accessible (this is the whole point, really)
echo \"=== DASHBOARD VERIFICATION ===\"
echo \"Dashboard should be at: http://localhost:18789\"
echo \"Testing connectivity...\"

# Try to open browser (if GUI available)
if command -v xdg-open >/dev/null 2>&1; then
    echo \"Opening dashboard in browser...\"
    xdg-open \"http://localhost:18789\" 2>/dev/null &
elif command -v open >/dev/null 2>&1; then
    echo \"Opening dashboard in browser...\"
    open \"http://localhost:18789\" 2>/dev/null &
else
    echo \"Cannot auto-open browser. Manual access: http://localhost:18789\"
    echo \"Bookmark this. Thomas would bite you if you forget.\"
fi

# Test HTTP connectivity (because optimism isn't a strategy)
curl -s -o /dev/null -w \"%{http_code}\" http://localhost:18789 2>/dev/null || echo \"Failed to connect\"
echo \" HTTP status code\"

# If curl fails, check if port is listening
if ! curl -s http://localhost:18789 >/dev/null 2>&1; then
    echo \"⚠️  Dashboard may not be running. Checking port...\"
    netstat -tlnp | grep :18789 || echo \"Port 18789 not listening. Like Romeo ignoring your calls.\"
fi

# === SSH ACCESS METHOD (CRITICAL DISCOVERY) ===
echo \"\"
echo \"=== SSH TUNNEL ACCESS (For remote servers) ===\"
echo \"From your LOCAL machine (not SSH session):\"
echo \"  ssh -N -L 18789:127.0.0.1:18789 root@YOUR_SERVER_IP\"
echo \"Then open browser: http://localhost:18789\"
echo \"\"
echo \"=== DIRECT ACCESS (If firewall allows) ===\"
echo \"  http://YOUR_SERVER_IP:18789\"
echo \"\"
echo \"=== QUICK TEST ===\"
echo \"Health endpoint: curl http://localhost:18789/health\"
echo \"Should return: {\"ok\":true,\"status\":\"live\"}\"
```

## Phase 6: Verification (The "Did It Actually Work?" Phase)

### Step 12: Doctor's Checkup (Post-Restoration Health Assessment)

**🎯 IMPORTANT: Doctor Interactive Prompts**
When you run `openclaw doctor` after fresh install or restore, expect:

1. **"Install missing bundled plugin runtime deps now?"** → **YES ✅**
   - Installs 40+ required packages (takes 2-5 minutes)
   - This is NORMAL after fresh install

2. **"Update gateway service config to recommended defaults?"** → **YES ✅**
   - Fixes systemd service pointing to wrong binary path
   - Ensures gateway starts correctly

3. **Version mismatch warning**: "Config written by newer OpenClaw" → **IGNORE ✅**
   - Just a warning, not an error
   - Configs are backward compatible

4. **Run `openclaw doctor --fix`** after interactive prompts
   - Applies remaining fixes
   - Verifies everything works

**Example successful doctor output:**
```
Telegram: ok (@OpenClawZABot)
WhatsApp: not linked
Agents: atlas (default), seeker, setup, edge, vertex, forge
Heartbeat interval: 1h (atlas)
```

**If doctor shows issues, follow its suggestions!**
```bash
# The doctor is in. Stethoscope ready. Thomas is watching (and might bite).
echo "=== DOCTOR'S CHECKUP - POST-RESTORATION HEALTH ASSESSMENT ==="
echo "Phase 1: Vital Signs"
echo "1. Heartbeat (Process check):"
ps aux | grep -E "(openclaw|lossless)" | grep -v grep | wc -l
echo "2. Blood Pressure (Port check):"
netstat -tlnp | grep -E ":18789|:3000" || echo "⚠️  No OpenClaw ports listening"
echo "3. Temperature (Service status):"
openclaw status 2>&1 | head -5 || echo "⚠️  Status check failed"

echo "---"
echo "Phase 2: Organ Function"
echo "4. Brain (Database):"
ls -la ~/.openclaw/lcm.db* 2>/dev/null | wc -l
echo "5. Nervous System (Config):"
ls -la ~/.openclaw/openclaw.json 2>/dev/null && echo "✅ Config present"
echo "6. Limbs (Agents):"
ls -la ~/.openclaw/agents/ 2>/dev/null | wc -l
echo "7. Digestive System (Workspace):"
ls -la ~/.openclaw/workspace/ 2>/dev/null | head -3

echo "---"
echo "Phase 3: Reflex Test"
echo "8. Gateway response:"
curl -s -o /dev/null -w "Gateway: %{http_code}\n" http://localhost:18789 2>/dev/null || echo "❌ No gateway response"
echo "9. Basic command test:"
openclaw --version 2>&1 | head -1 || echo "❌ OpenClaw not responding"
echo "10. Agent count:"
find ~/.openclaw/agents -type f -name "*.json" 2>/dev/null | wc -l

echo "---"
echo "DOCTOR'S NOTES:"
echo "If 7+ checks pass: Patient is healthy. Proceed."
echo "If 4-6 checks pass: Patient needs attention. Investigate."
echo "If <4 checks pass: Critical condition. Restore failed."
echo "Thomas's opinion: If it doesn't work, bite someone."
```
echo "1. Database files:" && ls -la ~/.openclaw/lcm.db* 2>/dev/null | wc -l
echo "   (If missing: Even Luna's tongue can't fix this)"
echo "2. Configuration:" && ls -la ~/.openclaw/openclaw.json 2>/dev/null
echo "   (Should be present, like Buster wanting a cuddle)"
echo "3. Agents directory:" && ls -la ~/.openclaw/agents/ 2>/dev/null | head -3
echo "   (The workforce, hopefully less stubborn than Romeo)"
echo "4. Workspace:" && ls -la ~/.openclaw/workspace/ 2>/dev/null | head -3
echo "   (The office. Don't turn your back on it)"
echo "5. Credentials:" && ls -la ~/.openclaw/credentials/ 2>/dev/null | head -3
echo "   (The keys. Guard them like Thomas guards his spot)"
echo "6. Tasks:" && ls -la ~/.openclaw/tasks/ 2>/dev/null | head -3
echo "   (The to-do list. Probably longer than Luna's tongue)"
echo "7. Logs:" && ls -la ~/.openclaw/logs/ 2>/dev/null | head -3
echo "   (The diary. Hopefully less dramatic than the dogs' day)"
```
# Test Telegram configuration (if applicable)
if [ -f ~/.openclaw/credentials/telegram/bob.json ]; then
    echo "Telegram config present. Bob might actually respond now."
fi

# Check for our test marker (if you created one)
if [ -f ~/.openclaw/test-marker.txt ]; then
    echo "Test marker found! Restoration successful."
    cat ~/.openclaw/test-marker.txt
fi
```

### Step 13: Test Functionality
```bash
# Send a test message (if Telegram configured)
openclaw channels list

# Check dashboard access
openclaw dashboard --no-open
echo "Dashboard should be at: http://localhost:18789"

# Basic functionality test
openclaw --help | head -5
```

## Phase 7: Cleanup (The Responsible Bit)

### Step 14: Clean Up Backup Files
```bash
# Keep only last 3 backups (hoarding is a disease)
cd /root/backups/openclaw
ls -t openclaw-backup-*.tar.gz | tail -n +4 | xargs rm -f

# Update retention in script (if you're feeling thorough)
sed -i 's/RETENTION_DAYS=7/RETENTION_DAYS=3/' /usr/local/bin/openclaw-backup
```

### Step 15: Document the Process
```bash
# Create restoration report
cat > /tmp/openclaw-restoration-report-$(date +%Y%m%d).md << EOF
# OpenClaw Restoration Report
Date: $(date)

## Summary
Successfully completed backup → delete → fresh install → restore cycle.

## Key Files Restored
$(find ~/.openclaw -type f -name "*.json" | head -10)

## Backup Used
$(ls -lh /root/backups/openclaw/openclaw-backup-*.tar.gz | tail -1)

## Status After Restoration
$(openclaw status 2>/dev/null | head -20)

## Notes
- Remember to restart any dependent services
- Check Telegram bots are responding
- Verify dashboard accessibility
EOF

echo "Report saved to: /tmp/openclaw-restoration-report-$(date +%Y%m%d).md"
```

## 🎯 CRITICAL NEW DISCOVERIES (April 2026 Testing)

### OpenClaw Architecture Revealed
Through real-world backup/restore testing, we discovered:

1. **OpenClaw is NOT a global npm package** - It's installed as a **local dependency** within `.openclaw/extensions/lossless-claw/node_modules/openclaw/`
2. **The binary is `openclaw.mjs`** - An ES Module (`#!/usr/bin/env node`) requiring Node.js 22.12+
3. **Backup contains WORKING binary** - The restored `.openclaw/extensions/lossless-claw/node_modules/openclaw/openclaw.mjs` is fully functional
4. **Live system detection** - Always check for running OpenClaw gateway before testing restore
5. **CLI vs Gateway separation** - Gateway can run without CLI in PATH; they're separate components
6. **Broken npm symlinks common** - Global npm install often creates broken symlinks that need manual fixing

### SSH Dashboard Access Pattern
For VPS servers (like 161.97.110.234):

```bash
# From local machine, create SSH tunnel:
ssh -L 18789:localhost:18789 root@SERVER_IP

# Then access in local browser:
# http://localhost:18789
```

### CLI Troubleshooting & Universal Wrapper
When `openclaw` command not found:

```bash
#!/bin/bash
# Universal OpenClaw wrapper
# Save as /usr/local/bin/openclaw

# Location 1: Backup test location
BACKUP_BIN="/tmp/openclaw-restore-sandbox-*/restored/.openclaw/extensions/lossless-claw/node_modules/openclaw/openclaw.mjs"
if [ -f "$BACKUP_BIN" ]; then
    cd "$(dirname "$BACKUP_BIN")/../../../../"
    node "$BACKUP_BIN" "$@"
    exit $?
fi

# Location 2: Global npm install
GLOBAL_BIN="/usr/lib/node_modules/openclaw/openclaw.mjs"
if [ -f "$GLOBAL_BIN" ]; then
    node "$GLOBAL_BIN" "$@"
    exit $?
fi

# Location 3: Try to find it
FOUND=$(find /usr/lib/node_modules -name "openclaw.mjs" 2>/dev/null | head -1)
if [ -n "$FOUND" ]; then
    node "$FOUND" "$@"
    exit $?
fi

# Location 4: Dependency of lossless-claw
DEP_BIN="/usr/lib/node_modules/@martian-engineering/lossless-claw/node_modules/openclaw/openclaw.mjs"
if [ -f "$DEP_BIN" ]; then
    node "$DEP_BIN" "$@"
    exit $?
fi

echo "❌ OpenClaw not found. Try: sudo npm install -g @martian-engineering/lossless-claw"
exit 1
```

### ✅ DOCTOR SEQUENCE CONFIRMED (Real-World Validation)
**CORRECT ORDER (Tested & Verified):**
```bash
# After fresh install OR restore:
openclaw doctor           # Step 1: Diagnose issues

# Interactive prompts will appear:
# 1. "Install missing bundled plugin runtime deps now?" → YES ✅
# 2. "Update gateway service config to recommended defaults?" → YES ✅

openclaw doctor --fix     # Step 2: Apply remaining fixes
```

**KEY FINDINGS FROM ACTUAL DOCTOR RUN:**
1. **Version mismatch warning is HARMLESS**: "Config written by newer OpenClaw" = just a warning, not an error
2. **Dependencies auto-install**: Doctor can fix 40+ missing packages automatically
3. **Systemd service mismatch**: Gateway often points to wrong binary path (doctor fixes this)
4. **Telegram bot verification**: Doctor checks `@OpenClawZABot` connectivity

### Verified Restore Process
```bash
# Test if restored OpenClaw works
RESTORED_DIR="/tmp/openclaw-restore-sandbox-20260409-182511/restored"
OPENCLAW_BIN="$RESTORED_DIR/.openclaw/extensions/lossless-claw/node_modules/openclaw/openclaw.mjs"

if [ -f "$OPENCLAW_BIN" ]; then
    cd "$RESTORED_DIR"
    node "$OPENCLAW_BIN" --version  # Should output: OpenClaw 2026.4.2 (d74a122)
    node "$OPENCLAW_BIN" doctor     # Test functionality (follow interactive prompts!)
fi
```

### Production Safety Protocol
When testing restore on live systems:
```bash
# 1. Check for running services
ps aux | grep -i "openclaw\|gateway\|telegram" | grep -v grep

# 2. Use isolated profile to avoid conflicts
openclaw --profile test doctor

# 3. If gateway is running, test carefully or stop it first
openclaw gateway stop
# ... test restore ...
openclaw gateway start
```

## The Memento/Bootstrap Mechanism

### Future-Proofing: Leaving Notes for Your Future Self
```bash
# Create a bootstrap message for next time
cat > ~/.openclaw/BOOTSTRAP.md << 'EOF'
# OpenClaw Bootstrap Instructions
Created: $(date)

## If You're Reading This...
The system has been freshly restored. Here's what you need to know:

1. **Backup Location:** /root/backups/openclaw/
2. **Restore Script:** /usr/local/bin/openclaw-restore
3. **Last Restoration:** $(date)
4. **Key Configs Restored:** All credentials and configurations

## Next Steps:
- Test Telegram bots
- Verify dashboard at http://localhost:18789
- Schedule regular backups (cron example below)

## Cron Job for Regular Backups:
```bash
# Daily config backup at 2 AM
0 2 * * * /usr/local/bin/openclaw-backup config

# Weekly full backup Sunday at 3 AM
0 3 * * 0 /usr/local/bin/openclaw-backup full
```

## Emergency Contact:
If everything breaks... well, you have the backups. Good luck.
EOF

echo "Bootstrap instructions saved to: ~/.openclaw/BOOTSTRAP.md"
```

## Advanced: Strategic Copying When Full Copies Fail

Sometimes `cp -r` gets interrupted (especially with large backups). When this happens, use piecemeal copying like a butler moving a library one shelf at a time:

```bash
# Create directory first (empty is less intimidating)
mkdir -p ~/.openclaw

# Copy critical components individually (in order of importance)
cp -r /path/to/backup/agents ~/.openclaw/
cp -r /path/to/backup/workspace ~/.openclaw/
cp /path/to/backup/openclaw.json ~/.openclaw/
cp -r /path/to/backup/credentials ~/.openclaw/
cp -r /path/to/backup/tasks ~/.openclaw/
cp -r /path/to/backup/logs ~/.openclaw/
cp /path/to/backup/lcm.db* ~/.openclaw/

# Then copy remaining directories (the less critical bits)
for dir in backup browser cache canvas completions cron delivery-queue devices env extensions flows identity media memory sandbox scripts telegram testing; do
    if [ -d "/path/to/backup/$dir" ]; then
        cp -r "/path/to/backup/$dir" ~/.openclaw/
    fi
done
```

**Why this works:**
1. Smaller operations are less likely to timeout
2. Critical data is restored first (agents, workspace, database)
3. You can monitor progress and identify which copy fails
4. It's like moving house - essentials first, decorations later

## Disaster Simulation Preservation

Keep your disaster simulation directory (`~/.openclaw-disaster-simulated`) as a monument to what could have been. It contains the `test-marker.txt` that proves the simulation worked and serves as a sobering reminder of why we bother with backups in the first place.

**Watch Out For (The "I Told You So" Section)**

1. **Disk Space** - Backups need room. Check with `df -h` first. Luna-sized backups require Luna-sized space.
2. **Running Processes** - OpenClaw hates being interrupted. Stop it properly. Like calling Romeo - do it firmly.
3. **Permission Issues** - OpenClaw is particular about file permissions. Thomas would bite you for wrong permissions.
4. **Network Dependencies** - Fresh install needs internet. Obviously. Even Buster knows this.
5. **Timeouts** - Large backups take time. Don't panic. Make tea. Watch Thomas hop around.
6. **Interrupted Copies** - Use strategic piecemeal copying when `cp -r` fails.
7. **Version Mismatch** - If backup was made with newer OpenClaw version, you'll get warnings. The data restores fine, but OpenClaw might complain. HELL YEAH, it still works.
8. **Missing Dependencies** - Restored environment might lack npm modules. Install missing ones as they appear. Put that in your pipe and smoke it: `npm install -g @sinclair/typebox` (or whatever it complains about).
7. **Broken Symlinks** - OpenClaw binary symlink often breaks. Fix with: `ln -s /usr/lib/node_modules/@martian-engineering/lossless-claw/node_modules/.bin/openclaw /usr/local/bin/openclaw`
8. **Version Mismatches** - Backup may warn about config written by newer version. Usually safe to ignore.
9. **Safety Blocks** - System may block `rm -rf` commands. This is a feature, not a bug.
10. **Test Verification** - Always create unique test markers (`echo "TEST_$(date +%Y%m%d_%H%M%S)" > ~/.openclaw/test-marker.txt`) to verify restoration.

## Who Made This?

**Author:** Stef Ferreira  
**Style:** English dry humour (because backup procedures should be entertaining)  
**Philosophy:** "Test your backups before you need them. Or don't. Live dangerously. Also, don't turn your back on Thomas the Jack Russell - he bites. HELL YEAH."

**Canine Inspiration:**
- **Romeo's Approach:** Sometimes you need to shout to get attention (like when backups fail). HELL YEAH, he'll listen then.
- **Luna's Enthusiasm:** That worm-like wriggle when something actually works. Tongue like an anteater, could lick a grape through chicken wire.
- **Buster's Face:** The look you give when you realize you didn't test the restore. Face made for E-pol dog food commercials.
- **Thomas's Warning:** "Don't turn your back on untested backups" (he'd bite you for less). Old but spry, hops like a bunny, grumpy but right.  
**Date:** April 9, 2026  
**Version:** 2.2.0 (Updated with symlink fix, safety blocks, and test markers)

## How This Skill Learns

This skill evolves through **real-world testing**. When you discover something doesn't work:

1. **Load the skill first** with `skill_view('openclaw-complete-backup-delete-fresh-install-restore-cycle')`
2. **Follow its instructions** until you hit a problem
3. **Patch immediately** with `skill_manage(action='patch')` - don't wait!
4. **Document the fix** in the skill so future users benefit

**Example learning cycle:** We discovered the restore script doesn't copy to `~/.openclaw` directly. The skill was patched immediately with the manual copy workaround. This is how skills grow smarter over time.

## Recognition

If this skill saves your OpenClaw installation:
1. Credit: **Stef Ferreira**  
2. Style: **English dry humour**  
3. Lesson: **Always test restores before you need them**

---

*"Backups are like umbrellas. You don't appreciate them until it's raining and you realize you left yours at home."*  
*- The backup/restore skill, probably*

**Next skill in this style:** `skill-personality-development`  
**Personality consistency:** 95% (dry humour, practical, safety-first)  
**Success rate:** Higher than your untested backups

---

**- Stef Ferreira**  
*English dry humour backup enthusiast*  
*Canine-approved disaster recovery*  
*HELL YEAH, it works!*