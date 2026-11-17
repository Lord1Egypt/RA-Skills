# Public-page evidence

Public-page evidence is an optional local input. It is not a license to browse a restricted service.
Obtain confirmation before an agent or browser opens an external provider page, and use only the
official HTTPS page for the exact single public IP.

## Workflow

1. Validate the exact public IP and confirm that the operator owns it or has authorization.
2. Explain the provider, page domain, target IP, visible fields to be recorded, and possible
   cross-border transfer. Obtain explicit confirmation for the external page access.
3. Open the official page in read-only mode. Do not log in, submit a form, solve CAPTCHA, bypass a
   rate limit, use a mirror, or defeat an access control.
4. Verify that the page visibly echoes the exact target IP.
5. Record only the concise fields below. Ignore generic marketing text, examples, search history,
   contacts, email addresses, names of individuals, hostnames, raw HTML, and free-text analysis.
6. Write one local JSON evidence file and pass it to the CLI with `--evidence`. The CLI validates
   the domain, target, timestamp, duplicate-provider rule, data type, and field allowlist.

If the page is blocked, requires login/CAPTCHA, changes layout, or does not echo the target, keep the
provider as `unavailable` or `not-requested`. Do not invent an empty success record.

## Official pages and fields

### IPinfo

URL: `https://ipinfo.io/{ip}`

Permitted visible fields: `country`, `country_code`, `region`, `city`, `asn`, `organization`,
`route_prefix`, `network_type`, `anycast`, `privacy`, `is_proxy`, `is_vpn`, `is_tor`, `is_hosting`,
`is_relay`, `is_residential_proxy`, `timezone`, `latitude`, `longitude`.

### Scamalytics

URL: `https://scamalytics.com/ip/{ip}`

Permitted visible fields: `risk_score`, `country`, `country_code`, `region`, `city`, `asn`, `isp`,
`organization`, `is_hosting`, `is_vpn`, `is_tor`, `is_proxy`, `is_bot`, and
`is_residential_proxy`. Use explicit result rows only; do not infer a positive flag from explanatory
prose.

### IPQualityScore

URL: `https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip}`

Permitted visible fields: `risk_score`, `country`, `region`, `city`, `asn`, `isp`, `is_proxy`,
`is_vpn`, `is_tor`, and `recent_abuse` when explicitly displayed for the target.

### ipdata

URL: `https://ipdata.co/{ip}`

Permitted visible fields: `trust_score`, `country`, `asn`, `organization`, `domain`, `route_prefix`,
`network_type`, `is_tor`, `is_vpn`, `is_hosting`, `is_proxy`, `is_relay`, `is_anonymous`, and
`blocklist_reports`. A threat token is positive only when it is an explicit field or boolean.

### Ping0.cc

URL: `https://ping0.cc/ip/{ip}`

The built-in adapter treats this as experimental. Permitted concise fields are `risk_score`, `asn`,
`country`, `region`, `city`, `organization`, `network_type`, `native_ip`, `native_classification`,
and explicit network flags. Verify the target IP particularly carefully.

## Evidence JSON

Use provider IDs `ipinfo`, `scamalytics`, `ipqs`, `ipdata`, or `ping0`. AbuseIPDB has no supported
public-page fallback and must use its independently configured header key through the official API.

```json
{
  "evidence": [
    {
      "provider": "ipqs",
      "target_ip": "<PUBLIC_IP>",
      "source_url": "https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/<PUBLIC_IP>",
      "observed_at": "2026-01-01T00:00:00Z",
      "data": {
        "risk_score": 0,
        "country": "<visible country>",
        "asn": "AS64500",
        "is_proxy": false,
        "is_vpn": false,
        "is_tor": false
      }
    }
  ]
}
```

The CLI rejects non-official domains, non-HTTPS URLs, non-default ports, user information,
credential query parameters, URLs without the target IP, target mismatches, duplicates, unknown
fields, invalid booleans/scores/ASN/CIDR values, and invalid timestamps. Evidence replaces only a
non-success selected provider result; a successful API result remains authoritative.
