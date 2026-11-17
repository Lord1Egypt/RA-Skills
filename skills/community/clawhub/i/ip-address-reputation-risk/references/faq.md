# FAQ and troubleshooting

## Why did the default command not query providers?

That is the v2.0 safety default. `python scripts/ip_intelligence.py <PUBLIC_IP>` validates the
single public IP, reads any local evidence, and writes a local report. Sources are marked
`not-requested`, which is different from a failed request. Add `--external` only after reviewing
the target, provider list, transmitted field, and possible cross-border transfer.

Interactive runs show a `YES` prompt. Piped or scheduled runs also require `--confirm-external`:

```bash
python scripts/ip_intelligence.py 8.8.8.8 \
  --external --confirm-external --profile fast --format json
```

`--self` uses the same gate and cannot resolve the machine's IP before confirmation.

## Which profile should I use?

`fast` is the default and uses five keyless sources. `resilient` adds configured header-authenticated
providers while avoiding the experimental page source. `comprehensive` is opt-in and can involve
more recipients, including public-page-only providers that remain disabled for API collection.

## What do the source states mean?

- `success`: validated structured evidence returned;
- `skipped`: an enabled provider needs a missing configured credential;
- `not-requested`: no external request was made, or the provider API is disabled;
- `unavailable`: an experimental source could not be read or parsed;
- `error`: an enabled provider failed validation, transport, or upstream processing.

No non-success state is a negative finding. No numeric score means `unknown`, not safe or low risk.

## Why are some former APIs unavailable?

IP-API was removed because its former endpoint used plaintext HTTP. IPQualityScore, Scamalytics,
and ipdata API adapters are disabled because their former integrations could put credentials in URL
paths, query strings, or arbitrary configured endpoints. They can still be represented by validated
official public-page evidence imported locally.

## How are credentials handled?

Only independently configured `IPINFO_TOKEN` and `ABUSEIPDB_API_KEY` are supported. They are sent in
request headers. Do not put keys in arguments, URLs, evidence, reports, logs, or bug reports. A
provider's terms and data-transfer conditions remain the operator's responsibility.

## Why is an IP rejected?

The CLI accepts a literal global public IPv4 or IPv6 address only. It rejects hostnames, private,
loopback, link-local, reserved, multicast, unspecified, and documentation-only addresses. Resolve a
hostname through a separately authorized process, then choose one public IP explicitly.

## Why is a page source unavailable?

The page may be blocked, require login, present CAPTCHA, change layout, or fail to echo the exact IP.
Do not bypass the restriction or use a mirror. Keep the provider state unavailable and record the
coverage gap. Public-page evidence must use the official HTTPS domain and only the documented fields.

## How should reports be handled?

Reports contain the full IP and may contain geographic region, organization/ISP, route or allocation
prefixes, and risk labels. Set restrictive file permissions, avoid public Issues, demo sites, and
public logs, and delete reports under the organization's retention schedule. The reports contain no
raw upstream payloads, contacts, email addresses, or API keys.

The tool may transmit an IP to external providers and that transfer may be cross-border. The operator
must assess authorization, notice, lawful basis, personal-information handling, data-export rules,
retention, and provider contracts. This project is not legal advice.
