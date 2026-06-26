---
name: octodns
description: Manage DNS zones across multiple providers using octoDNS ("DNS as code"). Use when you need to (1) manage DNS records in YAML format, (2) sync DNS zones between providers, (3) deploy DNS changes with version control, (4) bulk-update DNS records, or (5) migrate zones between DNS providers. Supports easyDNS, Route53, Cloudflare, NS1, and 50+ other DNS providers.
repository: https://github.com/easydns/octodns-skill
author: Mark E. Jeftovic (https://github.com/markjr)
---

# octoDNS - DNS as Code

Manage DNS zones declaratively across multiple providers using octoDNS. Think of it as "infrastructure as code" but for DNS records.

## ⚠️ CRITICAL SAFETY WARNING

**octoDNS operates on "desired state" - the YAML file represents the ENTIRE zone.**

**If the zone file has 1 record but DNS has 50 records, octoDNS will DELETE 49 records.**

**MANDATORY SAFETY WORKFLOW:**

1. **For existing zones: ALWAYS dump first** (`scripts/dump.sh`)
2. **ALWAYS preview before applying** (run without `--doit`)
3. **REVIEW the diff carefully** - unexpected "Delete" lines = DANGER
4. **Never assume** - verify the preview matches your intent

## Quick Start

### 1. Install octoDNS

```bash
scripts/install.sh
```

This installs octoDNS core plus the easyDNS provider.

### 2. Dump existing zone (REQUIRED for existing zones)

**If managing an existing zone with records already in DNS:**

```bash
scripts/dump.sh example.com.
```

This creates `config/example.com.yaml` with ALL current records. **Skipping this step will delete existing records!**

### 3. Create a config file

```bash
scripts/init_config.sh example.com
```

Creates `config/production.yaml` with easyDNS provider configured.

### 4. Define your zone

Create `config/example.com.yaml`:

```yaml
---
# Root record (@)
'':
  ttl: 300
  type: A
  value: 192.0.2.1

# www subdomain
www:
  ttl: 300
  type: CNAME
  value: example.com.

# Mail records
'':
  ttl: 300
  type: MX
  values:
    - priority: 10
      value: mail.example.com.
```

### 5. Preview changes (MANDATORY)

**Always preview first - look for unexpected Delete lines:**

```bash
scripts/sync.sh
```

(Note: dry-run is the default - no flag needed)

### 6. Apply changes (only when safe)

```bash
scripts/sync.sh --doit
```

## Common Operations

### Sync local YAML to DNS provider

```bash
scripts/sync.sh --zone example.com --doit
```

### Dump existing zone to YAML

```bash
scripts/dump.sh example.com
```

Creates `config/example.com.yaml` from live DNS.

### Validate zone file syntax

```bash
scripts/validate.sh config/example.com.yaml
```

### Sync between two providers

```bash
scripts/sync_providers.sh route53 easydns example.com
```

## Configuration

### Provider Setup

Edit `config/production.yaml`:

```yaml
providers:
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config
  
  easydns:
    class: octodns_easydns.EasyDnsProvider
    token: env/EASYDNS_TOKEN
    api_key: env/EASYDNS_API_KEY
    portfolio: env/EASYDNS_PORTFOLIO

zones:
  example.com:
    sources:
      - config
    targets:
      - easydns
```

### Environment Variables

Set these for easyDNS:

```bash
export EASYDNS_TOKEN="your-api-token"
export EASYDNS_API_KEY="your-api-key"
export EASYDNS_PORTFOLIO="your-portfolio-id"
```

## Supported Record Types

easyDNS provider supports:
- A, AAAA
- CNAME
- MX
- TXT
- NS
- SRV
- CAA
- NAPTR
- DS

## Advanced Usage

### Multiple Zones

Use dynamic zone config to manage all zones in a directory:

```yaml
zones:
  '*':
    sources:
      - config
    targets:
      - easydns
```

Any `.yaml` file in `config/` becomes a zone.

### Provider-to-Provider Migration

See [references/migration.md](references/migration.md) for migrating zones between DNS providers.

### Dynamic DNS Updates

See [references/dynamic-dns.md](references/dynamic-dns.md) for automated DNS updates from scripts.

## Workflow

1. Create/edit zone files in `config/`
2. Run `scripts/sync.sh --noop` to preview
3. Review changes
4. Run `scripts/sync.sh --doit` to apply
5. Commit zone files to git

## Troubleshooting

**"Provider not found"**: Install provider package:
```bash
pip install octodns-easydns
```

**"Authentication failed"**: Check environment variables are set correctly.

**"Zone not found"**: Ensure zone exists in DNS provider first, or use `--force` to create.

## Documentation

- octoDNS docs: https://octodns.readthedocs.io/
- easyDNS provider: https://github.com/octodns/octodns-easydns
- Record format guide: [references/records.md](references/records.md)
