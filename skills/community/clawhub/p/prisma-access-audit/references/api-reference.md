# Prisma Access API Reference

API endpoints, authentication, and response structures for auditing Palo Alto
Prisma Access tenants. Covers Strata Cloud Manager (SCM) API, legacy Panorama
Cloud Services API, and Prisma Access Insights API.

## Authentication

### Strata Cloud Manager — OAuth 2.0 Client Credentials Flow

Strata Cloud Manager uses OAuth 2.0 with a Service Account bound to a Tenant
Service Group (TSG). All API calls require a Bearer token obtained from the
token endpoint.

**Token Request:**

```
POST https://auth.apps.paloaltonetworks.com/oauth2/access_token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=<service_account_client_id>
&client_secret=<service_account_client_secret>
&scope=tsg_id:<your_tsg_id>
```

**Token Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 899,
  "scope": "tsg_id:1234567890"
}
```

- Tokens expire in 899 seconds (~15 minutes). Cache and refresh proactively.
- The `scope` field must include the TSG ID. Omitting it returns 401.
- The Service Account requires a minimum role of `Auditor` or `View-Only
  Administrator` for read-only audit access.

**Using the token:**

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/<resource>
Authorization: Bearer <access_token>
```

### Legacy Panorama Cloud Services API

For tenants still managed via Panorama with the Cloud Services plugin, use
the standard PAN-OS XML API with an API key generated from Panorama:

```
GET https://<panorama_ip>/api/?type=keygen&user=<username>&password=<password>
```

Returns an API key for subsequent requests:

```
GET https://<panorama_ip>/api/?type=config&action=get&xpath=<xpath>&key=<api_key>
```

Legacy API returns XML. Configuration paths for Prisma Access objects live
under the cloud services device group hierarchy in Panorama. If the tenant
has migrated to Strata Cloud Manager, the legacy API may return stale data.
Always confirm which management plane is authoritative before auditing.

## Strata Cloud Manager API Endpoints

Base URL: `https://api.sase.paloaltonetworks.com/sse/config/v1`

All endpoints accept the `folder` query parameter to scope results to a
specific policy folder: `Mobile Users`, `Remote Networks`, `Service Connections`,
or `Shared`.

### Security Policies

**List security rules:**

```
GET /security-rules?folder=Mobile Users
GET /security-rules?folder=Remote Networks
```

Response fields per rule:
- `name` — rule name
- `source` — source address objects/groups
- `destination` — destination address objects/groups
- `from` — source zone list
- `to` — destination zone list
- `application` — App-ID list or `["any"]`
- `service` — service objects or `["application-default"]` / `["any"]`
- `action` — `allow`, `deny`, `drop`, `reset-client`, `reset-server`, `reset-both`
- `profile_setting` — Security Profile Group or individual profiles
- `disabled` — boolean
- `log_start` / `log_end` — logging flags
- `tag` — administrative tags

**List decryption rules:**

```
GET /decryption-rules?folder=Mobile Users
GET /decryption-rules?folder=Remote Networks
```

**List NAT rules:**

```
GET /nat-rules?folder=Mobile Users
GET /nat-rules?folder=Remote Networks
```

### Security Profiles and Profile Groups

**Security Profile Groups:**

```
GET /security-profile-groups?folder=Shared
```

Response includes the bound profile names for each type: `virus`,
`spyware`, `vulnerability`, `url-filtering`, `file-blocking`,
`wildfire-analysis`, `data-filtering`.

**Individual profiles:**

```
GET /anti-spyware-profiles?folder=Shared
GET /vulnerability-protection-profiles?folder=Shared
GET /wildfire-anti-virus-profiles?folder=Shared
GET /url-filtering-profiles?folder=Shared
GET /dns-security-profiles?folder=Shared
GET /file-blocking-profiles?folder=Shared
GET /data-filtering-profiles?folder=Shared
```

### Address Objects and Groups

```
GET /addresses?folder=Shared
GET /address-groups?folder=Shared
```

Address objects include `ip_netmask`, `ip_range`, `ip_wildcard`, or `fqdn`
type fields. Address groups reference member address objects by name.

### Application Filters and Groups

```
GET /application-filters?folder=Shared
GET /application-groups?folder=Shared
```

### Remote Networks

**List remote network sites:**

```
GET /remote-networks
```

Response fields per site:
- `name` — site name
- `region` — Prisma Access compute location
- `ike_gateway` — reference to IKE gateway configuration
- `ipsec_tunnel` — reference to IPSec tunnel configuration
- `subnets` — local subnets behind the remote network site

**IKE gateways:**

```
GET /ike-gateways
```

Response includes `peer_address`, `authentication` (pre-shared-key or
certificate), `protocol` (IKEv1/IKEv2), `crypto_profile` reference.

**IPSec tunnels:**

```
GET /ipsec-tunnels
```

Response includes `auto_key` (IKE gateway reference, proxy IDs),
`crypto_profile` reference.

**IKE and IPSec crypto profiles:**

```
GET /ike-crypto-profiles
GET /ipsec-crypto-profiles
```

Crypto profiles define encryption algorithm (AES-128/256-CBC, AES-128/256-GCM),
hash (SHA256/SHA384/SHA512), DH group (14/19/20), and SA lifetime.

**BGP routing:**

```
GET /bgp-routing
```

Returns BGP configuration per remote network site: peer ASN, local ASN,
advertised prefixes, route filters, and authentication settings.

### Mobile Users

**Mobile user regions:**

```
GET /mobile-users/regions
```

Returns configured compute locations for mobile user GlobalProtect
connectivity.

**GlobalProtect agent settings:**

```
GET /mobile-agent/global-settings
```

Returns portal and gateway configuration: authentication profiles,
split-tunnel settings, client certificate requirements.

**HIP objects and profiles:**

```
GET /hip-objects
GET /hip-profiles
```

HIP objects define compliance checks (OS patch, disk encryption, antivirus).
HIP profiles combine objects into enforcement policies referenced in
security rules.

### Service Connections

```
GET /service-connections
```

Response fields per connection:
- `name` — connection name
- `region` — Prisma Access compute location
- `ike_gateway` — IKE gateway reference
- `ipsec_tunnel` — IPSec tunnel reference
- `subnets` — on-premises subnets reachable via this connection
- `bgp` — BGP peering configuration
- `qos` — QoS bandwidth allocation and traffic classification

## Prisma Access Insights API

Prisma Access Insights provides operational telemetry and monitoring data.
The API base URL differs from the configuration API:

Base URL: `https://pa-<region>.api.prismaaccess.com/api/sase/v2.0`

Authentication uses the same OAuth 2.0 token from Strata Cloud Manager.

### Key Endpoints

**Tunnel status (remote networks and service connections):**

```
POST /resource/tenant/<tsg_id>/custom/query/prisma_sase_external_network
{
  "properties": [
    {"property": "site_name"},
    {"property": "tunnel_status"},
    {"property": "node_type"},
    {"property": "last_status_change"}
  ],
  "filter": {
    "operator": "AND",
    "rules": [
      {"property": "tunnel_status", "operator": "equals", "values": ["down"]}
    ]
  }
}
```

**Mobile user connection telemetry:**

```
POST /resource/tenant/<tsg_id>/custom/query/prisma_sase_connected_user
{
  "properties": [
    {"property": "user_name"},
    {"property": "gphost_hostip"},
    {"property": "gpclient_version"},
    {"property": "compute_location"},
    {"property": "hip_status"}
  ]
}
```

**Bandwidth utilization:**

```
POST /resource/tenant/<tsg_id>/custom/query/prisma_sase_bandwidth
{
  "properties": [
    {"property": "site_name"},
    {"property": "allocated_bandwidth_mbps"},
    {"property": "used_bandwidth_mbps"},
    {"property": "utilization_pct"}
  ],
  "filter": {
    "operator": "AND",
    "rules": [
      {"property": "utilization_pct", "operator": "greater_than", "values": [70]}
    ]
  }
}
```

**GlobalProtect client version distribution:**

```
POST /resource/tenant/<tsg_id>/custom/query/prisma_sase_gp_client_versions
{
  "properties": [
    {"property": "gpclient_version"},
    {"property": "count"}
  ]
}
```

## Common Response Structure

All Strata Cloud Manager configuration API responses follow a consistent
envelope:

```json
{
  "data": [
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "resource-name",
      "folder": "Mobile Users",
      ...resource-specific fields...
    }
  ],
  "offset": 0,
  "total": 42,
  "limit": 200
}
```

- `data` — array of resource objects
- `offset` — pagination offset (0-based)
- `total` — total matching resources
- `limit` — maximum resources returned per request (default 200)

For paginated results, increment `offset` by `limit` until `offset >= total`:

```
GET /security-rules?folder=Mobile Users&offset=0&limit=200
GET /security-rules?folder=Mobile Users&offset=200&limit=200
```

### Error Responses

```json
{
  "_errors": [
    {
      "code": "E003",
      "message": "Invalid Object",
      "details": {
        "errorType": "Invalid Object",
        "message": "Detailed error description"
      }
    }
  ],
  "_request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

Common error codes:
- `401 Unauthorized` — token expired or invalid TSG ID in scope
- `403 Forbidden` — Service Account lacks required role
- `404 Not Found` — resource or folder does not exist
- `429 Too Many Requests` — rate limit exceeded (see below)

## Rate Limiting

Strata Cloud Manager API enforces rate limits per Service Account:

| Endpoint Category | Rate Limit | Window |
|-------------------|-----------|--------|
| Configuration read (`GET`) | 60 requests | per minute |
| Configuration write (`POST/PUT/DELETE`) | 30 requests | per minute |
| Prisma Access Insights queries | 120 requests | per minute |

When rate-limited, the API returns `429 Too Many Requests` with a
`Retry-After` header indicating seconds to wait. For audit workflows:

- Batch configuration reads to minimize API calls — retrieve full resource
  lists rather than individual objects.
- Use pagination (`limit=200`) to reduce the number of calls for large
  rulebases.
- Cache responses during the audit session — configuration data is
  point-in-time and does not change during the audit window.
- For Prisma Access Insights, use time-bounded queries to avoid scanning
  the full data lake on each call.

## API Version Notes

- Strata Cloud Manager API uses versioned paths (`/sse/config/v1/`). Check
  release notes for breaking changes when Palo Alto Networks increments the
  API version.
- Prisma Access Insights API version (`/api/sase/v2.0/`) may differ by
  region. The region prefix in the base URL (`pa-<region>`) corresponds to
  the tenant's primary compute region.
- Legacy Panorama API does not version Prisma Access-specific xpaths
  differently from on-premises configuration. Cloud Services plugin
  version determines available features.
