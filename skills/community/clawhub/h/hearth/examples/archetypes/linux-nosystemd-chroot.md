# Archetype: Linux without systemd (chroot, Termux, Alpine OpenRC)

For devices that have a Linux userspace but not systemd. Common cases:

- Kali NetHunter chroot on Android
- Termux on Android
- Alpine Linux with OpenRC
- A chroot or container that isn't running PID 1 init

## When to use this archetype

- The user can SSH in and get a working shell with `uptime`, `free`, `df`
- `systemctl is-active` is either missing or returns nonsense
- L4 service-state checks are not meaningful

## YAML

```yaml
- name: phone-pentest
  address: 192.0.2.50
  auth: ssh-pass
  user: kali
  password_env: HEARTH_PASS_PHONE
  ssh_connect_timeout: 8        # mobile networks are slow
  ssh_warmup: true              # first SSH usually times out, retry
  no_systemd: true              # report "no-systemd (chroot — N/A)" for L4
  apps:
    - name: tool-present
      type: command
      command: 'test -x /usr/bin/nmap && echo present || echo MISSING'
      expect_match: '^present$'
    - name: tailscale
      type: command
      command: 'tailscale --socket=/var/run/tailscale/tailscaled.sock ip -4'
      expect_match: '^100\.'
```

## What the 5 layers will show

```
=== 192.0.2.50 phone-pentest ===
  L1 ping:    OK
  L2 uptime:  1 week, 6 days, 20 hours, load: 1.32 1.51 1.72
  L3 mem:     used 3.1Gi / 5.2Gi, 2.1Gi avail | disk: / 61% used, 42G free
  L4 svc:     no-systemd (chroot — N/A)
  L5 app:     tool-present=OK (present) | tailscale=OK (100.64.0.10)
```

## Tweaks

- **High latency**: bump `ssh_connect_timeout` to 8-12. Mobile networks vary widely.
- **Phone sleeps**: `ssh_warmup: true` does a throwaway SSH first to wake the device, ignores the inevitable failure, then runs the real probe on the second attempt.
- **No systemd, BUT some services**: some chroots run things like sshd via init scripts. You can use `type: command` with `pgrep -x sshd` instead of relying on systemctl.

## Tailscale in userspace mode

Chroots can't get a TUN device, so Tailscale runs in userspace networking mode with an explicit socket. The probe must include the socket path:

```yaml
command: 'tailscale --socket=/var/run/tailscale/tailscaled.sock ip -4'
```