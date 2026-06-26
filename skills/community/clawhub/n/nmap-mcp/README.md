# nmap-mcp

> An nmap MCP server for AI-assisted network security auditing.

A [Model Context Protocol](https://modelcontextprotocol.io) server that wraps [nmap](https://nmap.org) with **14 purpose-built tools**, returning **structured JSON output** instead of raw text — so your AI agent can actually reason about what it finds.

Built for use with [OpenClaw](https://openclaw.ai) and compatible with any MCP client.

---

## Why this one?

Most nmap MCP servers dump raw nmap text back at the model. This one parses everything into structured JSON, so you get machine-readable port lists, service versions, OS matches, and script output — not walls of text to squint at.

It also ships with things you actually need for responsible security tooling:

- **Scope enforcement** — CIDR allowlist, configured in `config.yaml`. Targets outside your allowed ranges are rejected before nmap runs and logged. No accidental scans of the public internet.
- **Audit logging** — every tool call is logged as a JSON line: timestamp, tool, target, args, success/fail.
- **Scan persistence** — every result is saved to disk with a `scan_id`. Retrieve any past scan cross-session with `nmap_get_scan`.
- **Injection guard** — `nmap_custom_scan` strips shell metacharacters before they touch a subprocess.
- **Privilege-aware** — SYN, OS, and ARP scans need raw socket access. The README tells you the one command to set it up cleanly (`setcap`), no full root required.

---

## Requirements

- [OpenClaw](https://openclaw.ai) — the MCP-native AI agent runtime this is built for
- [mcporter](https://mcporter.dev) — MCP server manager (`npm install -g mcporter`); not bundled with OpenClaw, needs separate install
- Python 3.10+
- nmap 7.0+ installed and in PATH
- `fastmcp`, `python-nmap`, `pyyaml` (see `requirements.txt`)

---

## Installation

### Option A — ClawHub (recommended)

The easiest way if you're already using OpenClaw:

```bash
# Install the ClawHub CLI if you haven't already
npm i -g clawhub

# Install the skill
clawhub install nmap-mcp
```

Files land in `~/.openclaw/workspace/skills/nmap-mcp/`. Then follow the [Post-install setup](#post-install-setup) steps below.

### Option B — GitHub

```bash
git clone https://github.com/sbmilburn/nmap-mcp.git
cd nmap-mcp
```

Then follow the [Post-install setup](#post-install-setup) steps below.

---

### Post-install setup

#### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 2. Grant nmap raw socket capability

Required for SYN scans, OS detection, and ARP discovery. Only needs to be done once (redo after nmap upgrades):

```bash
sudo setcap cap_net_raw+ep $(which nmap)

# Verify
getcap $(which nmap)
# /usr/bin/nmap cap_net_raw=ep
```

> **Why `setcap` instead of `sudo`?** It gives nmap exactly the capability it needs (raw sockets) without running the whole process as root. Cleaner and less risky than a sudoers rule.

#### 3. Configure scope

Edit `config.yaml` and set your allowed CIDRs before running:

```yaml
allowed_cidrs:
  - "127.0.0.0/8"         # loopback (always useful for testing)
  - "192.168.1.0/24"      # your local network
  - "10.0.0.0/8"          # internal RFC1918 — trim to your actual range

audit_log: "./audit.log"
scan_dir: "./scans"
nmap_bin: "/usr/bin/nmap"

timeouts:
  quick: 120
  standard: 300
  deep: 600
```

---

## Register with mcporter (OpenClaw)

### 1. Install mcporter (if you haven't already)

mcporter is a separate package — not bundled with OpenClaw:

```bash
npm install -g mcporter
```

Verify: `mcporter list` should run without errors.

### 2. Add nmap-mcp to mcporter's config

Edit (or create) `~/.mcporter/mcporter.json`:

```json
{
  "mcpServers": {
    "nmap": {
      "command": "python3",
      "args": ["-u", "/path/to/nmap-mcp/server.py"],
      "type": "stdio",
      "env": {
        "NMAP_CONFIG": "/path/to/nmap-mcp/config.yaml"
      }
    }
  }
}
```

Replace `/path/to/nmap-mcp/` with the actual path to the skill:
- **ClawHub install:** `~/.openclaw/workspace/skills/nmap-mcp/`
- **GitHub clone:** wherever you ran `git clone`

If `mcporter.json` already exists with other servers, add just the `"nmap": { ... }` block inside `"mcpServers"` — don't replace the whole file.

### 3. Restart OpenClaw

OpenClaw reads `mcporter.json` at startup. After restarting, verify the tools loaded:

```bash
npx mcporter list nmap
```

You should see all 14 tools listed. If you see an error, check that `python3` is in your PATH and that `fastmcp` is installed (`pip install fastmcp`).

---

## Tools

### Host Discovery

| Tool | Description | Needs cap_net_raw |
|------|-------------|:-----------------:|
| `nmap_ping_scan(target)` | ICMP + TCP ping sweep, no port scan | No |
| `nmap_arp_discovery(target)` | ARP discovery — most reliable on LAN, returns MAC+vendor | Yes |

### Port Scanning

| Tool | Description | Needs cap_net_raw |
|------|-------------|:-----------------:|
| `nmap_top_ports(target, count=100)` | Fast TCP connect scan of N most common ports | No |
| `nmap_syn_scan(target, ports="1-1024")` | SYN half-open scan — faster and stealthier | Yes |
| `nmap_tcp_scan(target, ports="1-1024")` | Full TCP connect scan — no special privileges | No |
| `nmap_udp_scan(target, ports="...")` | UDP scan — finds SNMP, DNS, NTP, TFTP, etc. | Yes |

### Service & OS Detection

| Tool | Description | Needs cap_net_raw |
|------|-------------|:-----------------:|
| `nmap_service_detection(target, ports, intensity=7)` | Service name, product, version, CPE | No |
| `nmap_os_detection(target)` | OS fingerprinting with accuracy % | Yes |

### NSE Scripts

| Tool | Description | Needs cap_net_raw |
|------|-------------|:-----------------:|
| `nmap_script_scan(target, scripts, ports)` | Run named NSE scripts, e.g. `ssl-cert,http-title` | No |
| `nmap_vuln_scan(target, ports)` | Full `vuln` NSE category — checks CVEs + misconfigs | No |

### All-in-One & Utilities

| Tool | Description | Needs cap_net_raw |
|------|-------------|:-----------------:|
| `nmap_full_recon(target, ports)` | SYN + service + OS + default scripts combined | Yes |
| `nmap_custom_scan(target, flags)` | Arbitrary flags, still scope-checked and logged | Varies |
| `nmap_list_scans(limit=20)` | List recent saved scans | No |
| `nmap_get_scan(scan_id)` | Retrieve full result of any past scan | No |

---

## Usage with OpenClaw

Just ask naturally — OpenClaw picks the right tool and runs it:

> *"Scan 10.35.251.0/24 for open ports"*

> *"Run a full recon on 10.35.251.10"*

> *"What services are running on 10.35.251.50?"*

> *"Check 10.35.251.25 for known vulnerabilities"*

> *"Do an ARP sweep of the 10.35.251.0/24 network and tell me what's alive"*

The agent picks the appropriate tool, runs it, and gets back structured JSON it can actually reason about — not a wall of text to parse.

---

## Example Output

### Network sweep — find live hosts and open ports across a subnet

**Prompt:** *"Do a fast port scan of 10.35.251.0/24"*

```json
{
  "scan_id": "20260304_120000_a1b2c3",
  "target": "10.35.251.0/24",
  "top_ports_scanned": 100,
  "total_open": 11,
  "per_host": {
    "10.35.251.1": {
      "hostname": "gateway.local",
      "state": "up",
      "open_ports": [
        {"port": 53,  "protocol": "tcp", "state": "open", "service": "domain",  "version": ""},
        {"port": 80,  "protocol": "tcp", "state": "open", "service": "http",    "version": ""},
        {"port": 443, "protocol": "tcp", "state": "open", "service": "https",   "version": ""}
      ]
    },
    "10.35.251.20": {
      "hostname": "",
      "state": "up",
      "open_ports": [
        {"port": 22,  "protocol": "tcp", "state": "open", "service": "ssh",     "version": ""},
        {"port": 80,  "protocol": "tcp", "state": "open", "service": "http",    "version": ""},
        {"port": 443, "protocol": "tcp", "state": "open", "service": "https",   "version": ""}
      ]
    },
    "10.35.251.55": {
      "hostname": "",
      "state": "up",
      "open_ports": [
        {"port": 80,   "protocol": "tcp", "state": "open", "service": "http",      "version": ""},
        {"port": 631,  "protocol": "tcp", "state": "open", "service": "ipp",       "version": ""},
        {"port": 9100, "protocol": "tcp", "state": "open", "service": "jetdirect", "version": ""}
      ]
    },
    "10.35.251.100": {
      "hostname": "",
      "state": "up",
      "open_ports": [
        {"port": 8080, "protocol": "tcp", "state": "open", "service": "http-proxy", "version": ""}
      ]
    }
  }
}
```

The agent can immediately tell you: `.1` is the gateway, `.55` looks like a network printer (IPP + JetDirect), `.20` has SSH exposed, and `.100` has something on 8080 worth investigating.

---

### Service detection — find out exactly what's running

**Prompt:** *"What services are running on 10.35.251.20?"*

```json
{
  "scan_id": "20260304_120045_b2c3d4",
  "target": "10.35.251.20",
  "intensity": 7,
  "total_open": 2,
  "per_host": {
    "10.35.251.20": {
      "hostname": "",
      "state": "up",
      "open_ports": [
        {
          "port": 22,
          "protocol": "tcp",
          "state": "open",
          "service": "ssh",
          "version": "OpenSSH 9.6p1 Ubuntu 3ubuntu13.14"
        },
        {
          "port": 80,
          "protocol": "tcp",
          "state": "open",
          "service": "http",
          "version": "nginx 1.24.0"
        }
      ]
    }
  }
}
```

Exact software versions — actionable for CVE lookup or patch management.

---

## Typical Audit Workflow

```
1. Find live hosts:           nmap_arp_discovery("10.35.251.0/24")
2. Quick port overview:       nmap_top_ports("10.35.251.0/24", count=100)
3. Service detection:         nmap_service_detection("10.35.251.20")
4. OS fingerprint:            nmap_os_detection("10.35.251.20")
5. Check for known vulns:     nmap_vuln_scan("10.35.251.20")
6. Deep single-host audit:    nmap_full_recon("10.35.251.20")
```

---

## Running Tests

```bash
python3 -m pytest tests/ -v
```

28 tests covering scope enforcement, audit logging, scan persistence, injection guards, port summary logic, and live integration against localhost.

Set `SKIP_LIVE_TESTS=1` to run only unit tests (no actual nmap calls):

```bash
SKIP_LIVE_TESTS=1 python3 -m pytest tests/ -v
```

---

## Security Notes

- **Only scan networks you own or have explicit written permission to scan.** Unauthorized network scanning is illegal in many jurisdictions.
- Keep your `config.yaml` CIDR allowlist tight — default to your actual subnet, not all of RFC1918.
- The audit log captures all scan activity. Review it periodically.
- `nmap_custom_scan` rejects shell metacharacters (`;`, `|`, `&`, `` ` ``, `$`, etc.) but is still the most flexible tool — use the specific tools where possible.

---

## License

MIT

---

## Contributing

PRs welcome. Please include tests for new tools or behavior changes — the test suite is the spec.
