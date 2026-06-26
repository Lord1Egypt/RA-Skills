# Archetype: Linux + systemd

The default archetype. Covers most servers: Debian/Ubuntu/Arch/Fedora/RHEL with a normal systemd setup.

## When to use this archetype

- Standard Linux server with systemd
- Reachable via SSH (password or key)
- Has typical CLI tools: `uptime`, `free`, `df`, `systemctl`

## YAML

```yaml
- name: web-server
  address: 192.0.2.20
  auth: ssh-pass
  user: admin
  password_env: HEARTH_PASS_WEB
  services: [ssh, nginx, fail2ban]
  apps:
    - name: web
      type: http
      url: http://web-server.lan/
      expect_code: 200
```

For SSH-key auth instead of password:

```yaml
  auth: ssh-key
  user: admin
  key_path: ~/.ssh/id_ed25519
```

## What the 5 layers will show

```
=== 192.0.2.20 web-server ===
  L1 ping:    OK
  L2 uptime:  3 days, 4 hours, load: 0.12 0.08 0.05
  L3 mem:     used 1.2Gi / 4.0Gi, 2.5Gi avail | disk: / 23% used, 75G free
  L4 svc:     ssh=active nginx=active fail2ban=active
  L5 app:     web=HTTP 200
```

## Tweaks

- **Many services to check**: list them all in `services:`. Order doesn't matter.
- **Service has a non-obvious unit name**: check on the device with `systemctl list-units --type=service | grep -i <name>` first.
- **Wired+Wi-Fi failover host**: hearth doesn't care — it probes the IP you provide. Document the failover IP in your YAML as a comment.

## Common services to monitor

| Role | Typical services |
|------|------------------|
| Web server | `ssh nginx fail2ban` or `ssh apache2 fail2ban` |
| Mail server | `ssh postfix dovecot fail2ban` |
| DNS server | `ssh bind9` or `ssh unbound` |
| Database | `ssh mariadb` or `ssh postgresql` |
| Caching | `ssh redis-server memcached` |
| Container host | `ssh docker containerd` |
| Tailscale node | append `tailscaled` to whatever else is running |