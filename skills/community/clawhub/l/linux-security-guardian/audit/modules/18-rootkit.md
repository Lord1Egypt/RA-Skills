# Module 18 — Rootkit Detection

## Commands
```bash
# rkhunter
which rkhunter >/dev/null 2>&1 && rkhunter --check --skip-keypress --report-warnings-only 2>/dev/null

# chkrootkit
which chkrootkit >/dev/null 2>&1 && chkrootkit 2>/dev/null | grep -v "not found\|not tested\| not \| OK"

# If neither: manual checks
# Hidden processes (compare /proc vs ps)
ls /proc | grep -E "^[0-9]+$" | wc -l
ps aux | wc -l

# Suspicious network listeners not in ss output
cat /proc/net/tcp 2>/dev/null | awk '{print $2}' | while read h; do
  printf '%d.%d.%d.%d:%d\n' $(echo $h | sed 's/\(..\)\(..\)\(..\)\(..\):\(....\)/0x\4 0x\3 0x\2 0x\1 0x\5/' | xargs printf '%d %d %d %d %d')
done 2>/dev/null | head -20

# Check for common rootkit files
for f in /dev/.udev /dev/.static /usr/lib/libsh /usr/lib/.sshd /tmp/.ICE-unix /tmp/.font-unix; do
  [ -e "$f" ] && echo "SUSPICIOUS: $f"
done

# Kernel module check
lsmod 2>/dev/null
# Look for unsigned or unexpected modules
```

## Checks & Findings

### rkhunter/chkrootkit Warnings
- Any warning → HIGH (investigate immediately)
- Rootkit detected → CRITICAL (emergency response needed)

### Tools Not Installed
- Neither rkhunter nor chkrootkit → MEDIUM (blind spot)

### Suspicious Files
- Any known rootkit file paths found → CRITICAL

### Hidden Process Indicator
- /proc count vs ps count mismatch → HIGH

## Output Format
```
[CRITICAL] 18-rootkit: rkhunter_warning | warning: Suspicious file /usr/bin/s3 — possible rootkit
[MEDIUM] 18-rootkit: no_tools | rkhunter and chkrootkit not installed
```
