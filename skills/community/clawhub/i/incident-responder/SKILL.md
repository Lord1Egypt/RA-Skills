---
name: incident-responder
description: Playbook-driven incident response — MITRE ATT&CK mapping, evidence collection, timeline reconstruction, containment procedures, and post-incident reporting. Integrates with BlackArch forensics tools on ARGUS.
homepage: https://github.com/nousresearch/argus
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq", "grep", "awk"]
      mcps: ["cve-mcp", "aynops"]
      optional_bins: ["volatility3", "tshark", "autopsy", "sleuthkit", "bulk_extractor", "hashcat", "john"]
    os: ["linux"]
---

# Incident Responder

Playbook-driven incident response framework for ARGUS. Provides structured IR workflows: triage, evidence collection, MITRE ATT&CK mapping, timeline reconstruction, containment procedures, and post-incident reporting. Integrates with BlackArch forensics tools and CVE-MCP for threat intelligence during active incidents.

Runs on ARGUS infrastructure. Subscription service at $9/month.

## Prerequisites

- **ARGUS host** with BlackArch tools (forensics tools recommended)
- **CVE-MCP** available for threat intelligence during incidents
- **aynops** available for network-level evidence collection
- `curl`, `jq`, `grep`, `awk` on PATH
- Root/sudo access for forensic acquisition (volatility, tcpdump, disk imaging)

## Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| ARGUS host | local | IR coordination and evidence storage |
| CVE-MCP | localhost MCP | Vulnerability intelligence during incidents |
| aynops | localhost MCP | Network recon during containment |
| BlackArch tools | `/usr/share/` | Forensics, cracking, network analysis |
| Evidence store | `~/App/domains/argus/evidence/` | Immutable evidence archive |

## Incident Response Playbooks

### Playbook 1: Suspected Data Exfiltration

```
Phase 1 — TRIAGE (first 15 minutes)
  → Verify exfiltration indicators
  → Identify affected systems
  → Determine data classification level
  → Declare severity (P1-P4)

Phase 2 — EVIDENCE COLLECTION
  → Snapshot network connections: netstat -tlnp
  → Capture active connections: ss -tunap
  → Dump process list: ps auxf
  → Capture firewall logs: iptables -L -n -v
  → Snapshot DNS cache: systemd-resolve --statistics
  → Begin packet capture: tcpdump -i any -w /evidence/exfil-$(date +%s).pcap

Phase 3 — DEEP ANALYSIS
  → Analyze PCAP with tshark
  → Check auth logs for unusual access
  → Review outbound connections to known-bad IPs
  → Check cron/at for persistence
  → Audit ~/.ssh/authorized_keys

Phase 4 — CONTAINMENT
  → Block suspect IPs at firewall
  → Kill suspicious outbound connections
  → Revoke compromised credentials
  → Quarantine affected systems

Phase 5 — IMPACT ASSESSMENT
  → Determine data volume exfiltrated
  → Assess data sensitivity (PII, secrets, IP)
  → Regulatory notification requirements (GDPR 72h)
  → Customer impact analysis

Phase 6 — REMEDIATION
  → Patch exploited vulnerability
  → Rotate all credentials
  → Harden network segmentation
  → Deploy additional monitoring

Phase 7 — POST-INCIDENT
  → Root cause analysis (RCA)
  → Update IR playbook with lessons learned
  → Update threat model
  → Schedule tabletop exercise
```

### Playbook 2: Ransomware Infection

```
Phase 1 — TRIAGE
  → ISOLATE infected system immediately (pull network cable / disable NIC)
  → Do NOT power off (preserve memory for forensics)
  → Identify ransomware strain
  → Check if decryption tools exist (NoMoreRansom.org)

Phase 2 — EVIDENCE PRESERVATION
  → Memory dump: dd if=/dev/fmem of=/evidence/mem-$(hostname).dump
  → Disk image: dd if=/dev/sda of=/evidence/disk-$(hostname).img
  → Screenshot/photo of ransom note
  → Record encryption timestamps

Phase 3 — SCOPE DETERMINATION
  → Check network shares for encryption spread
  → Review backup integrity
  → Determine Patient Zero (initial infection vector)

Phase 4 — CONTAINMENT
  → Block C2 communication at firewall
  → Disable RDP/SMB on unaffected systems
  → Reset all domain credentials
  → Isolate affected network segments

Phase 5 — RECOVERY
  → Restore from clean backups (verify integrity first)
  → Rebuild affected systems from scratch
  → Apply security patches before reconnecting to network

Phase 6 — POST-INCIDENT
  → Determine initial access vector
  → Close the gap that allowed infection
  → Improve backup strategy (3-2-1 rule)
  → Deploy endpoint detection improvements
```

### Playbook 3: Credential Compromise

```
Phase 1 — TRIAGE
  → Identify compromised account(s)
  → Determine privilege level (user/admin/service)
  → Check for lateral movement indicators
  → Revoke credentials immediately

Phase 2 — EVIDENCE COLLECTION
  → Auth logs: /var/log/auth.log
  → Last logins: last -f /var/log/wtmp
  → Failed attempts: lastb -f /var/log/btmp
  → Current sessions: who / w
  → SSH keys audit: find /home -name "authorized_keys"

Phase 3 — SCOPE
  → Systems accessed by compromised account
  → Data accessed/modified
  → New accounts/spoofed credentials created
  → Persistence mechanisms installed

Phase 4 — CONTAINMENT
  → Force password reset for affected user
  → Rotate all service account credentials
  → Revoke all active sessions
  → Audit and clean SSH authorized_keys
  → Enable MFA if not already active

Phase 5 — IMPACT
  → Data accessed classification
  → Lateral movement extent
  → Persistence mechanisms found
  → Regulatory reporting requirements

Phase 6 — REMEDIATION
  → Close initial compromise vector
  → Deploy MFA for all privileged accounts
  → Implement session recording
  → Reduce credential standing privileges
```

## Core Commands

### Phase 1: Triage — Quick System Snapshot

Capture the state of a potentially compromised system:

```bash
HOSTNAME=$(hostname)
CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"

echo "=== IR Triage: $HOSTNAME ==="
echo "Case directory: $CASEDIR"
echo ""

# System info
echo "--- System Info ---"
uname -a > "$CASEDIR/uname.txt"
cat /etc/os-release > "$CASEDIR/os-release.txt"
uptime > "$CASEDIR/uptime.txt"

# Network connections
echo "--- Network Connections ---"
ss -tunap > "$CASEDIR/netstat-connections.txt"
ss -tunap | grep ESTAB | wc -l > "$CASEDIR/active-connections-count.txt"

# Listening ports
echo "--- Listening Ports ---"
ss -tlnp > "$CASEDIR/listening-ports.txt"

# Process list
echo "--- Process Tree ---"
ps auxf > "$CASEDIR/process-tree.txt"

# Current users
echo "--- Active Sessions ---"
who > "$CASEDIR/active-sessions.txt"
w >> "$CASEDIR/active-sessions.txt"

# Recent logins
echo "--- Recent Logins ---"
last -20 > "$CASEDIR/recent-logins.txt"

# Failed logins
echo "--- Failed Logins ---"
lastb -20 > "$CASEDIR/failed-logins.txt" 2>/dev/null || echo "  (lastb not available)"

# Cron jobs
echo "--- Cron Jobs ---"
crontab -l > "$CASEDIR/crontab.txt" 2>/dev/null
for user in $(cut -d: -f1 /etc/passwd); do
  crontab -u "$user" -l >> "$CASEDIR/crontab-all.txt" 2>/dev/null
done

# Loaded kernel modules
echo "--- Kernel Modules ---"
lsmod > "$CASEDIR/lsmod.txt"

# Open files
echo "--- Open Files (network) ---"
lsof -i > "$CASEDIR/lsof-network.txt" 2>/dev/null

echo ""
echo "Triage snapshot complete: $CASEDIR"
ls -la "$CASEDIR/"
```

### Auth Log Analysis

Extract brute-force and suspicious login patterns:

```bash
AUTH_LOG="/var/log/auth.log"
CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"

echo "=== Auth Log Analysis ==="

# Failed login count by IP
echo "--- Top Failed Login Sources ---"
grep "Failed password" "$AUTH_LOG" | \
  awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -20 | \
  tee "$CASEDIR/failed-by-ip.txt"

# Successful logins from unusual hours
echo ""
echo "--- Logins Between 00:00-05:00 ---"
grep "Accepted" "$AUTH_LOG" | \
  awk '{print $1, $2, $3, $9, $11}' | grep -E "0[0-5]:[0-9]{2}:" | \
  tee "$CASEDIR/night-logins.txt"

# Root login attempts
echo ""
echo "--- Root Login Attempts ---"
grep "root" "$AUTH_LOG" | grep -E "Failed|Accepted" | \
  tail -20 | tee "$CASEDIR/root-attempts.txt"

# New user creation
echo ""
echo "--- User Creation Events ---"
grep "new user" "$AUTH_LOG" | \
  tee "$CASEDIR/new-users.txt"

# Sudo usage
echo ""
echo "--- Sudo Usage ---"
grep "sudo" "$AUTH_LOG" | grep "COMMAND" | \
  tail -30 | tee "$CASEDIR/sudo-commands.txt"

# SSH key additions
echo ""
echo "--- SSH Key Events ---"
grep -i "authorized_keys" "$AUTH_LOG" | \
  tee "$CASEDIR/ssh-key-events.txt"
```

### Memory Forensics (Volatility)

If Volatility is installed, capture and analyze memory:

```bash
MEMDUMP="/evidence/mem-$(hostname)-$(date +%s).dump"
CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"

echo "=== Memory Forensics ==="

# Capture memory
echo "--- Memory Dump ---"
if [ -f /dev/fmem ]; then
  sudo dd if=/dev/fmem of="$MEMDUMP" bs=1M 2>&1
  echo "Memory dump: $MEMDUMP"
else
  echo "  /dev/fmem not available — install fmem kernel module"
  echo "  Alternative: sudo dd if=/dev/mem of=$MEMDUMP bs=1M"
fi

# If volatility is available, analyze
if command -v volatility3 &>/dev/null && [ -f "$MEMDUMP" ]; then
  echo ""
  echo "--- Volatility Analysis ---"
  
  # Process list
  volatility3 -f "$MEMDUMP" windows.pslist > "$CASEDIR/vol-pslist.txt" 2>/dev/null
  
  # Network connections
  volatility3 -f "$MEMDUMP" windows.netscan > "$CASEDIR/vol-netscan.txt" 2>/dev/null
  
  # Command history
  volatility3 -f "$MEMDUMP" windows.cmdline > "$CASEDIR/vol-cmdline.txt" 2>/dev/null
  
  # DLL injection detection
  volatility3 -f "$MEMDUMP" windows.dlllist > "$CASEDIR/vol-dlllist.txt" 2>/dev/null
  
  echo "Volatility analysis: $CASEDIR/vol-*.txt"
else
  echo "  Volatility not available or no memory dump"
fi
```

### PCAP Analysis (tshark)

Analyze captured network traffic:

```bash
PCAP="$1"
if [ -z "$PCAP" ]; then
  echo "Usage: $0 <capture.pcap>"
  exit 1
fi

CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"

echo "=== PCAP Analysis: $PCAP ==="

# Statistics
echo "--- Capture Statistics ---"
capinfos "$PCAP" | tee "$CASEDIR/capinfos.txt"

# Protocol hierarchy
echo ""
echo "--- Protocol Hierarchy ---"
tshark -r "$PCAP" -q -z io,phs | tee "$CASEDIR/protocols.txt"

# Top talkers (IP conversations)
echo ""
echo "--- Top IP Conversations ---"
tshark -r "$PCAP" -q -z conv,ip | head -30 | tee "$CASEDIR/top-conversations.txt"

# DNS queries
echo ""
echo "--- DNS Queries ---"
tshark -r "$PCAP" -Y "dns.flags.response == 0" -T fields \
  -e dns.qry.name | sort | uniq -c | sort -rn | head -30 | \
  tee "$CASEDIR/dns-queries.txt"

# HTTP requests
echo ""
echo "--- HTTP Requests ---"
tshark -r "$PCAP" -Y "http.request" -T fields \
  -e http.host -e http.request.uri | head -30 | \
  tee "$CASEDIR/http-requests.txt"

# TLS handshakes (SNI)
echo ""
echo "--- TLS SNI ---"
tshark -r "$PCAP" -Y "tls.handshake.extensions_server_name" -T fields \
  -e tls.handshake.extensions_server_name | sort | uniq -c | sort -rn | \
  tee "$CASEDIR/tls-sni.txt"

# Unique destination IPs
echo ""
echo "--- Unique Destination IPs ---"
tshark -r "$PCAP" -T fields -e ip.dst | sort -u | tee "$CASEDIR/unique-dest-ips.txt"

# Check for known-bad IPs
echo ""
echo "--- Known-Bad IP Check ---"
while IFS= read -r ip; do
  result=$(curl -s -X POST "http://localhost:8765/aynops/reputation" \
    -H "Content-Type: application/json" \
    -d "{\"ip\": \"$ip\"}" 2>/dev/null)
  score=$(echo "$result" | jq -r '.abuse_score // 0')
  if [ "$score" -gt 0 ]; then
    echo "  SUSPICIOUS: $ip (abuse score: $score)"
  fi
done < "$CASEDIR/unique-dest-ips.txt"
```

### Timeline Reconstruction

Build an event timeline from multiple log sources:

```bash
CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"
TIMELINE="$CASEDIR/timeline.jsonl"

echo "=== Timeline Reconstruction ==="

# Auth events
grep -E "Accepted|Failed|session opened|session closed" /var/log/auth.log | \
  while IFS= read -r line; do
    ts=$(echo "$line" | awk '{print $1, $2, $3}')
    event_type=$(echo "$line" | grep -q "Accepted" && echo "LOGIN_SUCCESS" || echo "LOGIN_FAILURE")
    user=$(echo "$line" | awk '{for(i=1;i<=NF;i++) if($i=="for") print $(i+1)}')
    ip=$(echo "$line" | grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b')
    echo "{\"timestamp\": \"$ts\", \"source\": \"auth.log\", \"type\": \"$event_type\", \"user\": \"$user\", \"ip\": \"$ip\"}" >> "$TIMELINE"
  done

# Sudo commands
grep "sudo.*COMMAND" /var/log/auth.log | \
  while IFS= read -r line; do
    ts=$(echo "$line" | awk '{print $1, $2, $3}')
    user=$(echo "$line" | awk -F' ;' '{print $2}' | awk '{print $1}')
    cmd=$(echo "$line" | grep -oP 'COMMAND=\K.*')
    echo "{\"timestamp\": \"$ts\", \"source\": \"auth.log\", \"type\": \"SUDO\", \"user\": \"$user\", \"command\": \"$cmd\"}" >> "$TIMELINE"
  done

# Sort timeline chronologically
sort -t'"' -k4 "$TIMELINE" > "$TIMELINE.sorted"
mv "$TIMELINE.sorted" "$TIMELINE"

echo ""
echo "=== Timeline Summary ==="
echo "Total events: $(wc -l < "$TIMELINE")"
echo ""
echo "--- Event Types ---"
jq -r '.type' "$TIMELINE" | sort | uniq -c | sort -rn
echo ""
echo "--- Unique Users ---"
jq -r '.user' "$TIMELINE" | sort -u | grep -v '^null$'
echo ""
echo "--- Unique IPs ---"
jq -r '.ip' "$TIMELINE" | sort -u | grep -v '^null$'
echo ""
echo "Timeline: $TIMELINE"
```

### Containment Actions

Execute containment procedures:

```bash
CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"

echo "=== Containment Actions ==="
echo "WARNING: These actions modify system state. Confirm before execution."
echo ""

# Block IPs at firewall
block_ip() {
  IP="$1"
  echo "Blocking $IP at iptables..."
  sudo iptables -A INPUT -s "$IP" -j DROP
  sudo iptables -A OUTPUT -d "$IP" -j DROP
  echo "$IP blocked: $(date)" >> "$CASEDIR/blocked-ips.txt"
}

# Kill suspicious connections
kill_connections_to_ip() {
  IP="$1"
  echo "Killing connections to $IP..."
  sudo ss -K dst "$IP"
  echo "Connections to $IP terminated: $(date)" >> "$CASEDIR/terminated-connections.txt"
}

# Revoke user sessions
revoke_user() {
  USER="$1"
  echo "Revoking sessions for $USER..."
  sudo pkill -KILL -u "$USER"
  sudo passwd -l "$USER"
  echo "User $USER locked: $(date)" >> "$CASEDIR/locked-accounts.txt"
}

# Quarantine system
quarantine_system() {
  echo "Quarantining system — dropping all non-loopback traffic..."
  sudo iptables -P INPUT DROP
  sudo iptables -P FORWARD DROP
  sudo iptables -P OUTPUT DROP
  sudo iptables -A INPUT -i lo -j ACCEPT
  sudo iptables -A OUTPUT -o lo -j ACCEPT
  echo "System quarantined: $(date)" >> "$CASEDIR/quarantine.txt"
}

echo "Containment functions loaded:"
echo "  block_ip <ip_address>"
echo "  kill_connections_to_ip <ip_address>"
echo "  revoke_user <username>"
echo "  quarantine_system"
```

### Post-Incident Report Template

Generate an incident report:

```bash
CASEDIR="$HOME/App/domains/argus/evidence/ir-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$CASEDIR"
REPORT="$CASEDIR/incident-report.md"

cat > "$REPORT" << 'EOF'
# Incident Report

## Executive Summary

**Incident ID:** IR-YYYY-NNN
**Date/Time Detected:** 
**Date/Time Resolved:**
**Severity:** P1 / P2 / P3 / P4
**Incident Commander:**

### What Happened
(Brief description — 2-3 sentences)

### Impact
- Systems affected: 
- Data exposed/modified: 
- Duration: 
- Regulatory impact: 

---

## Timeline

| Time | Event | Source |
|------|-------|--------|
| | Initial compromise detected | |
| | Triage started | |
| | Containment completed | |
| | Eradication completed | |
| | Recovery completed | |
| | Post-incident review | |

---

## Technical Details

### Initial Access Vector
(How did the attacker get in?)

### Indicators of Compromise (IOCs)
```
IP addresses:
Domains:
File hashes:
Registry keys:
```

### MITRE ATT&CK Mapping

| Tactic | Technique | Evidence |
|--------|-----------|----------|
| Initial Access | | |
| Execution | | |
| Persistence | | |
| Privilege Escalation | | |
| Defense Evasion | | |
| Credential Access | | |
| Discovery | | |
| Lateral Movement | | |
| Collection | | |
| Exfiltration | | |
| Command & Control | | |

### Evidence Inventory

| File | SHA-256 | Description |
|------|---------|-------------|
| | | |

---

## Containment & Eradication

### Actions Taken
1. 
2. 
3. 

### Remediation
1. 
2. 
3. 

---

## Lessons Learned

### What Went Well
1. 

### What Could Be Improved
1. 

### Action Items

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| | | | |

---

## Appendices

### A. Affected Systems
### B. Evidence Log
### C. Communication Log
### D. Regulatory Notifications

---

**Report Prepared By:**
**Date:**
**Classification:** CONFIDENTIAL
EOF

echo "Incident report template: $REPORT"
```

## Usage Patterns

### Incident Lifecycle

When an incident is declared:

1. **Triage (T+0-15min)** — Quick system snapshot, determine scope and severity
2. **Evidence Collection (T+15-60min)** — Memory dump, disk image, logs, PCAP
3. **Deep Analysis (T+60min-4h)** — Log analysis, PCAP review, malware analysis
4. **Containment (T+1-4h)** — Block IOCs, isolate systems, revoke credentials
5. **Impact Assessment (T+4-8h)** — Data classification, regulatory needs, customer impact
6. **Remediation (T+8-72h)** — Patch, rebuild, harden, deploy monitoring
7. **Post-Incident (T+72h-1w)** — RCA, lessons learned, playbook update, tabletop exercise

### Tabletop Exercise

Regular simulated incident response:

1. Select a playbook scenario
2. Walk through each phase without executing actions
3. Identify gaps in tooling, logging, or process
4. Time each phase — find bottlenecks
5. Update playbook with improvements
6. Schedule next exercise

### Evidence Integrity

All evidence must follow ARGUS AEO format:

```
Raw File → SHA-256 → Tool → Filtered Data → Bayesian Conclusion
```

Never modify evidence files once archived. Store in `~/App/domains/argus/evidence/objects/`.

## Pricing Tiers

### Incident Responder ($9/month)

- All 3 core playbooks (Data Exfiltration, Ransomware, Credential Compromise)
- Auth log analysis pipeline
- Network snapshot commands
- Timeline reconstruction
- Evidence collection scripts
- Post-incident report template
- MITRE ATT&CK mapping guidance
- Email support (business hours)

### Incident Responder Pro ($29/month)

- Custom playbook development (per your infrastructure)
- Advanced forensics: Volatility, Autopsy, bulk_extractor
- PCAP analysis with tshark + known-bad IP checking
- CVE-MCP integration during incidents
- Threat intel enrichment during triage
- Regulatory notification templates (GDPR, CCPA, HIPAA)
- Priority support (4-hour SLA)
- Quarterly tabletop exercise facilitation

### Enterprise ($99/month)

- All Pro features
- Custom playbook library (unlimited)
- SIEM integration (Splunk, ELK)
- SOAR playbook automation
- Multi-tenant incident management
- Retainer: 24/7 on-call IR support
- Annual red team exercise
- Compliance mapping (NIST, ISO 27001, SOC2)

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `EVIDENCE_DIR` | `~/App/domains/argus/evidence` | Evidence storage root |
| `IR_CASE_DIR` | `$EVIDENCE_DIR/ir-YYYYMMDD-HHMMSS` | Per-incident case directory |
| `AUTH_LOG` | `/var/log/auth.log` | Authentication log path |
| `CVE_MCP_URL` | `http://localhost:8765/cve-mcp` | CVE-MCP endpoint |
| `AYNOPS_MCP_URL` | `http://localhost:8765/aynops` | AynOps endpoint |
| `IR_ALERT_WEBHOOK` | (required) | Slack/Discord for incident alerts |
| `ESCALATION_CONTACT` | (required) | On-call contact for P1 incidents |
| `RETENTION_DAYS` | `90` | Evidence retention period |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| lastb empty | wtmp/btmp not enabled | `sudo touch /var/log/btmp && sudo chmod 600 /var/log/btmp` |
| tshark permission denied | Not in wireshark group | `sudo usermod -aG wireshark $USER` |
| Volatility module fails | Wrong profile | `volatility3 -f dump imageinfo` |
| Memory dump fails | /dev/fmem not loaded | `sudo modprobe fmem` or install fmem |
| lsof not found | Not installed | `sudo pacman -S lsof` |
| bulk_extractor hangs | Large disk | Run on specific partition, not entire disk |

## Security

- **Read-only by default** — evidence collection is non-destructive
- **Containment requires confirmation** — blocking IPs/killing processes needs explicit approval
- **Chain of custody** — all evidence SHA-256 hashed on collection
- **Immutable evidence** — never modify files in evidence/objects/ after archiving
- **Need-to-know** — incident details shared only with authorized responders
- **Legal hold** — incidents with regulatory impact may require evidence preservation beyond retention

## BlackArch Forensics Tools

Available for advanced forensics (install as needed):

| Tool | Use |
|------|-----|
| volatility3 | Memory forensics |
| tshark | PCAP analysis |
| autopsy | Digital forensics platform |
| sleuthkit | Filesystem forensics |
| bulk_extractor | Data carving |
| hashcat | Password recovery (authorized) |
| john | Password auditing |
| wireshark | Interactive packet analysis |

Install via:
```bash
cd ~/App/domains/argus/tools
./manage-blackarch.sh install volatility3 tshark autopsy sleuthkit bulk_extractor
```

## Related Skills

- **vulnerability-scanner** — identify the vulnerability exploited during incident
- **cve-tracker** — CVE intelligence for the exploited vulnerability
- **osint-investigator** — OSINT to attribute threat actor
- **gdpr-security-auditor** — regulatory impact assessment post-incident
