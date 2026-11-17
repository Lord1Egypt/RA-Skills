# IP Intelligence Fusion

[English](README.md) | [简体中文](README.zh-CN.md)

[![Version](https://img.shields.io/badge/version-2.0.0-0969da)](scripts/ip_intelligence.py)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-2da44e)](LICENSE)

Auditable, multi-source intelligence for one public IPv4 or IPv6 address. The tool normalizes
registry, routing, geolocation, network-type, and reputation evidence into local JSON, Markdown,
or self-contained HTML reports.

This project is an investigation aid, not an automatic allow/deny, identity, location-proof, or
platform-review tool. The MIT license is not legal advice and is not a guarantee that a deployment
complies with Chinese law, another jurisdiction's law, provider terms, or an organization's policy.
See [COMPLIANCE.md](COMPLIANCE.md) before publishing or operating it.

## Scope

Supported use cases are limited to:

- checking infrastructure and public IPs owned by the operator;
- verifying information already published by a provider or registry;
- authorized security operations and abnormal-request triage;
- acceptance testing of proxy or network-provider deliveries where the operator has authorization.

The public v2.0 interface accepts exactly one public IP. It does not accept customer login logs,
account logs, cookies, device identifiers, device fingerprints, or batch IP datasets.

The following uses are prohibited by the project documentation and operating policy:

- unauthorized investigation or profiling of a person, customer, employee, or account;
- bulk collection of personal IP addresses or linking IPs with identity or account records;
- location spoofing, account farming, bulk registration, or evading platform review;
- bypassing CAPTCHA, login limits, access controls, or provider restrictions;
- port scanning, vulnerability exploitation, attacks, or proxy forwarding.

An IP may be personal information when it is linked with a person, account, customer, employee, or
login record. The operator must establish authorization, notice and lawful basis where required,
retention limits, and provider-contract compliance before using a result.

## Safety defaults

- The default mode is local-only. It validates the supplied IP, imports local evidence, and builds
  a report without making a network request.
- Remote lookups require `--external`. Interactive terminals always show a confirmation prompt;
  non-interactive runs also require `--confirm-external`.
- The prompt identifies the target IP, selected providers, approved domains, and possible
  cross-border transmission. This confirmation is an operation audit, not proof of legal authority.
- The default profile is `fast`. `comprehensive` must be selected explicitly.
- Only approved HTTPS domains are reachable. Redirects, user information, non-standard ports, and
  credential-bearing query parameters are rejected.
- Raw upstream responses, contact data, email addresses, and personalized hostnames are not
  collected into reports. API credentials, when supported, are sent in request headers only.

## Requirements

- Python 3.9 or later
- Standard library only
- Network access only when `--external` is intentionally enabled

## Quick start

Validate one IP and print a local-only JSON report. This command does not contact a provider:

```bash
python scripts/ip_intelligence.py 8.8.8.8 --format json
```

Generate local JSON and offline HTML files under `reports/`:

```bash
python scripts/ip_intelligence.py 8.8.8.8
```

Import the repository's synthetic public-page fixture for a local test. Evidence files are read
locally and are never fetched by the CLI:

```bash
python scripts/ip_intelligence.py 8.8.8.8 \
  --evidence tests/fixtures/public-page-evidence-8.8.8.8.json \
  --format markdown
```

Enable approved external providers after reviewing the confirmation prompt:

```bash
python scripts/ip_intelligence.py 8.8.8.8 --external --profile fast
```

For a scheduled or piped run, provide the non-interactive confirmation flag:

```bash
python scripts/ip_intelligence.py 8.8.8.8 \
  --external --confirm-external --profile fast --format json
```

Checking the machine's current public IP also requires both flags. The IP is resolved only after
confirmation:

```bash
python scripts/ip_intelligence.py --self --external --confirm-external --format json
```

Use `--providers` or `--exclude` to narrow a run. Use `--profile comprehensive` only when the
larger provider set and its additional transmissions are justified. `--include-raw` was removed
in v2.0 and is intentionally an unsupported argument.

## Provider boundaries

The following are the only CLI request domains in v2.0. Every request uses HTTPS and the final
response URL must remain on an approved host.

| Provider | Approved domain(s) | v2.0 collection mode |
|---|---|---|
| GeoJS | `get.geojs.io` | keyless API |
| RDAP | `rdap.org`, `rdap-bootstrap.arin.net` | registry API |
| RIPEstat | `stat.ripe.net` | routing API |
| ipapi.is | `api.ipapi.is` | keyless API |
| proxycheck.io | `proxycheck.io` | keyless API |
| Ping0.cc | `ping0.cc`, `www.ping0.cc`, `ip.ping0.cc` | experimental public page adapter |
| IPinfo | `api.ipinfo.io` | API with header token; public-page evidence is local input |
| AbuseIPDB | `api.abuseipdb.com` | API with header key |
| IPQualityScore | `ipqualityscore.com`, `www.ipqualityscore.com` | public-page evidence only |
| Scamalytics | `scamalytics.com`, `www.scamalytics.com` | public-page evidence only |
| ipdata | `ipdata.co`, `www.ipdata.co` | public-page evidence only |
| `--self` resolver | `api64.ipify.org` | only after confirmation |

The former IP-API HTTP adapter is removed. IPQualityScore, Scamalytics, and ipdata API adapters are
disabled because their previous integrations required credentials in URL paths, queries, or an
arbitrary endpoint. Public-page evidence must be captured from the official page, match the exact
target IP, and contain only allowlisted fields. Do not log in, submit forms, solve CAPTCHA, or
bypass an access control to obtain it.

## Credentials

Credentials are optional and are never requested by the CLI. If an operator has independently
configured an approved provider, the supported variables are:

| Provider | Variable | Transport |
|---|---|---|
| IPinfo | `IPINFO_TOKEN` | `Authorization: Bearer ...` header |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | `Key` request header |

Keys must never be placed in command arguments, evidence files, URLs, reports, logs, or issue
attachments. Provider terms, processing locations, retention, and transfer conditions must be
checked separately.

## Reports and data handling

Reports contain the complete target IP and may contain geographic region, organization/ISP,
allocation or route prefixes, and network-risk labels. The report metadata states:

```json
{
  "policy": {
    "network_mode": "local-only",
    "confirmation_mode": null,
    "sent_fields": [],
    "policy_version": "2.0"
  },
  "data_policy": {
    "accepted_input": "single public IP",
    "personal_data_mode": "not intended for customer or account logs",
    "raw_payloads": false,
    "contact_data": false
  }
}
```

In external mode, the policy records `external-confirmed` and the provider domains that actually
started requests. Set restrictive file permissions, do not upload reports to public Issues,
demonstration sites, or shared public logs, and delete them according to the organization's
retention schedule.

## Migration from 1.4.x

v2.0 is a breaking release:

- the default command no longer contacts the network;
- remote access requires `--external` and explicit confirmation;
- the default provider profile is `fast`; `comprehensive` is opt-in;
- raw response output and `--include-raw` are removed;
- the IP-API plaintext adapter is removed;
- the former credential-in-URL adapters are disabled;
- the report schema and CLI version are `2.0` and `2.0.0`;
- old ZIP archives and package directories are not official release artifacts.

## Development

```bash
py -3 -m unittest discover -s tests -v
py -3 -m py_compile scripts/ip_intelligence.py tests/test_ip_intelligence.py
py -3 scripts/release_audit.py
```

Only audited source, documentation, tests, and the license belong in a release. Do not commit
archives, caches, generated reports, real query results, raw responses, or secrets.

## License

Released under the [MIT License](LICENSE). The license does not provide legal advice or a
compliance warranty.
