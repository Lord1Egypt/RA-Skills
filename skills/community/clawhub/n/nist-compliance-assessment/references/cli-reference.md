# NIST 800-53 Compliance CLI Reference — Read-Only Commands

Read-only verification commands organized by NIST 800-53 control family
for each supported platform. All commands are non-modifying — suitable
for production compliance assessment without change risk.

## Access Control (AC)

| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |
|-------------|---------|---------|-------|----------|
| Local accounts and privileges | `show running-config \| include username` | `show configuration system login` | `show running-config section username` | `show admins all` |
| AAA configuration | `show running-config \| section aaa` | `show configuration system authentication-order` | `show running-config section aaa` | `show config running \| match authentication-profile` |
| VTY/console access settings | `show running-config \| section line` | `show configuration system services ssh` | `show management ssh` | `show running management-profile` |
| SSH version and status | `show ip ssh` | `show configuration system services ssh` | `show management ssh` | `show config running \| match ssh` |
| Session idle timeout | `show running-config \| include exec-timeout` | `show configuration system login \| match idle-timeout` | `show running-config \| include idle-timeout` | `show config running \| match idle-timeout` |
| Privilege level assignments | `show privilege` | `show configuration system login class` | `show privilege` | `show admins all` |
| Active management sessions | `show users` | `show system users` | `show users` | `show admins` |
| HTTP/HTTPS server status | `show running-config \| include ip http` | `show configuration system services web-management` | `show management api http-commands` | `show running management-profile` |

## Audit and Accountability (AU)

| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |
|-------------|---------|---------|-------|----------|
| Logging configuration | `show logging` | `show configuration system syslog` | `show logging` | `show logging-status` |
| Remote syslog servers | `show running-config \| include logging host` | `show configuration system syslog host` | `show logging \| include Logging to` | `show config running \| match syslog` |
| Log buffer and severity | `show logging \| include Buffer` | `show configuration system syslog file` | `show logging \| include Buffer` | `show config running \| match log-severity` |
| NTP associations | `show ntp associations` | `show ntp associations` | `show ntp associations` | `show ntp` |
| NTP synchronization status | `show ntp status` | `show ntp status` | `show ntp status` | `show ntp` |
| NTP authentication | `show running-config \| include ntp authenticate` | `show configuration system ntp` | `show running-config \| include ntp authenticate` | `show config running \| match ntp` |
| Service timestamps | `show running-config \| include service timestamps` | `show configuration system syslog time-override` | `show running-config \| include timestamps` | (enabled by default) |
| SNMP trap/inform targets | `show snmp host` | `show configuration snmp trap-group` | `show snmp host` | `show config running \| match snmp-trap` |

## Configuration Management (CM)

| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |
|-------------|---------|---------|-------|----------|
| Running vs startup diff | `show archive config differences` | `show system rollback compare 0 1` | `show running-config diffs` | `show config diff` |
| Config archive/rollback | `show archive` | `show system rollback` | `show boot-config` | `show config audit info` |
| Enabled services inventory | `show running-config \| include ^service\|^no service` | `show configuration system services` | `show running-config \| include management\|service` | `show running management-profile` |
| Unnecessary services check | `show running-config \| include finger\|pad\|small-servers\|source-route` | `show configuration system services \| match finger\|telnet\|ftp` | `show running-config \| include telnet\|http server` | `show config running \| match telnet\|http` |
| Boot/image integrity | `show version` | `show system storage` | `show version` | `show system info` |
| CDP/LLDP status | `show cdp neighbors` | `show lldp neighbors` | `show lldp neighbors` | (not applicable) |
| Configuration change log | `show archive log config all` | `show system commit` | `show logging last 50 \| include CONFIG` | `show config audit info` |

## Identification and Authentication (IA)

| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |
|-------------|---------|---------|-------|----------|
| AAA method lists | `show aaa method-lists all` | `show configuration system authentication-order` | `show aaa method-lists` | `show config running \| match authentication-profile` |
| TACACS+ servers | `show tacacs` | `show configuration system tacplus-server` | `show tacacs` | `show config running \| match tacplus` |
| RADIUS servers | `show radius server-group all` | `show configuration system radius-server` | `show radius-server` | `show config running \| match radius` |
| Password hash strength | `show running-config \| include username` (check `secret 9` or `algorithm-type scrypt`) | `show configuration system login \| match encrypted` | `show running-config section username` | `show config running \| match password-complexity` |
| SNMPv3 users | `show snmp user` | `show configuration snmp v3` | `show snmp user` | `show config running \| match snmp` |
| SNMP community strings | `show snmp community` | `show configuration snmp community` | `show snmp community` | `show config running \| match community` |
| SSH key configuration | `show ip ssh` (RSA/ECDSA key size) | `show configuration security ssh-known-hosts` | `show management ssh` | `show config running \| match ssh` |
| 802.1X status | `show dot1x all summary` | `show configuration protocols dot1x` | `show dot1x` | (not applicable — network access control) |

## System and Communications Protection (SC)

| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |
|-------------|---------|---------|-------|----------|
| Boundary ACLs | `show ip access-lists` | `show configuration firewall family inet` | `show ip access-lists` | `show running security-policy` |
| ACL hit counts | `show access-lists` | `show firewall` | `show ip access-lists` | `show rule-hit-count vsys vsys1 security rules all` |
| CoPP / control plane protection | `show policy-map control-plane` | `show configuration interfaces lo0 unit 0 family inet filter` | `show policy-map control-plane` | `show running dos-policy` |
| IPsec tunnel status | `show crypto ipsec sa` | `show security ike security-associations` | `show ip security connection` | `show vpn ipsec-sa` |
| IPsec crypto algorithms | `show crypto ipsec sa \| include encrypt\|hmac` | `show security ipsec security-associations detail` | `show ip security` | `show vpn ipsec-sa detail` |
| Storm control settings | `show storm-control broadcast` | `show configuration ethernet-switching-options storm-control` | `show storm-control` | (not applicable — L3 device) |
| Interface encryption (MACsec) | `show macsec summary` | `show security macsec connections` | `show mac security` | (not applicable) |
| Zone/segment isolation | `show running-config \| section zone` | `show configuration security zones` | `show running-config section access-list` | `show running zone` |

## System and Information Integrity (SI)

| Control Area | [Cisco] | [JunOS] | [EOS] | [PAN-OS] |
|-------------|---------|---------|-------|----------|
| OS version / patch level | `show version` | `show version` | `show version` | `show system info` |
| Software image integrity | `show software authenticity running` | `show system software validate` | `show version` | `show system info \| match sw-version` |
| Content/signature updates | (N/A for base IOS) | (N/A for base JunOS) | (N/A for base EOS) | `show system info \| match content` |
| IPS/threat status | (requires FirePOWER) | `show security idp status` | (external IDS) | `show running threat-prevention` |
| NetFlow/traffic monitoring | `show flow monitor` | `show services accounting flow` | `show flow tracking` | `show running netflow` |
| Interface error counters | `show interfaces counters errors` | `show interfaces statistics` | `show interfaces counters errors` | `show interface all` |
| System uptime and reload reason | `show version \| include uptime\|reload` | `show system uptime` | `show uptime` | `show system info \| match uptime` |
| Active CVE check resources | Cisco PSIRT: sec.cloudapps.cisco.com | Juniper SA: supportportal.juniper.net | Arista SA: arista.com/security | PAN SA: security.paloaltonetworks.com |
