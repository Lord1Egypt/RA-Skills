# Provider reference

## Provider roles

| ID | Source | Primary role | Access |
|---|---|---|---|
| `ipqs` | IPQualityScore | fraud score, proxy, VPN, Tor, recent abuse | public page; API optional |
| `abuseipdb` | AbuseIPDB | community abuse confidence and reports | existing API key only |
| `scamalytics` | Scamalytics | fraud score, blacklists, proxy traits | public page; API optional |
| `ipdata` | ipdata | trust, threats, ASN, network | public page; API optional |
| `proxycheck` | proxycheck.io | proxy/VPN type and risk score | keyless; key optional |
| `ipapi-is` | ipapi.is | ASN/company and coarse network/risk flags | keyless |
| `ping0` | Ping0.cc | risk and native/hosting classification | keyless experimental page |
| `ipinfo` | IPinfo | geo, ASN/company, route, anonymization | public page; API optional |
| `ip-api` | IP-API | geo, ASN/ISP, mobile/proxy/hosting | keyless HTTP |
| `rdap` | RDAP.org/APNIC | registry allocation and contacts | keyless |
| `ripestat` | RIPEstat | announced prefix, origin, visibility | keyless |
| `geojs` | GeoJS | independent geo and ASN cross-check | keyless |

Existing credentials may activate official APIs automatically. Never request or expose them.
API success takes priority over imported public-page evidence.

When read-only page tooling is available, a skipped, unavailable, or failed IPQualityScore API
result must trigger an attempt to read its official public lookup page. If that page cannot be
validated, preserve the original source state and report the public-page coverage gap. AbuseIPDB
has no supported public-page fallback: without an existing credential, keep it as not collected.

## Presentation order

Order numeric risk and reputation channels by public recognition and risk relevance, never by
returned score: IPQualityScore, AbuseIPDB, Scamalytics, ipdata, proxycheck.io, ipapi.is, Ping0.cc.
Show a missing source as not collected, not zero. Distinguish IPQualityScore public-page coverage
failure from AbuseIPDB's credential requirement. Show a successful provider with no numeric field
as no numeric score returned. Show a provider with direct reputation booleans as a boolean-only,
unscored signal, not a numeric value. Always label Ping0.cc experimental.

Group provider detail tabs as follows:

1. Risk and reputation: IPQualityScore, AbuseIPDB, Scamalytics, ipdata, proxycheck.io, ipapi.is, Ping0.cc.
2. Network and privacy: IPinfo, IP-API.
3. Registry and routing: RDAP.org, RIPEstat.
4. Geolocation cross-check: GeoJS.

Ordering is presentation metadata, not universal authority. RDAP is authoritative for registry
allocation and RIPEstat for observed BGP routing; neither supplies a fraud score.

## Adapter cautions

- `ipapi.is` may return current flat fields (`ip`, `company_name`, `asn_num`, `asn_org`, `cc`,
  `lat`, `lon`) or older nested objects. Validate the echoed IP. Its `is_abuser` and `is_crawler`
  values are coarse unscored labels without an implied 0-100 score.
- IP-API's free endpoint is HTTP-only and may be blocked by secure networks.
- Ping0.cc has no stable arbitrary-IP JSON API. Validate page target echoes and treat parse failure
  as unavailable.
- Public pages may expose fewer or differently refreshed fields than paid APIs; label their
  collection method and apply the public-page numeric weight discount.
- IPinfo response fields depend on product tier. Scamalytics response shapes vary by integration.
