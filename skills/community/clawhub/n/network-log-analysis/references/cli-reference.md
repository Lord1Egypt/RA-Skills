# CLI Reference — Network Log Analysis

Commands organized by analysis phase: syslog server configuration,
device syslog verification, and log parsing one-liners.

## Syslog Server Configuration

### rsyslog

**Check running configuration:**
```bash
rsyslogd -N1          # Validate config syntax
cat /etc/rsyslog.conf # Main configuration
ls /etc/rsyslog.d/    # Drop-in config fragments
```

**Common input modules:**
```
# UDP listener (traditional syslog)
module(load="imudp")
input(type="imudp" port="514")

# TCP listener (reliable transport)
module(load="imtcp")
input(type="imtcp" port="514")

# RELP listener (reliable event logging protocol)
module(load="imrelp")
input(type="imrelp" port="2514")
```

**Facility/severity routing rules:**
```
# Route by facility to separate files
local0.*    /var/log/network/routers.log
local1.*    /var/log/network/switches.log
local2.*    /var/log/network/firewalls.log

# Route by severity (critical and above to alert file)
*.crit      /var/log/network/critical.log

# Route by source IP (requires property-based filter)
:fromhost-ip, isequal, "10.0.0.1"  /var/log/network/core-rtr01.log
```

**File output template with source hostname:**
```
template(name="NetworkLog" type="string"
  string="%TIMESTAMP% %HOSTNAME% %syslogtag%%msg%\n")

local0.* action(type="omfile" file="/var/log/network/routers.log"
  template="NetworkLog")
```

### syslog-ng

**Check running configuration:**
```bash
syslog-ng --syntax-only     # Validate config
cat /etc/syslog-ng/syslog-ng.conf
```

**Network source definition:**
```
source s_network {
    udp(port(514));
    tcp(port(514));
};
```

**Filter and destination examples:**
```
filter f_routers { facility(local0); };
filter f_critical { level(crit..emerg); };
filter f_cisco { match("%[A-Z]+-[0-7]-[A-Z_]+" value("MESSAGE")); };

destination d_routers { file("/var/log/network/routers.log"); };
destination d_critical { file("/var/log/network/critical.log"); };

log { source(s_network); filter(f_routers); destination(d_routers); };
log { source(s_network); filter(f_critical); destination(d_critical); };
```

**Preserve original hostname:**
```
options {
    keep-hostname(yes);
    use-dns(no);
};
```

## Device Syslog Configuration Commands

### Cisco IOS-XE

```
! Show current logging configuration
show logging

! Configure syslog destination
logging host 10.1.1.100 transport udp port 514
logging trap informational          ! Severity 6 and above
logging facility local0             ! Facility code for rsyslog routing
logging source-interface Loopback0  ! Consistent source IP

! Verify logging history
show logging history
```

### Juniper JunOS

```
# Show syslog configuration
show system syslog

# Configure syslog destination
set system syslog host 10.1.1.100 any info
set system syslog host 10.1.1.100 facility-override local0
set system syslog host 10.1.1.100 structured-data

# Enable structured syslog for parseable output
set system syslog host 10.1.1.100 explicit-priority
```

### Arista EOS

```
! Show current logging settings
show logging

! Configure syslog destination
logging host 10.1.1.100 514 protocol udp
logging trap informational
logging facility local0
logging source-interface Loopback0
```

### NTP Verification

```
! Cisco IOS-XE
show ntp status
show ntp associations

# Juniper JunOS
show system ntp
show system ntp associations

! Arista EOS
show ntp status
show ntp associations
```

## Log Parsing One-Liners

### Timestamp Extraction and Sorting

```bash
# Sort merged logs chronologically (RFC 3164 format: Mmm dd HH:MM:SS)
sort -k1M -k2n -k3 merged.log

# Sort RFC 5424 ISO timestamps
sort -t'T' -k1 rfc5424.log

# Convert RFC 3164 to epoch for numeric sorting
awk '{
  cmd = "date -d \""$1" "$2" "$3"\" +%s 2>/dev/null"
  cmd | getline epoch; close(cmd)
  print epoch, $0
}' logfile.log | sort -n | cut -d' ' -f2-
```

### Pattern Extraction

```bash
# Extract all Cisco mnemonics from log file
grep -oP '%\S+-\d-\S+' cisco.log | sort | uniq -c | sort -rn

# Extract all source IPs from syslog messages
grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' network.log | sort | uniq -c | sort -rn

# Extract authentication-related messages
grep -iE 'AUTH|LOGIN|SSH|AUTHEN|FAILED|ACCEPT' network.log

# Extract interface state changes
grep -iE 'UPDOWN|LINK|LINEPROTO|changed state' network.log

# Extract configuration change events
grep -iE 'CONFIG|SYS-5-CONFIG_I|CONFIGURED|commit' network.log

# Extract routing adjacency events
grep -iE 'OSPF|BGP|ADJCHG|NBRDOWN|NEIGHBOR|ADJCHANGE' network.log
```

### Frequency Analysis

```bash
# Message count per hour
awk '{print $1, $2, substr($3,1,2)":00"}' network.log | sort | uniq -c | sort -rn

# Message count per device per day
awk '{print $1, $2, $4}' network.log | sort | uniq -c | sort -rn

# Top 20 most frequent message types (Cisco mnemonic)
grep -oP '%\S+-\d-\S+' cisco.log | sort | uniq -c | sort -rn | head -20

# Events per severity level
grep -oP '%\S+-(\d)-' cisco.log | sort | uniq -c | sort -rn
```

### Correlation Helpers

```bash
# Extract events within ±5 minutes of a known timestamp
# (Requires epoch conversion for precision)
TARGET_EPOCH=$(date -d "2024-03-15 14:30:00" +%s)
WINDOW=300  # 5 minutes in seconds
awk -v target="$TARGET_EPOCH" -v win="$WINDOW" '{
  cmd = "date -d \""$1" "$2" "$3"\" +%s 2>/dev/null"
  cmd | getline epoch; close(cmd)
  if (epoch >= target-win && epoch <= target+win) print
}' network.log

# Find events on multiple devices within same minute
awk '{print $1, $2, substr($3,1,5)}' merged.log | sort | uniq -c | \
  awk '$1 > 1 {print}'

# Track a single IP across all log files
grep "10.0.0.50" /var/log/network/*.log | sort -t: -k2
```

### Compressed Log Analysis

```bash
# Search within gzipped rotated logs
zgrep "PATTERN" /var/log/network/*.gz

# Merge current and rotated logs for full timeline
zcat /var/log/network/routers.log.*.gz | cat - /var/log/network/routers.log | sort -k1M -k2n -k3
```

## Logrotate Configuration

### Standard network log rotation

```
# /etc/logrotate.d/network-syslog
/var/log/network/*.log {
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
    create 0640 syslog adm
    sharedscripts
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

Key settings for forensic readiness:
- `rotate 90` — retain 90 days of compressed logs
- `compress` — gzip old logs to save space
- `delaycompress` — keep yesterday's log uncompressed for easy grep
- `create 0640 syslog adm` — proper permissions for log access
