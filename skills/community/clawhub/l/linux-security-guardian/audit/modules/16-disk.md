# Module 16 — Disk & Inode Usage

## Commands
```bash
df -h                          # disk usage human readable
df -i                          # inode usage
df -h | awk 'NR>1 {gsub(/%/,""); if ($5+0 > 80) print $0}'  # > 80% used

# Find largest files
find / -xdev -type f -size +100M 2>/dev/null | head -20

# Large files in /var/log (log bloat)
find /var/log -type f -size +50M 2>/dev/null

# /tmp size
du -sh /tmp 2>/dev/null
```

## Thresholds
- > 80% → LOW
- > 85% → MEDIUM
- > 90% → HIGH
- > 95% → CRITICAL auto-alert

## Inode Exhaustion
- > 85% inodes used → HIGH (can block new file creation even if disk space free)

## Output Format
```
[HIGH] 16-disk: disk_usage | /var/log: 91% full | largest: /var/log/syslog (2.1GB)
[PASS] 16-disk: root_partition | 45% used
```
