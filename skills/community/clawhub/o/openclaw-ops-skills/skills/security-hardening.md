# Security Hardening

> **Protect your agent, your systems, and your data from autonomous operations**
> Priority: CRITICAL | Category: Security

## Overview

OpenClaw agents have shell access, browser control, and the ability to execute actions on your behalf. They run in loops without requiring approval. Security is not optional - it's existential.

## Known Vulnerabilities

### Recent CVEs

```yaml
cve_history:
  cve_2024_001:
    severity: "CVSS 8.8 (HIGH)"
    type: "Remote Code Execution"
    impact: "Agent could execute arbitrary commands"
    mitigation: "Update to v2.3.1+"

  cve_2024_015:
    severity: "CVSS 7.5 (HIGH)"
    type: "Authentication Bypass"
    impact: "Unauthorized agent control"
    mitigation: "Enable strict API key validation"

clawhavoc_campaign:
    severity: "CRITICAL"
    type: "Supply Chain Poisoning"
    impact: "1,184+ malicious skills on ClawHub (~12% of registry)"
    payload_types:
      - "Cryptocurrency stealers"
      - "Reverse shells"
      - "Credential exfiltration"
      - "Fake trading bots"
    affected: "All users who installed skills during campaign period"
```

### Exposure Statistics

```yaml
exposure_data:
  exposed_instances: "30,000+"
  sources:
    - "Bitsight scans"
    - "Censys scans"
  common_issues:
    - "Default gateway authentication"
    - "Exposed browser control"
    - "Overly permissive allowlists"
    - "File system over-access"
```

## Security Configuration

### 1. Gateway Security

```json
{
  "gateway": {
    "authentication": {
      "enabled": true,
      "method": "api-key",
      "rotation": "weekly",
      "complexity": {
        "min_length": 32,
        "require_special": true,
        "require_numbers": true
      }
    },
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 100,
      "burst": 20
    },
    "ip_whitelist": {
      "enabled": true,
      "addresses": ["localhost", "127.0.0.1"]
    }
  }
}
```

### 2. Browser Control Security

```yaml
browser_security:
  isolation:
    enabled: true
    profile: "isolated-agent"
    data_separation: true

  permissions:
    default: "deny"
    allowlist:
      - "specific-domain.com"
      "*.internal.com"

  restrictions:
    - "No filesystem access"
    - "No camera/microphone"
    - "No geolocation"
    - "No clipboard read (write only)"

  monitoring:
    log_all_requests: true
    alert_on_suspicious: true
    block_unknown_domains: true
```

### 3. File System Boundaries

```yaml
filesystem_security:
  workspace_root:
    path: "~/.openclaw/workspace"
    access: "read-write"

  project_directories:
    path: "~/projects/*"
    access: "read-write"
    require_explicit: true

  system_paths:
    protected:
      - "/etc/"
      - "/usr/bin/"
      - "/System/"
      - "C:\\Windows\\"
    access: "read-only (specific files only)"

  forbidden:
    - "~/.ssh/"
    - "~/.aws/credentials"
    - "~/.gnupg/"
    - "*.key"
    - "*.pem"
    - ".env*"
```

### 4. Command Execution Control

```yaml
command_security:
  default_mode: "require_approval"

  allowlist:
    safe_commands:
      - "git status"
      - "git diff"
      - "git log"
      - "ls -la"
      - "cat FILE"
      - "grep PATTERN FILE"

    approval_required:
      - "git commit"
      - "git push"
      - "npm install"
      - "docker build"
      - "kubectl apply"

    forbidden:
      - "rm -rf"
      - "chmod 777"
      - "curl | bash"
      - "wget | sh"
      - "sudo **"
      - "eval **"

  sandbox_mode:
    enabled: true
    container: "openclaw-sandbox"
    network: "isolated"
```

## Skill Validation Protocol

### Before Installing Any Skill

```yaml
pre_install_checks:
  1:
    name: "Source Verification"
    checks:
      - "Skill from official ClawHub?"
      - "Author verified?"
      - "Skill has reviews?"
      - "Skill has stars > 10?"
    pass_threshold: "All checks"

  2:
    name: "Code Review"
    checks:
      - "Read skill source code"
      - "Check for obfuscated code"
      - "Check for network calls"
      - "Check for file operations"
      - "Check for command execution"
    pass_threshold: "No suspicious patterns"

  3:
    name: "Permission Analysis"
    checks:
      - "List all permissions required"
      - "Verify each permission is necessary"
      - "Check for overly broad permissions"
      - "Verify no credential access"
    pass_threshold: "All permissions justified"

  4:
    name: "Sandbox Test"
    checks:
      - "Install in test environment first"
      - "Monitor behavior"
      - "Check network activity"
      - "Check file access"
      - "Check command execution"
    pass_threshold: "No unexpected behavior"
```

### Red Flags

```yaml
suspicious_patterns:
  immediate_reject:
    - "Base64 encoded payloads"
    - "Obfuscated code"
    - "Unknown domains in network calls"
    - "Credential collection"
    - "Reverse shell patterns"
    - "Cryptocurrency operations"

  caution:
    - "Requests broad filesystem access"
    - "Requests system-level permissions"
    - "Modifies system configuration"
    - "Installs additional software"
    - "Creates scheduled tasks"
    - "Requires network access to unknown domains"

  verify:
    - "New author (no reputation)"
    - "Few or no reviews"
    - "Recent publication (no usage history)"
    - "Vague description"
    - "Overly broad permissions"
```

## Operational Security

### 1. Credential Management

```yaml
credentials_policy:
  storage:
    method: "environment_variables"
    rotation: "weekly"
    complexity:
      min_length: 32
      unique_per_service: true

  forbidden:
    - "Hardcoded credentials"
    - "Credentials in workspace files"
    - "Credentials in git"
    - "Credentials in logs"

  services:
    openclaw:
      method: "env: OPENCLAW_API_KEY"
      rotation: "monthly"

    external_apis:
      method: "env: SERVICE_API_KEY"
      rotation: "per_service_policy"
```

### 2. Audit Trail

```yaml
audit_logging:
  enabled: true

  log_events:
    - "All command executions"
    - "All file operations"
    - "All network requests"
    - "All skill installations"
    - "All configuration changes"
    - "All failures and errors"

  log_format: "JSON"
  log_rotation: "daily"
  log_retention: "90 days"

  monitoring:
    alert_on:
      - "Forbidden command attempts"
      - "Unknown network connections"
      - "Credential access attempts"
      - "Filesystem boundary violations"
      - "Multiple failed authentications"
```

### 3. Isolation Strategy

```yaml
isolation_levels:
  agent_level:
    - "Dedicated agent user"
    - "Restricted permissions"
    - "No sudo access"

  workspace_level:
    - "Isolated workspace directory"
    - "No access to user home"
    - "No access to system directories"

  network_level:
    - "VPN for remote operations"
    - "Firewall rules"
    - "Network segmentation"
```

## Security Commands

### Regular Security Audits

```bash
# Deep security scan
openclaw security audit --deep

# Auto-fix issues
openclaw security audit --fix

# JSON output for monitoring
openclaw security audit --json

# Check specific area
openclaw security audit --area filesystem

# Verify skill integrity
openclaw security verify-skills

# Check for vulnerabilities
openclaw security check-cve

# Audit exposed credentials
openclaw security audit --credentials
```

### Health Checks

```bash
# Comprehensive health check
openclaw doctor --deep --fix --yes

# Status check
openclaw status --all --deep

# Exposure scan
openclaw security scan-exposure

# Permission audit
openclaw security audit-permissions
```

## Incident Response

### If Security Incident Suspected

```yaml
immediate_actions:
  1: "STOP: Kill all agent processes"
    command: "openclaw stop --force"

  2: "ISOLATE: Disconnect from network"
    command: "Disconnect network interface"

  3: "ASSESS: Review logs for suspicious activity"
    command: "openclaw logs --suspicious --since=24h"

  4: "SANITIZE: Rotate all credentials"
    command: "Rotate all API keys and passwords"

  5: "VERIFY: Run full security audit"
    command: "openclaw security audit --deep"

  6: "RECOVER: Restore from clean backup if needed"
    command: "Restore from pre-incident backup"
```

### Post-Incident

```yaml
post_incident:
  analysis:
    - "Root cause analysis"
    - "Impact assessment"
    - "Data compromise check"

  remediation:
    - "Patch vulnerability"
    - "Update skills"
    - "Review security settings"
    - "Document lessons learned"

  prevention:
    - "Add monitoring for attack pattern"
    - "Update security policies"
    - "Train on indicators"
    - "Schedule more frequent audits"
```

## Security Checklist

### Initial Setup

```yaml
setup_security:
  authentication:
    - [ ] "Strong API keys configured"
    - [ ] "Key rotation scheduled"
    - [ ] "Multi-factor enabled (if available)"

  filesystem:
    - [ ] "Workspace boundaries set"
    - [ ] "System paths protected"
    - [ ] "Credential files blocked"
    - [ ] "Write permissions limited"

  network:
    - [ ] "IP whitelist configured"
    - [ ] "Rate limiting enabled"
    - [ ] "SSL/TLS enforced"
    - [ ] "Unknown domains blocked"

  skills:
    - [ ] "All skills verified"
    - [ ] "No suspicious patterns found"
    - [ ] "Permissions reviewed"
    - [ ] "Source code audited"

  monitoring:
    - [ ] "Audit logging enabled"
    - [ ] "Alerts configured"
    - [ ] "Regular scans scheduled"
    - [ ] "Exposure monitoring active"
```

### Ongoing

```yaml
ongoing_security:
  daily:
    - [ ] "Review security logs"
    - [ ] "Check for failed authentications"
    - [ ] "Verify no unknown skills installed"

  weekly:
    - [ ] "Run security audit"
    - [ ] "Rotate sensitive credentials"
    - [ ] "Review skill permissions"
    - [ ] "Check for CVEs"

  monthly:
    - [ ] "Deep security scan"
    - [ ] "Review all skills"
    - [ ] "Update OpenClaw"
    - [ ] "Security assessment"
```

## Key Takeaway

**Your agent has the keys to your kingdom. Security is not an afterthought - it's the foundation.**

---

**Related Skills**: `scope-control.md`, `docs-first.md`
