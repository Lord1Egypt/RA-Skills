# System Administration

## System Info
- OS: Debian Bookworm (slim)
- Runtime: Node.js v22, Python 3, Go
- Volume: /root (snapshots-backed)

## Common Operations

### Process Management
```bash
ps aux | grep process_name
top -bn1 | head -20
kill PID
systemctl status service_name
journalctl -u service_name -f
```

### Disk & Storage
```bash
df -h                    # Disk usage
du -sh /path/*           # Directory sizes
ncdu /path               # Interactive disk usage
lsblk                    # Block devices
```

### Network
```bash
ss -tlnp                 # Listening ports
ip addr                  # Network interfaces
curl -I url              # HTTP headers
dig domain               # DNS lookup
traceroute host          # Route tracing
```

### File Operations
```bash
find /path -name "*.log" -mtime +7    # Old log files
rsync -avz source/ dest/               # Sync directories
tar -czf archive.tar.gz /path         # Create archive
chmod 755 script.sh                    # Permissions
chown user:group file                  # Ownership
```

### Package Management
```bash
apt update && apt upgrade             # System update
apt install package                   # Install
apt search keyword                    # Search
dpkg -l | grep package               # Check installed
```

## Monitoring
- **healthcheck** skill for security audits
- Cron-based health checks
- Log rotation and cleanup
- Resource usage alerts

## Backup Strategy
- Workspace volume has snapshot support
- Regular git commits for code
- Export databases regularly
- Document backup locations

## Service Management
- Supervisor for process management
- Systemd for system services
- Docker for containerized services
- Nginx/Caddy for web serving

## Troubleshooting
1. Check logs first: `journalctl`, app logs
2. Verify network: `ss`, `curl`, `ping`
3. Check resources: `df -h`, `free -h`, `top`
4. Review recent changes: `history`, git log
5. Test in isolation before applying fix
