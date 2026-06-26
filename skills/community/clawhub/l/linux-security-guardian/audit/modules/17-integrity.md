# Module 17 — File Integrity (AIDE/Tripwire)

## Commands
```bash
# Check if AIDE installed
which aide >/dev/null 2>&1 && echo "aide_available" || echo "aide_not_installed"

# Run AIDE check (read-only)
aide --check 2>/dev/null | tail -30

# Check if tripwire installed
which tripwire >/dev/null 2>&1 && tripwire --check 2>/dev/null | tail -20

# If neither installed — basic check
# Compare key binary hashes against last known (from BASELINE.md)
for f in /bin/ls /bin/ps /usr/bin/sudo /bin/login /usr/bin/passwd; do
  sha256sum $f 2>/dev/null
done
```

## Checks & Findings

### AIDE/Tripwire Not Installed
- Neither installed → MEDIUM (recommend installation)

### AIDE Violations
- Modified system files → HIGH (possible rootkit/compromise)
- New unexpected files in /bin /sbin /usr/bin → HIGH

### Binary Hash Check
- If BASELINE.md has hashes: compare current vs baseline
- Any mismatch → CRITICAL

## Output Format
```
[HIGH] 17-integrity: aide_violation | modified: /usr/bin/sudo | unexpected change
[MEDIUM] 17-integrity: aide_not_installed | recommend: apt install aide
```
