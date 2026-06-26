---
name: prisma-config
description: Generate Prisma Access configurations for Strata Cloud Manager (SCM). Use when creating security policies, NAT rules, decryption policies, URL filtering profiles, GlobalProtect configs, or any SCM configuration objects.
argument-hint: "[config-type] [details]"
version: 1.1.0
metadata:
  openclaw:
    emoji: "\U0001F6E1\uFE0F"
    homepage: https://github.com/leesandao/prismaaccess-skill
---

# Prisma Access Configuration Generator

Generate production-ready Prisma Access configurations for Strata Cloud Manager (SCM).

## Supported Configuration Types

When the user specifies `$ARGUMENTS`, generate the corresponding configuration. If no type is specified, ask which configuration they need.

### Security Policy Rules
- Pre-rules and post-rules
- Source/destination zones, addresses, and users
- Application and service definitions
- Security profiles (antivirus, anti-spyware, vulnerability protection, URL filtering, file blocking, wildfire)
- Log forwarding profiles
- Rule ordering and positioning

### NAT Rules
- Source NAT (dynamic IP and port, dynamic IP, static IP)
- Destination NAT
- Bidirectional NAT
- NAT for GlobalProtect and service connections

### Decryption Policy
- SSL forward proxy rules
- SSL inbound inspection rules
- Decryption profiles
- Certificate management considerations
- No-decrypt rules for sensitive categories

### URL Filtering Profiles
- Category-based actions (allow, alert, block, continue, override)
- Custom URL categories
- Credential phishing prevention
- HTTP header insertion

### GlobalProtect Configuration
- Portal configuration
- Gateway configuration
- Authentication profiles (SAML, LDAP, RADIUS, client certificate)
- HIP profiles and HIP objects
- Split tunneling configuration
- Agent configuration (connect method, auto-restore)

### Address Objects and Groups
- IP netmask, IP range, IP wildcard mask, FQDN
- Address groups (static and dynamic)

### Service Connections
- IPSec tunnel configuration
- BGP routing
- Static routes
- QoS profiles

### Other SCM Objects
- Application filters and application groups
- Custom applications (signatures)
- External dynamic lists (EDL)
- Tags and tag groups
- Log forwarding profiles
- Security profile groups

## Output Format

Always output configurations as **SCM API-compatible JSON** payloads that can be directly used with the Strata Cloud Manager API:

```
POST https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}
```

Include:
1. The JSON payload body
2. The target API endpoint path
3. The required `folder` parameter (e.g., `"Prisma Access"`, `"Mobile Users"`, `"Remote Networks"`)
4. Any query parameters needed

## Best Practices to Follow

When generating configurations, always apply these Palo Alto Networks best practices:

1. **Security policies**: Use application-based rules instead of port-based; enable logging on all rules; apply security profiles to all allow rules
2. **Zone design**: Use distinct zones for Mobile Users, Remote Networks, and Service Connections
3. **Naming conventions**: Use clear, descriptive names with consistent prefixes (e.g., `PA-SEC-`, `PA-NAT-`, `PA-DEC-`)
4. **Rule ordering**: Place more specific rules before general rules; deny rules before allow rules where applicable
5. **Profile recommendations**: Apply best-practice security profile groups; use strict profiles for sensitive traffic
6. **Logging**: Enable log-at-session-end for all rules; configure log forwarding to a SIEM or Cortex Data Lake
