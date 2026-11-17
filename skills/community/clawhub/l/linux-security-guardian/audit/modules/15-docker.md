# Module 15 — Docker Security (if running)

## Check if Docker present
```bash
which docker >/dev/null 2>&1 || { echo "Docker not installed — module skip"; exit 0; }
systemctl is-active docker >/dev/null 2>&1 || { echo "Docker not running — module skip"; exit 0; }
```

## Commands
```bash
# Docker version (check if up to date)
docker version 2>/dev/null

# Running containers
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null

# All containers including stopped
docker ps -a 2>/dev/null

# Containers running as root
docker inspect $(docker ps -q) 2>/dev/null | python3 -c "
import json,sys
for c in json.load(sys.stdin):
  user = c['Config']['User']
  name = c['Name']
  if not user or user == 'root':
    print(f'ROOT CONTAINER: {name}')
"

# Privileged containers (CRITICAL)
docker inspect $(docker ps -q) 2>/dev/null | python3 -c "
import json,sys
for c in json.load(sys.stdin):
  if c['HostConfig']['Privileged']:
    print(f'PRIVILEGED: {c[\"Name\"]}')
"

# Containers with host network mode
docker inspect $(docker ps -q) 2>/dev/null | python3 -c "
import json,sys
for c in json.load(sys.stdin):
  if c['HostConfig']['NetworkMode'] == 'host':
    print(f'HOST_NETWORK: {c[\"Name\"]}')
"

# Check Docker socket exposure
docker inspect $(docker ps -q) 2>/dev/null | grep -i "docker.sock"

# Docker daemon config
cat /etc/docker/daemon.json 2>/dev/null
```

## Checks & Findings

### Privileged Containers
- Any container with --privileged → CRITICAL (full host access)

### Containers Running as Root
- Container with no USER set → MEDIUM

### Docker Socket Mounted
- /var/run/docker.sock mounted in container → CRITICAL (container escape)

### Host Network Mode
- Container with --network host → HIGH

### Docker Version
- Check against latest stable
- > 3 major versions behind → HIGH

### Docker Daemon Security Defaults (daemon.json)
Check /etc/docker/daemon.json for security settings:
```bash
cat /etc/docker/daemon.json 2>/dev/null || echo "{} or not found"
```

#### Checks
| Parameter | Secure Value | Severity if Missing/Wrong |
|-----------|-------------|--------------------------|
| userns-remap | "default" or a dedicated user | HIGH (containers run as root by default) |
| no-new-privileges | true | MEDIUM (prevents privilege escalation via suid) |
| seccomp-profile | /etc/docker/seccomp.json or "default" | MEDIUM (seccomp restricts syscalls) |
| live-restore | true | LOW (containers survive daemon restart) |
| log-driver | "json-file" or "journald" | LOW (no logging = no forensics) |
| log-opts.max-size | "10m" | LOW (unbounded logs fill disk) |
| log-opts.max-file | "3" | LOW |
| icc (inter-container comms) | false (unless needed) | MEDIUM |
| iptables | true | HIGH (Docker manages its own firewall rules) |
| ip-forward | true (if Docker needs it) | LOW |
| bip (bridge IP) | custom private range | LOW (default 172.17.0.1/16 is fine) |
| default-ulimits | set (nofile, nproc) | LOW |
| exec-opts | native.cgroupdriver=systemd | MEDIUM (cgroupfs vs systemd) |

#### Recommended daemon.json
```json
{
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "icc": false,
  "iptables": true,
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

#### ⚠️ Important: userns-remap implications
- Enabling userns-remap remaps UIDs/GIDs inside containers
- Existing container volumes may have permission issues after enabling
- Requires Docker daemon restart
- Confirm required before applying

#### Output Format (daemon.json)
```
[HIGH] 15-docker: daemon_userns_remap | userns-remap: not set | containers run as root | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 15-docker: daemon_no_new_privs | no-new-privileges: not set | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 15-docker: daemon_seccomp | seccomp-profile: not set | action_id: ACT-YYYYMMDD-XXX
[PASS] 15-docker: daemon_live_restore | live-restore: true ✓
```

### Exposed Container Ports
- Ports bound to 0.0.0.0 unexpectedly → cross-check with module 08

## Output Format
```
[CRITICAL] 15-docker: privileged_container | container: webapp | --privileged flag set
[CRITICAL] 15-docker: docker_socket_mounted | container: proxy | /var/run/docker.sock exposed
```
