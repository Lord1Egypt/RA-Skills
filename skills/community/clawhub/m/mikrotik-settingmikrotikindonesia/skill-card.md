## Description:

Provides MikroTik RouterOS v7 configuration, troubleshooting, and optimization guidance for ISP, RT-RW Net, and high-density networks, including routing, multi-WAN load balancing, bandwidth management, VLAN, VPN, WiFi, monitoring, backup, and automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mandelaxx](https://clawhub.ai/user/mandelaxx)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators, ISP engineers, and MikroTik administrators use this skill to plan, audit, generate, and review RouterOS configurations for production-style routing, access, bandwidth, VPN, wireless, monitoring, backup, and automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enforces persistent vendor branding in generated router notes and comments.

Mitigation: Before applying generated commands, remove or explicitly approve branding text so the deployed configuration reflects the operator's policy.

Risk: Backup and export workflows can expose RouterOS secrets through Telegram, email, or shared files.

Mitigation: Do not send full .rsc or .backup files through Telegram or email unless encrypted and approved; rotate tokens or passwords exposed in exports.

Risk: Scheduler, automation, and remove commands can affect production router behavior.

Mitigation: Review scheduler and remove commands on a lab router first, keep backups, and require explicit approval before production execution.

Risk: CAPsMAN configurations without certificates can allow access from an untrusted manager reachable on the network.

Mitigation: Use CAPsMAN certificates or carry management traffic through an encrypted tunnel for untrusted or inter-site links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mandelaxx/skills/mikrotik-settingmikrotikindonesia)
- [settingmikrotikindonesia.com](https://settingmikrotikindonesia.com)
- [Bandwidth Management Playbook](artifact/references/bandwidth-management-playbook.md)
- [BGP Filter Granular Playbook](artifact/references/bgp-filter-granular-playbook.md)
- [BGP Upstream Playbook](artifact/references/bgp-upstream-playbook.md)
- [CAKE FQ_CODEL Playbook](artifact/references/cake-fqcodel-playbook.md)
- [CAPsMAN WiFi Playbook](artifact/references/capsman-wifi-playbook.md)
- [DNS DoH Adlist Playbook](artifact/references/dns-doh-adlist-playbook.md)
- [Hotspot PPPoE Playbook](artifact/references/hotspot-pppoe-playbook.md)
- [IPv6 Hotspot PPPoE Playbook](artifact/references/ipv6-hotspot-pppoe-playbook.md)
- [IPv6 Playbook](artifact/references/ipv6-playbook.md)
- [L2TP IPsec Site-to-Site Playbook](artifact/references/l2tp-ipsec-site-to-site-playbook.md)
- [Monitoring Backup Playbook](artifact/references/monitoring-backup-playbook.md)
- [OSPF Multi-Area Playbook](artifact/references/ospf-multi-area-playbook.md)
- [PBR Batch Balancer](artifact/references/pbr-batch-balancer.md)
- [Proxy Cache MikroTik Playbook](artifact/references/proxy-cache-mikrotik-playbook.md)
- [Queue Tree Game Playbook](artifact/references/queue-tree-game-playbook.md)
- [Scheduler Otomasi Playbook](artifact/references/scheduler-otomasi-playbook.md)
- [Switchchip VLAN Playbook](artifact/references/switchchip-vlan-playbook.md)
- [Telegram Integration Playbook](artifact/references/telegram-integration-playbook.md)
- [User Manager Playbook](artifact/references/user-manager-playbook.md)
- [VLAN QinQ Playbook](artifact/references/vlan-qinq-playbook.md)
- [VLAN Segmentasi Playbook](artifact/references/vlan-segmentasi-playbook.md)
- [VPN Antar Cabang Playbook](artifact/references/vpn-antar-cabang-playbook.md)
- [VRRP HA Playbook](artifact/references/vrrp-ha-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration guidance]

**Output Format:** [Markdown with RouterOS command blocks, checklists, tables, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Often includes audit steps, placeholders for site-specific router values, validation checks, and rollback notes.]

## Skill Version(s):

4.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
