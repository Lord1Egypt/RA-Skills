# Migrating DNS Zones Between Providers

Guide for migrating DNS zones from one provider to another using octoDNS.

## Overview

octoDNS makes provider-to-provider migration straightforward:

1. Dump existing zone from source provider
2. Review and clean up the YAML
3. Configure target provider
4. Sync to target provider

## Step-by-Step Migration

### 1. Dump from Source Provider

Create a config for the source provider (e.g., Route53):

```yaml
# config/source.yaml
providers:
  route53:
    class: octodns_route53.Route53Provider
    access_key_id: env/AWS_ACCESS_KEY_ID
    secret_access_key: env/AWS_SECRET_ACCESS_KEY
  
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config

zones:
  example.com:
    sources:
      - route53
    targets:
      - config
```

Dump the zone:

```bash
scripts/dump.sh example.com
```

This creates `config/example.com.yaml` with all existing records.

### 2. Review and Clean Up

Check the dumped YAML:

```bash
cat config/example.com.yaml
```

Remove or update:
- Provider-specific records you don't want to migrate
- Records managed by other systems
- Outdated or test records

### 3. Configure Target Provider

Update `config/production.yaml`:

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

### 4. Preview the Migration

Dry-run to see what will be created:

```bash
scripts/sync.sh --zone example.com --noop
```

Review the output carefully. octoDNS will show:
- Creates: New records to be added
- Updates: Records that differ from source
- Deletes: Records in target but not in source

### 5. Apply the Migration

When ready:

```bash
scripts/sync.sh --zone example.com --doit
```

### 6. Verify

Check records in the new provider:

```bash
dig @ns1.easydns.com example.com
dig @ns1.easydns.com www.example.com
```

## Dual-Provider Sync

Keep two providers in sync (for redundancy):

```yaml
zones:
  example.com:
    sources:
      - config
    targets:
      - route53
      - easydns
```

Changes in YAML are applied to both providers.

## Incremental Migration

Migrate subdomains separately:

```yaml
# Migrate mail.example.com first
zones:
  mail.example.com:
    sources:
      - config
    targets:
      - easydns
  
  # Keep main domain on old provider for now
  example.com:
    sources:
      - config
    targets:
      - route53
```

## Common Issues

### NS Records

- octoDNS may try to set apex NS records
- Most providers manage these automatically
- Use `ignored` to skip NS record management:

```yaml
zones:
  example.com:
    sources:
      - config
    targets:
      - easydns
    ignored:
      - '': [NS]
```

### SOA Records

SOA records are provider-managed. octoDNS handles them automatically.

### TTL Differences

Some providers have minimum TTL values. octoDNS will warn if your TTL is too low.

### Record Type Support

Not all providers support all record types. Check provider documentation:
- https://github.com/octodns/octodns-easydns#support-information

## Rollback

If something goes wrong:

1. Keep old provider config
2. Point DNS back to old provider's nameservers
3. Fix issues in YAML
4. Re-sync

## Provider-Specific Notes

### easyDNS
- Supports full NS record management
- Default portfolio must be configured
- Currency defaults to CAD

### Route53
- Automatically manages apex NS/SOA
- Uses AWS credentials
- Regional configuration available

### Cloudflare
- Proxy records not supported by octoDNS
- Use TTL=1 (auto) for proxied records

## Testing Strategy

1. **Test zone first**: Create a test domain and migrate that first
2. **Non-production migration**: Migrate staging environments before production
3. **Backup**: Keep YAML dumps of all zones
4. **Gradual cutover**: Update NS records gradually (short TTL first)
5. **Monitor**: Watch for DNS resolution issues after migration
