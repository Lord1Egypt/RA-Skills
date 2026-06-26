# NIST 800-53 Rev 5 Control Reference — Network Device Mapping

Control families with direct network device relevance mapped to CSF functions
and concrete audit checks. NIST SP 800-53 is a public-domain US government
publication — control descriptions are referenced directly.

**Baseline columns:** L = Low, M = Moderate, H = High impact baseline.
A checkmark (✓) means the control is part of that baseline.

**CSF functions:** ID = Identify, PR = Protect, DE = Detect, RS = Respond, RC = Recover.

## Access Control (AC)

| Control ID | Control Name | CSF Function | Network Device Audit Check | L | M | H |
|------------|-------------|-------------|---------------------------|---|---|---|
| AC-2 | Account Management | PR.AC | Verify all local accounts are authorized, no default/shared accounts, dormant accounts disabled | ✓ | ✓ | ✓ |
| AC-2(1) | Account Management — Automated System Account Management | PR.AC | Confirm centralized AAA manages account lifecycle (create/modify/disable/remove) | | ✓ | ✓ |
| AC-3 | Access Enforcement | PR.AC | Verify role-based access separates read-only, operator, and admin privileges | ✓ | ✓ | ✓ |
| AC-4 | Information Flow Enforcement | PR.AC, PR.DS | Verify ACLs enforce traffic flow policies between zones/segments | | ✓ | ✓ |
| AC-6 | Least Privilege | PR.AC | Confirm accounts use minimum privilege level required for role (no unnecessary priv 15 / superuser) | ✓ | ✓ | ✓ |
| AC-6(1) | Least Privilege — Authorize Access to Security Functions | PR.AC | Verify only designated admin accounts can modify security configuration | | ✓ | ✓ |
| AC-7 | Unsuccessful Logon Attempts | PR.AC | Check login failure lockout/delay configured on console, VTY, and web UI | ✓ | ✓ | ✓ |
| AC-12 | Session Termination | PR.AC | Verify idle timeout on VTY, console, SSH, and web management sessions | | ✓ | ✓ |
| AC-17 | Remote Access | PR.AC, PR.PT | Confirm SSH v2 only, Telnet disabled, source-address restrictions on VTY/management | ✓ | ✓ | ✓ |

## Audit and Accountability (AU)

| Control ID | Control Name | CSF Function | Network Device Audit Check | L | M | H |
|------------|-------------|-------------|---------------------------|---|---|---|
| AU-2 | Event Logging | DE.AE | Verify logging captures login attempts, config changes, ACL matches, privilege escalation | ✓ | ✓ | ✓ |
| AU-3 | Content of Audit Records | DE.AE | Confirm log entries include timestamp, event type, source, outcome, subject identity | ✓ | ✓ | ✓ |
| AU-3(1) | Content of Audit Records — Additional Audit Information | DE.AE | Verify logs include session ID, source IP, and terminal type for management access | | ✓ | ✓ |
| AU-4 | Audit Log Storage Capacity | DE.AE | Check local log buffer size and verify remote syslog destination is configured | ✓ | ✓ | ✓ |
| AU-5 | Response to Audit Logging Process Failures | DE.AE | Verify device generates alert when logging destination is unreachable | | ✓ | ✓ |
| AU-6 | Audit Record Review, Analysis, and Reporting | DE.AE, DE.DP | Confirm logs forwarded to SIEM or central analysis platform for review and correlation | ✓ | ✓ | ✓ |
| AU-8 | Time Stamps | PR.PT | Verify NTP synchronization with authenticated time sources, service timestamps enabled | ✓ | ✓ | ✓ |

## Configuration Management (CM)

| Control ID | Control Name | CSF Function | Network Device Audit Check | L | M | H |
|------------|-------------|-------------|---------------------------|---|---|---|
| CM-2 | Baseline Configuration | PR.IP | Compare running config against approved baseline; detect configuration drift | ✓ | ✓ | ✓ |
| CM-3 | Configuration Change Control | PR.IP | Verify config archive/rollback capability, change history preserved | | ✓ | ✓ |
| CM-5 | Access Restrictions for Change | PR.AC, PR.IP | Confirm only authorized accounts can modify device configuration | | ✓ | ✓ |
| CM-6 | Configuration Settings | PR.IP | Verify device matches organizational security configuration checklists | ✓ | ✓ | ✓ |
| CM-7 | Least Functionality | PR.IP, PR.PT | Confirm unnecessary services disabled (finger, pad, small-servers, CDP/LLDP where not needed, HTTP server) | ✓ | ✓ | ✓ |
| CM-7(1) | Least Functionality — Periodic Review | PR.IP | Verify periodic review of enabled services and protocols occurs | | ✓ | ✓ |
| CM-8 | System Component Inventory | ID.AM | Confirm device is recorded in asset inventory with platform, version, role, and location | ✓ | ✓ | ✓ |

## Identification and Authentication (IA)

| Control ID | Control Name | CSF Function | Network Device Audit Check | L | M | H |
|------------|-------------|-------------|---------------------------|---|---|---|
| IA-2 | Identification and Authentication (Organizational Users) | PR.AC | Verify centralized AAA (TACACS+/RADIUS) with local fallback, unique user identification | ✓ | ✓ | ✓ |
| IA-2(1) | Multi-Factor Authentication to Privileged Accounts | PR.AC | Confirm MFA for administrative access (certificate + password, token-based) | | ✓ | ✓ |
| IA-2(2) | Multi-Factor Authentication to Non-Privileged Accounts | PR.AC | Verify MFA for non-privileged accounts on High-impact systems | | | ✓ |
| IA-3 | Device Identification and Authentication | PR.AC | Verify device-to-device authentication: routing peer auth, 802.1X, MAB on access ports | ✓ | ✓ | ✓ |
| IA-5 | Authenticator Management | PR.AC | Check password complexity enforcement, credential hashing (scrypt/SHA-256), SSH key management | ✓ | ✓ | ✓ |
| IA-5(1) | Authenticator Management — Password-Based Authentication | PR.AC | Verify minimum password length, complexity, and rotation requirements | ✓ | ✓ | ✓ |
| IA-8 | Identification and Authentication (Non-Organizational Users) | PR.AC | Verify authentication for external/vendor access to devices (no shared vendor accounts) | ✓ | ✓ | ✓ |

## System and Communications Protection (SC)

| Control ID | Control Name | CSF Function | Network Device Audit Check | L | M | H |
|------------|-------------|-------------|---------------------------|---|---|---|
| SC-5 | Denial-of-Service Protection | PR.DS | Verify CoPP/rate limiting on control plane, storm control on access ports | ✓ | ✓ | ✓ |
| SC-7 | Boundary Protection | PR.AC, PR.DS | Verify ACL filtering at network boundaries, infrastructure ACL protects management addresses | ✓ | ✓ | ✓ |
| SC-7(3) | Boundary Protection — Access Points | PR.AC | Confirm all external connections are identified and monitored | | ✓ | ✓ |
| SC-8 | Transmission Confidentiality and Integrity | PR.DS | Verify encryption in transit: SSH for management, IPsec/MACsec for data, TLS for web management | | ✓ | ✓ |
| SC-10 | Network Disconnect | PR.AC | Verify session timeout on inactive SSH, VPN dead peer detection, idle connection teardown | | ✓ | ✓ |
| SC-13 | Cryptographic Protection | PR.DS | Audit crypto algorithms: flag DES, 3DES, RC4, MD5; require AES-128+, SHA-256+ | ✓ | ✓ | ✓ |
| SC-23 | Session Authenticity | PR.DS | Verify session integrity protections (TCP sequence number randomization, anti-replay) | | ✓ | ✓ |

## System and Information Integrity (SI)

| Control ID | Control Name | CSF Function | Network Device Audit Check | L | M | H |
|------------|-------------|-------------|---------------------------|---|---|---|
| SI-2 | Flaw Remediation | ID.RA, PR.IP | Check OS version against vendor security advisories, verify no known critical CVEs | ✓ | ✓ | ✓ |
| SI-2(2) | Flaw Remediation — Automated Flaw Remediation Status | ID.RA | Verify automated vulnerability scanning includes network devices | | ✓ | ✓ |
| SI-3 | Malicious Code Protection | DE.CM | Verify IPS signatures current on firewall/IPS appliances, check threat prevention update status | ✓ | ✓ | ✓ |
| SI-4 | System Monitoring | DE.CM, DE.AE | Verify NetFlow/sFlow, IDS/IPS, traffic monitoring on critical segments | ✓ | ✓ | ✓ |
| SI-4(4) | System Monitoring — Inbound and Outbound Communications Traffic | DE.CM | Confirm monitoring covers both inbound and outbound traffic at boundary devices | | ✓ | ✓ |
| SI-5 | Security Alerts, Advisories, and Directives | DE.DP | Confirm subscription to vendor security advisories (Cisco PSIRT, Juniper, Palo Alto, Arista) | ✓ | ✓ | ✓ |
| SI-7 | Software, Firmware, and Information Integrity | PR.DS | Verify device image integrity: secure boot, signed images, hash verification | ✓ | ✓ | ✓ |
