# DNS Record Format Reference

Complete guide to defining DNS records in octoDNS YAML format.

## Basic Structure

```yaml
---
# Record at zone apex (@)
'':
  ttl: 300
  type: A
  value: 192.0.2.1

# Subdomain
www:
  ttl: 300
  type: CNAME
  value: example.com.
```

## Common Record Types

### A / AAAA Records

Single value:
```yaml
'':
  ttl: 300
  type: A
  value: 192.0.2.1
```

Multiple values (round-robin):
```yaml
'':
  ttl: 300
  type: A
  values:
    - 192.0.2.1
    - 192.0.2.2
```

IPv6:
```yaml
'':
  ttl: 300
  type: AAAA
  value: 2001:db8::1
```

### CNAME

```yaml
www:
  ttl: 300
  type: CNAME
  value: example.com.
```

**Note**: CNAME targets must end with a dot (.) for absolute domains.

### MX Records

```yaml
'':
  ttl: 300
  type: MX
  values:
    - priority: 10
      value: mail1.example.com.
    - priority: 20
      value: mail2.example.com.
```

### TXT Records

Single value:
```yaml
'':
  ttl: 300
  type: TXT
  value: "v=spf1 include:_spf.google.com ~all"
```

Multiple values:
```yaml
'':
  ttl: 300
  type: TXT
  values:
    - "v=spf1 include:_spf.google.com ~all"
    - "google-site-verification=abc123"
```

### SRV Records

```yaml
_sip._tcp:
  ttl: 300
  type: SRV
  values:
    - priority: 10
      weight: 60
      port: 5060
      target: sipserver.example.com.
```

### NS Records

```yaml
subdomain:
  ttl: 3600
  type: NS
  values:
    - ns1.example.com.
    - ns2.example.com.
```

### CAA Records

```yaml
'':
  ttl: 300
  type: CAA
  values:
    - flags: 0
      tag: issue
      value: letsencrypt.org
    - flags: 0
      tag: iodef
      value: mailto:security@example.com
```

## Multiple Records on Same Name

You can have multiple record types for the same name:

```yaml
'':
  - ttl: 300
    type: A
    value: 192.0.2.1
  - ttl: 300
    type: MX
    values:
      - priority: 10
        value: mail.example.com.
  - ttl: 300
    type: TXT
    value: "v=spf1 mx ~all"
```

## Wildcard Records

```yaml
'*':
  ttl: 300
  type: A
  value: 192.0.2.1
```

Matches `anything.example.com`

## Zone Include

Reference another YAML file:

```yaml
# In main zone file
mail:
  $include: mail-config.yaml
```

## Comments

```yaml
# This is a comment
'':
  ttl: 300  # TTL in seconds
  type: A
  value: 192.0.2.1
```

## Tips

1. **Always use dots for absolute domains**: `example.com.` not `example.com`
2. **Relative names don't need dots**: `www` not `www.`
3. **TTL is in seconds**: 300 = 5 minutes, 3600 = 1 hour
4. **Use values (plural) for multiple records**: Even if you only have one now
5. **Quote TXT records**: Especially if they contain special characters

## Validation

Check syntax before applying:

```bash
scripts/validate.sh
```
