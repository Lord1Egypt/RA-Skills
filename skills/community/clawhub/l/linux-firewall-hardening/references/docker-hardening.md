# Docker Firewall Hardening

Docker manipulates iptables/nftables directly. By default, `dockerd` inserts rules **above** ufw in the FORWARD chain, meaning `docker run -p` exposes containers to the world even when ufw INPUT policy is DROP.

## Detection

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
sudo iptables -L DOCKER -n -v 2>/dev/null     # Docker-managed NAT rules
sudo iptables -L DOCKER-USER -n -v 2>/dev/null # User chain (may be empty)

# Check for unintended 0.0.0.0 exposure
docker inspect $(docker ps -q) --format '{{.Name}}: {{range $p, $c := .NetworkSettings.Ports}}{{$p}} -> {{(index $c 0).HostIp}}:{{(index $c 0).HostPort}} {{end}}' 2>/dev/null | grep "0.0.0.0"
```

## Key Principle

Docker manages its own chains (DOCKER, DOCKER-ISOLATION-STAGE-\*) for container NAT and inter-container communication. **Do NOT modify those chains directly.** Use the DOCKER-USER chain which Docker guarantees it will never touch.

## Mitigation Options

### Option A: DOCKER-USER Chain (RECOMMENDED)

The DOCKER-USER chain is evaluated BEFORE Docker's own rules but only affects the FORWARD chain. Use it to restrict which external interfaces can reach published ports:

```bash
# Block all external access to published ports on eth0 (public interface)
sudo iptables -C DOCKER-USER -i eth0 -j DROP 2>/dev/null || \
  sudo iptables -I DOCKER-USER 1 -i eth0 -j DROP

# Allow external HTTPS to reach containers
sudo iptables -C DOCKER-USER -i eth0 -p tcp --dport 443 -j ACCEPT 2>/dev/null || \
  sudo iptables -I DOCKER-USER 2 -i eth0 -p tcp --dport 443 -j ACCEPT

# Persist DOCKER-USER rules
sudo iptables-save | grep DOCKER-USER | sudo tee /etc/iptables/docker-user.rules
```

### Option B: Bind Published Ports to Specific IPs

Instead of `-p 8080:8080` (binds `0.0.0.0`):
```bash
docker run -p 127.0.0.1:8080:8080 myapp   # Loopback only
docker run -p 10.0.1.10:8080:8080 myapp    # Internal IP only
```

### Option C: Disable Docker's iptables Management

Edit `/etc/docker/daemon.json`:
```json
{ "iptables": false }
```
Then `sudo systemctl restart docker`.

**WARNING**: Makes you fully responsible for all NAT, port mapping, inter-container communication, and outbound masquerading rules.

## Docker + nftables Hosts

On hosts where nftables is the primary backend but Docker still uses iptables (legacy mode), the two systems coexist but do not share state. Docker's iptables rules are invisible to `nft list ruleset`. Always check both:
```bash
sudo iptables -L -n -v | grep -i docker
sudo nft list ruleset | grep -i docker  # will likely be empty
```
