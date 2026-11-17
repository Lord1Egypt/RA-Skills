# Public-page collection

Use this workflow only when the execution host actually provides a read-only browser or web-reading
tool. Do not assume the capability exists. These official pages supported ordinary single-IP
lookups without a new account when this skill was published, but availability and visible fields
can change at execution time.

## Workflow

1. Run the CLI baseline for the exact public IP and inspect every provider state.
2. For each supported provider whose API result is skipped, unavailable, or failed, open its
   official URL below directly. A successful API result is authoritative and needs no fallback.
3. Verify the result heading or body visibly echoes the exact target IP.
4. Extract only visible target-specific result fields listed below. Ignore marketing copy, recent
   searches, examples, generic feature descriptions, and locked fields.
5. If blocked by login, CAPTCHA, consent that requires transmitting data, or an unavailable page,
   skip that source. Do not bypass the restriction, use search snippets, or use third-party mirrors
   as evidence.
6. Write one JSON evidence file using the schema below and pass it with `--evidence`.

## Official pages and fields

### IPinfo

URL: `https://ipinfo.io/{ip}`

Record visible values from Summary, Geolocation, Anonymization, ASN, Company, and Abuse. Useful
fields: `country`, `country_code`, `region`, `city`, `asn`, `organization`, `route_prefix`,
`reverse_dns`, `network_type`, `anycast`, `privacy`, `is_proxy`, `is_vpn`, `is_tor`, `is_hosting`,
`is_relay`, `is_residential_proxy`, `timezone`, `latitude`, `longitude`.

Anonymization pages may show one detected trait and several unlabeled alternatives. Record a
boolean only when the page clearly pairs that exact label with Detected/True/False.

### Scamalytics

URL: `https://scamalytics.com/ip/{ip}`

Record `risk_score` from “Fraud Score”, plus visible `country`, `country_code`, `region`, `city`,
`asn`, `isp`, `organization`, `reverse_dns`, `is_hosting` (Datacenter or Server), `is_vpn`,
`is_tor`, `is_proxy` (Public Proxy or Web Proxy), `is_bot` (Search Engine Robot), and
`is_residential_proxy`. Do not treat explanatory phrases such as “could be proxying” as a
positive flag. Use explicit Yes/No result rows only.

### IPQualityScore

URL: `https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip}`

Record `risk_score` from the target-specific score “N out of 100”, plus `country`, `region`,
`city`, `asn`, `isp`, `reverse_dns`, `is_proxy`, `is_vpn`, `is_tor`, and `recent_abuse` when
explicitly displayed. Ignore generic prose elsewhere on the page describing what VPNs, proxies,
or bots can do.

Treat the IPQualityScore page as the required fallback when its API is skipped, unavailable, or
failed and the host has read-only page tooling. If the page cannot be validated, retain the
baseline state; do not create an empty evidence item or turn absence into zero risk.

### ipdata

URL: `https://ipdata.co/{ip}`

Record `trust_score` exactly as displayed; the CLI converts it to reputation risk using
`100 - trust_score`. Also record `country`, `asn`, `organization`, `domain`, `route_prefix`,
`network_type`, `is_tor`, `is_vpn`, `is_hosting` (DATACENTER), `is_proxy`, `is_relay` (PRIVACY
RELAY), `is_anonymous`, and `blocklist_reports`. A listed threat token is positive. Do not copy
the generic country-guide paragraph into `analysis`.

### Ping0.cc

URL: `https://ping0.cc/ip/{ip}`

The CLI already attempts this page. Host-tool evidence is useful only if the built-in adapter is
unavailable. Record explicit `risk_score`, `asn`, `country`, `region`, `city`, `organization`,
`network_type`, `native_ip`, and network flags. Treat this source as experimental and verify the
target IP particularly carefully.

## Evidence JSON

Use provider IDs `ipinfo`, `scamalytics`, `ipqs`, `ipdata`, or `ping0`.

AbuseIPDB is intentionally absent from this schema. Use only its official API when an existing
`ABUSEIPDB_API_KEY` is already configured. Do not collect AbuseIPDB through a public page.

```json
{
  "evidence": [
    {
      "provider": "ipqs",
      "target_ip": "<runtime public IP>",
      "source_url": "https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/<runtime public IP>",
      "observed_at": "<ISO 8601 observation time>",
      "data": {
        "risk_score": 0,
        "country": "<visible country>",
        "asn": "<visible ASN>",
        "is_proxy": false,
        "is_vpn": false,
        "is_tor": false
      }
    }
  ]
}
```

The CLI rejects non-official domains, non-HTTPS URLs, URLs that do not contain the target IP,
target mismatches, duplicate providers, unknown fields, invalid booleans/scores/ASN/CIDR, and
invalid timestamps. Evidence replaces only a skipped, unavailable, or failed provider result;
successful API results remain authoritative.
