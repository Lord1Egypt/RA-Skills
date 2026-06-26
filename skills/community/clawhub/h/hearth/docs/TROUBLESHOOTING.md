# Troubleshooting

Common issues you'll hit running hearth.

## "no devices.yaml found"

```
ERROR: no devices.yaml found.
```

hearth looks in three places, in order:
1. `$HEARTH_CONFIG` if set
2. `~/.hearth/devices.yaml`
3. `./devices.yaml` (CWD)

Fix: `cp examples/devices.example.yaml ~/.hearth/devices.yaml` and edit.

## "no YAML parser available"

```
ERROR: no YAML parser available. Install yq or python3-yaml.
```

hearth needs either `yq` (mikefarah's, written in Go) or Python 3 with PyYAML.

```bash
# Option 1 — yq (recommended)
# Linux: download binary from https://github.com/mikefarah/yq/releases
# macOS: brew install yq
# Termux: pkg install yq

# Option 2 — Python with PyYAML
sudo apt-get install python3-yaml      # Debian/Ubuntu
brew install pyyaml                     # macOS
pkg install python-yaml                 # Termux
pip3 install pyyaml                     # any platform
```

## SSH FAILED on first try, succeeds on second

Common with chroots and mobile devices. The first SSH attempt times out as the device wakes; the second succeeds.

```yaml
- name: phone-pentest
  ssh_warmup: true        # add this
  ssh_connect_timeout: 8  # bump this
```

`ssh_warmup: true` does a throwaway SSH first (and ignores the failure), then sleeps 2 seconds, then runs the real probe.

## "tailscale: command not found" but it's installed

The SSH user's PATH may not include `/usr/bin` or `/usr/sbin`. Fix one of:

- Use full path in the probe: `command: '/usr/bin/tailscale ip -4'`
- Add `/usr/bin` to the user's `~/.bashrc` PATH
- For chroots running tailscale in userspace mode, the socket path is non-default:
  ```yaml
  command: 'tailscale --socket=/var/run/tailscale/tailscaled.sock ip -4'
  ```

## L4 says service is `inactive` but I know it's running

The unit name in your `services:` list doesn't match the actual systemd unit. Check on the device:

```bash
systemctl list-units --type=service --state=running | grep -i <your-service>
```

Common naming gotchas:
- `nginx.service` not `nginx-server`
- `mariadb.service` not `mysql`
- `php-fpm@<version>.service` (e.g. `php8.4-fpm`) not just `php-fpm` on multi-version installs

## L1 OK, L2-L4 say "SSH FAILED"

The host is reachable but SSH is unresponsive. Possibilities:

1. **sshd not running** — `systemctl status sshd` from the device's console
2. **fail2ban banned your bridgehead** — check `fail2ban-client status sshd` on the device, unban with `fail2ban-client set sshd unbanip <bridgehead-ip>`
3. **MaxStartups exhausted** — too many simultaneous SSH attempts. Sweep one device at a time: `./scripts/sweep.sh --device <name>`
4. **Wrong user/password/key** — test manually: `sshpass -p "$HEARTH_PASS_X" ssh user@host`

## L5 HTTP probe shows `HTTP 000`

`000` is curl-speak for "couldn't connect at all". Possibilities:

- App is down — check the daemon at L4
- Port is closed — check firewall on the device
- Wrong URL/port — `curl -v <url>` from the bridgehead
- TLS handshake failed — try `verify_tls: false` in the YAML

## L5 HTTP probe shows `HTTP 502 / 503`

The reverse proxy (nginx/apache) is up but the upstream app is broken. Check the app's own logs.

## L5 HTTP probe shows `HTTP 401 / 403`

Auth is wrong. Either:

- The bearer token in the env var is expired/revoked
- The `auth_header_env` field doesn't match the actual env var name
- The endpoint doesn't accept Bearer auth (some need API key in a custom header — out of scope for the simple HTTP probe; use a `command` probe with a custom curl invocation)

## Sweep takes much longer than expected

Each device has a `device_timeout` (default 18s). 10 devices ≈ 14s sweep when all healthy.

If your sweep takes 30s+, isolate the slow one:

```bash
time ./scripts/sweep.sh --device device-1
time ./scripts/sweep.sh --device device-2
# etc — find which device is slow
```

Causes of slow probes:
- High latency to the device (mobile Wi-Fi, distant VPN)
- Slow `systemctl is-active` calls (unusual but possible on overloaded systems)
- Slow command probes (e.g. Magento `indexer:status` can take 5-10 seconds)

Bump `device_timeout` for that one device:

```yaml
- name: web-stack
  device_timeout: 25
```

## "device_timeout" firing on a device I want to be patient with

```yaml
- name: slow-device
  device_timeout: 30        # up from default 18
  ssh_connect_timeout: 10   # up from default 4
```

## sweep.sh hangs

This shouldn't happen — every device has its own `timeout` wrapper. If it does:

1. Hit Ctrl-C and post the issue
2. Include: which device was being probed when it hung, its `auth` type, and its `apps:` list

## hearth shows green but the device is actually broken

You probably need to add an L5 probe specific to the broken thing. The 5 layers catch generic problems; app-specific brokenness needs an app-specific check.

Example: a Magento server's Apache is up (L4 green) and `/` returns HTTP 200 (L5 generic), but the search index is corrupted and search queries return 500. Add:

```yaml
- name: search-works
  type: http
  url: 'https://shop.example.com/catalogsearch/result/?q=test'
  expect_code: 200
```

## Output is ugly / has weird characters

If you see `^[[31;1m` style escape codes, your terminal isn't interpreting ANSI colour codes correctly. hearth itself doesn't emit colours, but tools it calls might. Pipe through `cat -v` or `sed 's/\x1b\[[0-9;]*m//g'` to strip.

## Got something not in this list?

Open an issue at https://github.com/nj070574-gif/hearth/issues — please include:
- Your platform (`uname -a`)
- Your hearth version (`./scripts/sweep.sh --version`)
- The device archetype that's misbehaving
- A SANITISED excerpt of your `devices.yaml` (no real IPs, hostnames, tokens)
- The exact output you got
- The output you expected