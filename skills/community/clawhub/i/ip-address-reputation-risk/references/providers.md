# Provider reference

The CLI is local-only unless `--external` is used after explicit confirmation. The request layer
allows only the HTTPS domains below, rejects credential-bearing URLs, and validates redirect
destinations. A provider being listed here does not establish that its terms, processing location,
retention, or data-transfer conditions are suitable for a particular deployment.

## Provider roles and domains

| ID | Source | Approved domain(s) | Collection mode | Credentials |
|---|---|---|---|---|
| `geojs` | GeoJS | `get.geojs.io` | keyless API | none |
| `rdap` | RDAP.org / ARIN bootstrap | `rdap.org`, `rdap-bootstrap.arin.net` | registry API | none |
| `ripestat` | RIPEstat | `stat.ripe.net` | routing API | none |
| `ipapi-is` | ipapi.is | `api.ipapi.is` | keyless API | none |
| `proxycheck` | proxycheck.io | `proxycheck.io` | keyless API | none |
| `ping0` | Ping0.cc | `ping0.cc`, `www.ping0.cc`, `ip.ping0.cc` | experimental public page | none |
| `ipinfo` | IPinfo | `api.ipinfo.io` | API; public page as local evidence | `IPINFO_TOKEN` header |
| `abuseipdb` | AbuseIPDB | `api.abuseipdb.com` | API only | `ABUSEIPDB_API_KEY` header |
| `ipqs` | IPQualityScore | `ipqualityscore.com`, `www.ipqualityscore.com` | public page as local evidence only | API disabled |
| `scamalytics` | Scamalytics | `scamalytics.com`, `www.scamalytics.com` | public page as local evidence only | API disabled |
| `ipdata` | ipdata | `ipdata.co`, `www.ipdata.co` | public page as local evidence only | API disabled |
| `self` | ipify | `api64.ipify.org` | `--self` resolver after confirmation | none |

The former IP-API HTTP adapter is removed. No environment variable can replace the allowlist or
select an arbitrary endpoint. The former Scamalytics URL/key configuration is unsupported.

## Profiles

`fast` is the CLI default and selects `rdap`, `ripestat`, `geojs`, `ipapi-is`, and `proxycheck`.
`resilient` adds configured header-authenticated providers and omits experimental Ping0. The
`comprehensive` profile is empty as a declaration and expands to all registered providers only when
explicitly selected. Public-page-only providers do not make API requests; they become useful when
validated evidence is supplied with `--evidence`.

Use `--providers` to explicitly choose a set and `--exclude` to remove entries. Keep the set small
enough that the confirmation prompt accurately reflects the intended recipients.

## Request and data controls

- Only one normalized public IP is sent as the target field.
- IPinfo and AbuseIPDB credentials are request headers, never URL components.
- Query parameters contain only target IP or provider options; credential parameter names are
  rejected by the URL validator.
- Concurrent external provider workers are capped at three, with a per-host minimum request
  interval. Retryable 429/5xx responses honor `Retry-After` within the provider timeout budget.
- An approved redirect must remain HTTPS, use an approved hostname, and use the default HTTPS port.
- Public-page evidence is read-only and must be captured from the official page without login,
  form submission, CAPTCHA handling, or access-control bypass.

## Source-state interpretation

| State | Meaning |
|---|---|
| `success` | Validated structured fields were returned. |
| `skipped` | An enabled provider needs a missing configured credential. |
| `not-requested` | The run was local-only or the provider API is disabled. |
| `unavailable` | An experimental source could not be read or parsed. |
| `error` | An enabled source failed validation, transport, or upstream processing. |

None of the non-success states is negative evidence. A provider without a numeric score remains
unscored; booleans are contextual signals and are not converted to invented risk points.

## Public-page evidence

IPQualityScore, Scamalytics, ipdata, and IPinfo public pages may be represented by local evidence
when the host has read the official page. The CLI validates the exact target IP, official HTTPS
hostname, observation timestamp, duplicate-provider rule, and field allowlist. It rejects raw
payloads, contacts, email addresses, `analysis`, and personalized hostname fields.

See [public-pages.md](public-pages.md) for the permitted page workflow and JSON shape.
