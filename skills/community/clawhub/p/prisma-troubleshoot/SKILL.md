---
name: prisma-troubleshoot
description: Troubleshoot Prisma Access issues including GlobalProtect connectivity, policy matching, tunnel status, SCM API errors, and configuration push failures. Use when diagnosing connection problems or configuration issues.
argument-hint: "[issue-description]"
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - SCM_CLIENT_ID
        - SCM_CLIENT_SECRET
        - SCM_TSG_ID
      bins:
        - curl
    primaryEnv: SCM_CLIENT_ID
    emoji: "\U0001F527"
    homepage: https://github.com/leesandao/prismaaccess-skill
---

# Prisma Access Troubleshooting Guide

Diagnose and resolve common Prisma Access issues via Strata Cloud Manager.

## How to Use

Describe the issue in `$ARGUMENTS`, or let this skill guide you through interactive troubleshooting.

## Troubleshooting Areas

### 1. GlobalProtect Connectivity Issues

**Symptoms**: Users cannot connect, connection drops, slow connections

**Diagnostic Steps**:
1. Check portal/gateway status via SCM API:
   ```
   GET /sse/config/v1/mobile-agent/portals?folder=Mobile Users
   GET /sse/config/v1/mobile-agent/gateways?folder=Mobile Users
   ```
2. Verify authentication profile configuration
3. Check HIP profile requirements vs client compliance
4. Review split tunnel configuration
5. Check DNS resolution for portal/gateway FQDNs
6. Verify certificate chain (portal cert, gateway cert, CA cert)

**Common Causes**:
- Expired or misconfigured certificates
- SAML IdP unreachable or misconfigured
- HIP check failures (disk encryption, antivirus, OS version)
- DNS resolution failures
- MTU/fragmentation issues
- ISP blocking UDP 4501 (IPSec) — check for TCP fallback

### 2. Security Policy Not Matching

**Symptoms**: Traffic allowed when it should be blocked, or blocked when it should be allowed

**Diagnostic Steps**:
1. Export and review rule ordering:
   ```
   GET /sse/config/v1/security-rules?folder=Prisma Access&position=pre
   GET /sse/config/v1/security-rules?folder=Prisma Access&position=post
   ```
2. Check for shadow rules (broader rules preceding specific ones)
3. Verify source/destination zone assignments
4. Confirm App-ID identification (check for SSL decryption)
5. Review address object resolution (FQDN objects, dynamic groups)
6. Check user-to-IP mapping for user-based rules

**Common Causes**:
- Rule ordering: more specific rules after broader rules
- Missing SSL decryption: App-ID cannot identify encrypted traffic
- Zone confusion: Mobile Users vs Remote Networks vs Service Connections
- Stale FQDN resolution
- User-ID mapping delays or failures

### 3. Configuration Push Failures

**Symptoms**: Config changes not taking effect, push job errors

**Diagnostic Steps**:
1. Check candidate config status:
   ```
   POST /sse/config/v1/config-versions/candidate:push
   ```
2. Monitor push job status:
   ```
   GET /sse/config/v1/jobs/{job-id}
   ```
3. Review job error details for specific validation failures

**Common Causes**:
- **Reference errors**: rules reference deleted or renamed objects
- **Duplicate names**: objects with same name in different folders
- **Invalid values**: out-of-range ports, malformed IP addresses
- **Dependency conflicts**: circular references between objects
- **Concurrent edits**: another admin pushed changes simultaneously

### 4. Remote Network / Service Connection Issues

**Symptoms**: Tunnel down, BGP not establishing, routes not propagating

**Diagnostic Steps**:
1. Check tunnel status via SCM
2. Verify IKE/IPSec configuration matches on both ends:
   - IKE version, DH group, encryption algorithm, hash algorithm
   - Pre-shared key or certificate authentication
   - Local and peer IDs
3. Review BGP configuration:
   - AS numbers, peer IP addresses, route advertisements
   - MD5 authentication
4. Check for overlapping IP ranges between sites

**Common Causes**:
- IKE/IPSec parameter mismatch with on-prem device
- Pre-shared key mismatch
- BGP peer address not in the same subnet
- Firewall blocking IKE (UDP 500/4500) on the on-prem side
- Overlapping IP address spaces between sites

### 5. SCM API Errors

**Symptoms**: API calls returning errors

**Common Error Codes and Solutions**:

| Code | Error | Solution |
|------|-------|----------|
| 400 | `Invalid Object` | Check JSON payload format; verify all required fields |
| 401 | `Authentication Error` | Token expired — re-authenticate with OAuth2 |
| 403 | `Authorization Error` | Check role-based access; verify TSG ID permissions |
| 404 | `Object Not Found` | Verify object name and folder parameter |
| 409 | `Conflict` | Object already exists; use PUT to update instead of POST |
| 429 | `Rate Limit` | Back off and retry; implement exponential backoff |
| 500 | `Internal Error` | Retry after 30 seconds; check SCM service status |
| 504 | `Gateway Timeout` | Retry; consider breaking large operations into batches |

### 6. Performance and Latency Issues

**Diagnostic Steps**:
1. Check bandwidth allocation per region
2. Review QoS policy configuration
3. Verify closest service edge location
4. Check for suboptimal routing (hairpinning through distant regions)
5. Review concurrent session counts vs license limits

## Diagnostic Approach

When the user reports an issue:

1. **Identify the category** from the areas above
2. **Gather information**: ask for specific error messages, affected users/sites, timeline
3. **Check configuration**: use SCM API to review relevant configuration
4. **Identify root cause**: compare configuration against best practices
5. **Provide fix**: give specific SCM API calls or configuration changes to resolve
6. **Verify**: provide steps to confirm the fix worked
