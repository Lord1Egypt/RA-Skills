# MyIPChecker API Reference

## Endpoint

- Method: `GET`
- Base URL: `https://myipchecker.ai`
- Path: `/api/ip`
- Auth: none observed during live requests
- Content type on success: `application/json`

## Purpose

Look up geolocation and network metadata for an IPv4 address.

If no `ip` query parameter is supplied, the endpoint returns metadata for the caller IP.

## Query Parameters

- `ip`: optional IPv4 address to look up

Observed behavior:

- `GET /api/ip` returns the caller IP information.
- `GET /api/ip?ip=8.8.8.8` returns metadata for `8.8.8.8`.
- `GET /api/ip?target=8.8.8.8` did not look up `8.8.8.8`; it behaved like a no-parameter request.

Do not advertise `target` as supported.

## Successful Response Shape

The deployed API returns a plain JSON object rather than a wrapped envelope.

Observed fields include:

- `ip`
- `country`
- `countryCode`
- `region`
- `city`
- `zip`
- `lat`
- `lon`
- `timezone`
- `isp`
- `org`
- `as`

Not every field is guaranteed to appear for every IP. Treat missing keys as normal.

## Observed Examples

### Caller IP lookup

Request:

```text
GET https://myipchecker.ai/api/ip
```

Observed response on 2026-03-30:

```json
{
  "ip": "103.224.172.246",
  "country": "HK",
  "countryCode": "HK",
  "city": "Hong Kong",
  "zip": "999077",
  "lat": 22.27832,
  "lon": 114.17469,
  "timezone": "Asia/Hong_Kong",
  "isp": "BACK WAVES LIMITED - HK",
  "org": "BACK WAVES LIMITED - HK",
  "as": "AS153371 BACK WAVES LIMITED - HK"
}
```

### Specific IP lookup

Request:

```text
GET https://myipchecker.ai/api/ip?ip=8.8.8.8
```

Observed response on 2026-03-30:

```json
{
  "ip": "8.8.8.8",
  "country": "US",
  "countryCode": "US",
  "region": "California",
  "city": "Mountain View",
  "zip": "94043",
  "lat": 37.4056,
  "lon": -122.0775,
  "timezone": "America/Los_Angeles",
  "isp": "AS15169 Google LLC",
  "org": "AS15169 Google LLC",
  "as": "AS15169 Google LLC"
}
```

## Failure Behavior

Observed on 2026-03-30:

- A default Python `urllib` request without a browser-style `User-Agent` was blocked by Cloudflare with HTTP `403` and error `1010`.
- `GET /api/ip?ip=exa_mple.com` returned HTTP `500`; the response body was not stable across clients and may be empty or may contain an error JSON object.

Design helpers and explanations around those facts:

- Always send a browser-like `User-Agent`.
- Distinguish HTTP or transport failures from successful lookups.
- Handle both empty and structured error bodies without crashing.
