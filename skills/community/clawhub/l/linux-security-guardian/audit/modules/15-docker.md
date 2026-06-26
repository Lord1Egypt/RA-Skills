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

### Exposed Container Ports
- Ports bound to 0.0.0.0 unexpectedly → cross-check with module 08

## Output Format
```
[CRITICAL] 15-docker: privileged_container | container: webapp | --privileged flag set
[CRITICAL] 15-docker: docker_socket_mounted | container: proxy | /var/run/docker.sock exposed
```
