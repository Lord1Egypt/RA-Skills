# ip_api — IP geolocation (free, non-commercial)

## What this source has

ip-api.com returns geolocation and network metadata for IPv4 and IPv6 addresses: country, region, city, lat/lon, timezone, ISP, organization, AS number, mobile/proxy/hosting flags. Free tier is HTTP-only and explicitly non-commercial; the paid `pro.ip-api.com` tier offers HTTPS, higher rate limits, and commercial use.

Accuracy is ISP-grade — country level is reliable; city level is best-guess and often wrong by 50-200km. Mobile carrier and corporate IPs frequently geolocate to the carrier's HQ rather than the user.

Use ip-api for: country lookup from an IP, basic ASN/ISP attribution, "is this IP a known proxy/hosting provider". Pair with `geonames` for higher-precision place metadata once you have a country.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed (free tier) |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 45 req/min per source IP (free); resets per minute |

Exceed 45/min and the API returns `status: "fail"` with `message: "rate limit exceeded"` for the rest of the window. Free tier is HTTP only; HTTPS requires the paid tier.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `lookup` | Geolocate one IP | `ip` |

## Worked examples

```bash
# Look up an IP
python3 scripts/reach.py query ip_api lookup '{"ip": "8.8.8.8"}'

# Look up the caller's own IP (pass empty string)
python3 scripts/reach.py query ip_api lookup '{"ip": ""}'

# Request specific fields only (smaller payload)
python3 scripts/reach.py query ip_api lookup '{
  "ip": "1.1.1.1",
  "fields": "country,countryCode,city,lat,lon,isp,as,query"
}'
```

## Response shape

```json
{
  "status": "success",
  "country": "United States", "countryCode": "US",
  "region": "VA", "regionName": "Virginia", "city": "Ashburn",
  "zip": "20149", "lat": 39.03, "lon": -77.5,
  "timezone": "America/New_York",
  "isp": "Google LLC", "org": "Google Public DNS",
  "as": "AS15169 Google LLC",
  "query": "8.8.8.8"
}
```

`status: "fail"` returns `{status: "fail", message: "<reason>", query: "..."}`.

## Pitfalls

- **Free tier is HTTP only.** HTTPS requires `pro.ip-api.com` (paid). The connector's `base_url` is `http://...` deliberately.
- **Non-commercial only.** Free-tier ToS forbids commercial use. For commercial, switch to ipinfo.io, MaxMind, or pay for ip-api Pro.
- **`status` field.** Always check `status == "success"` — `"fail"` returns a different shape.
- **City-level accuracy is poor.** A residential IP often geolocates to the ISP's regional aggregation point, not the actual subscriber. Don't promise "where the user is" from this.
- **Rate-limit response is HTTP 200** with `status: "fail"`, not HTTP 429. Detect via the JSON, not the status code.
- **`fields` parameter** trims response. Default returns ~16 fields; explicit `fields` saves bytes and slightly improves latency.
- **Mobile/proxy/hosting flags** require paid tier. Free returns the basic location only.
- **IPv6 supported** but with reduced precision compared to IPv4.
- **Empty `ip` returns the caller's IP** — useful for "where are we egressing from" debugging.

## Source links

- API docs: https://ip-api.com/docs
- Free tier terms: https://ip-api.com/docs/legal
- Pro tier: https://members.ip-api.com/
