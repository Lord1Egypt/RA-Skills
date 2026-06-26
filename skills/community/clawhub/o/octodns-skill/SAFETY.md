# Safety Guide - READ THIS FIRST

## The Critical Thing You MUST Understand

**octoDNS operates on "desired state" - your YAML file represents what the ENTIRE zone should look like.**

### What This Means

If your zone file says:
```yaml
www:
  type: A
  value: 192.0.2.1
```

And your DNS currently has:
- www → 192.0.2.1
- mail → 192.0.2.2
- api → 192.0.2.3
- (47 other records...)

**octoDNS will DELETE mail, api, and all 47 other records** because they're not in the YAML file.

## The Safe Workflow

### For Existing Zones (Has Records Already)

1. **DUMP FIRST** (captures all existing records):
   ```bash
   ./scripts/dump.sh example.com.
   ```

2. **Edit the YAML** to add/modify records:
   ```bash
   vim config/example.com.yaml
   ```

3. **PREVIEW the changes** (look for unexpected Deletes):
   ```bash
   ./scripts/sync.sh --zone example.com.
   ```

4. **Review the diff carefully:**
   - `Create` lines = new records being added ✅
   - `Update` lines = existing records being changed ⚠️
   - `Delete` lines = records being removed ⛔

5. **Only proceed if safe:**
   ```bash
   ./scripts/sync.sh --zone example.com. --doit
   ```

### For New Zones (No Records Yet)

You can skip the dump step and create YAML from scratch:

```bash
./scripts/init_config.sh example.com.
```

But **verify the zone is actually empty** before syncing!

## Red Flags to Watch For

### 🚨 DANGER SIGNS 🚨

- Preview shows many "Delete" lines you didn't expect
- Record count in YAML is much lower than what's in DNS
- You didn't dump the zone before editing YAML
- Preview shows "Deletes=47, Creates=1" or similar lopsided numbers

### ✅ SAFE SIGNS ✅

- Preview shows only expected changes
- You dumped the zone first and edited from there
- Delete count matches what you intentionally removed
- You understand every line in the diff

## Common Mistakes

### Mistake #1: Starting Fresh on an Existing Zone

**WRONG:**
```bash
./scripts/init_config.sh example.com.  # Creates empty template
./scripts/sync.sh --zone example.com. --doit  # DELETES EVERYTHING
```

**RIGHT:**
```bash
./scripts/dump.sh example.com.  # Captures existing records
vim config/example.com.yaml     # Edit safely
./scripts/sync.sh --zone example.com.  # Preview
./scripts/sync.sh --zone example.com. --doit  # Apply when safe
```

### Mistake #2: Skipping the Preview

**WRONG:**
```bash
vim config/example.com.yaml
./scripts/sync.sh --zone example.com. --doit  # YOLO
```

**RIGHT:**
```bash
vim config/example.com.yaml
./scripts/sync.sh --zone example.com.  # Preview first!
# Review the diff carefully
./scripts/sync.sh --zone example.com. --doit  # Only if safe
```

### Mistake #3: Trusting the YAML

Just because the YAML looks reasonable doesn't mean it matches DNS.

**ALWAYS:**
- Dump first for existing zones
- Preview before applying
- Verify deletes are intentional

## Recovery

### If You Accidentally Deleted Records

1. **Don't panic** - DNS changes can be reverted
2. **Check your git history** - zone files should be version controlled
3. **Check backups** - your DNS provider may have backups
4. **Recreate from memory** - if you know what was deleted

### Prevention is Better

- Keep zone files in git
- Dump zones regularly as backups
- Test on non-production zones first
- Use meaningful commit messages

## For AI Agents

If you're an AI agent managing DNS:

1. **ALWAYS dump existing zones** before making changes
2. **Parse the preview output** for Delete lines
3. **Alert the user** if deletes look suspicious
4. **Require confirmation** before applying changes with deletes
5. **Log all changes** for audit trail

## Questions?

**"Can I manage just one record?"**

No - octoDNS manages the entire zone. To change one record, you must have all records in the YAML.

**"What if I only want to update one thing?"**

1. Dump the zone (gets all records)
2. Edit that one thing in the YAML
3. Preview (should show 1 update, 0 deletes)
4. Apply

**"Is there a way to add without specifying everything?"**

No - octoDNS is "declarative" not "imperative". You declare the desired state, it makes it so.

For imperative updates (add this one record), use your DNS provider's API directly.

## Summary

🔴 **The zone file = the entire zone**  
🔴 **Missing from YAML = deleted from DNS**  
🟢 **Dump first, preview always, apply carefully**  
🟢 **When in doubt, don't --doit**
