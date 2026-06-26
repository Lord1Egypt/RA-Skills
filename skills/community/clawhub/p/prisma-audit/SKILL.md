---
name: prisma-audit
description: Audit and validate Prisma Access configurations against best practices and security standards. Use when reviewing security policies, checking for misconfigurations, or validating compliance with PAN-OS best practices and CIS benchmarks.
argument-hint: "[config-file-or-scope]"
version: 1.1.0
metadata:
  openclaw:
    emoji: "\U0001F50D"
    homepage: https://github.com/leesandao/prismaaccess-skill
---

# Prisma Access Configuration Auditor

Audit and validate Prisma Access (SCM) configurations for security, compliance, and operational best practices.

## How to Use

Provide configuration to audit via `$ARGUMENTS`:
- A file path containing SCM configuration JSON
- A description of the scope to audit (e.g., "security policies", "all NAT rules")
- Paste configuration JSON directly

## Audit Categories

### 1. Security Policy Audit

Check for:
- **Shadow rules**: rules that are never matched because a broader rule precedes them
- **Overly permissive rules**: `any/any/any/allow` patterns without justification
- **Missing security profiles**: allow rules without antivirus, anti-spyware, vulnerability protection, URL filtering, or wildfire analysis profiles
- **Missing logging**: rules without log-at-session-end enabled
- **Disabled rules**: identify and flag disabled rules that may be forgotten
- **Unused rules**: rules with zero hit counts (if hit count data is available)
- **Port-based rules**: rules using service ports instead of App-ID
- **Rule naming**: inconsistent or missing rule names/descriptions
- **Implicit deny**: verify a clean-up rule exists at the end of the policy

### 2. NAT Policy Audit

Check for:
- NAT rules without corresponding security policy rules
- Overlapping NAT translations
- Missing bidirectional NAT where expected
- Source NAT exhaustion risks (insufficient IP pool)

### 3. Decryption Policy Audit

Check for:
- Traffic bypassing SSL decryption without justification
- Missing decryption profiles on rules
- Expired or soon-to-expire certificates
- No-decrypt rules that are too broad
- Missing forward trust and forward untrust CA certificates

### 4. GlobalProtect Audit

Check for:
- Weak authentication methods
- Missing HIP checks (disk encryption, host firewall, patch level)
- Overly permissive split tunnel configuration
- Missing client certificate requirements for high-security environments
- Inactive or unused portals/gateways

### 5. Object Hygiene

Check for:
- Unused address objects and groups
- Overlapping address definitions
- FQDN objects that fail to resolve
- Empty address groups or service groups
- Duplicate objects with different names

### 6. Compliance Checks

Validate against:
- **PAN-OS Best Practice Assessment (BPA)**: alignment with Palo Alto Networks recommendations
- **CIS Palo Alto Benchmark**: Center for Internet Security controls
- **Zero Trust principles**: least-privilege access, micro-segmentation, identity-based policies

## Output Format

For each finding, report:

```
[SEVERITY] Category - Finding Title
  Description: What was found
  Location: Rule/object name and position
  Risk: Why this is a problem
  Recommendation: How to fix it
  Reference: Link to PAN-OS documentation or best practice guide
```

Severity levels:
- **CRITICAL**: Immediate security risk, must fix
- **HIGH**: Significant security or operational risk
- **MEDIUM**: Best practice violation, should fix
- **LOW**: Cosmetic or minor improvement
- **INFO**: Informational finding, no action required

## Summary Report

At the end, provide:
1. **Score**: Overall configuration health score (0-100)
2. **Finding counts**: by severity level
3. **Top 5 priorities**: the most impactful fixes to address first
4. **Quick wins**: low-effort changes with high security impact
