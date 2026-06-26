---
name: omada-viewer
description: Read-only diagnostics for TP-Link Omada SDN controllers via the Open API. Use when inspecting Omada devices, clients, VLANs, LAN networks, WAN status, router ports, switch ports, DHCP ranges, port forwards, or general controller/network health. Requires user-provided Omada Open API credentials and HTTPS access to the user's controller. Best for troubleshooting and inventory, not config changes.
---

# Omada Viewer

**Read-only diagnostics for TP-Link Omada SDN controllers via the Open API.**

## What it does

Use this skill to inspect:
- Devices
- Clients
- VLANs / LAN networks
- WAN status
- Router ports
- Switch ports
- DHCP ranges
- Port forwards
- General controller health

## What it does NOT do

- Does **not** make configuration changes
- Does **not** create, edit, or delete controller settings
- Does **not** require Admin role for normal use

## Requirements

This skill **does require**:
- A reachable Omada controller over **HTTPS**
- A user-created **Open API application** in Omada
- User-provided credentials for that API app

Recommended role:
- **Viewer**

Required configuration:
- `OMADA_URL`
- `OMADA_CLIENT_ID`
- `OMADA_CLIENT_SECRET`

Optional configuration:
- `OMADA_OMADAC_ID`
- `OMADA_SITE`
- `OMADA_VERIFY_SSL`

## Quick Setup

1. In Omada, go to:
   - **Settings > Platform Integration > Open API**
2. Create an application in:
   - **Client mode**
3. Prefer this permission level:
   - **Viewer**
4. Store credentials locally, not in chat

## Common Commands

```bash
python scripts/omada_query.py summary
python scripts/omada_query.py clients
python scripts/omada_query.py devices
python scripts/omada_query.py vlans
python scripts/omada_query.py port-forwards
python scripts/omada_query.py wan-status
python scripts/omada_query.py router-summary
```

## Authentication

Use client credentials mode:

```http
POST {base_url}/openapi/authorize/token?grant_type=client_credentials
Content-Type: application/json

{
  "omadacId": "<omadac_id>",
  "client_id": "<client_id>",
  "client_secret": "<client_secret>"
}
```

Successful responses return:
- `accessToken`
- `refreshToken`
- `expiresIn`

Use the token like this:

```http
Authorization: AccessToken=<accessToken>
```

Important notes:
- Send JSON as UTF-8 **without BOM**
- Some local controllers allow `omadacId` discovery from `GET /api/info`

## Core Read Endpoints

All site-scoped paths below are relative to:

```text
/openapi/v1/{omadacId}/sites/{siteId}
```

### Discovery
- `GET /api/info`
- `GET /openapi/v1/{omadacId}/sites?page=1&pageSize=100`

### Devices and Clients
- `GET /devices?page=1&pageSize=200`
- `GET /devices/{deviceMac}`
- `GET /clients?page=1&pageSize=200`
- `GET /clients/{clientMac}`

### LAN / VLAN / DHCP
- `GET /lan-networks?page=1&pageSize=50`
- `GET /lan-networks/{networkId}`
- `GET /networks/vlans`

Typical LAN network responses may include:
- VLAN ID
- Gateway subnet
- DHCP range
- DNS settings
- Lease time

### Port Forwards / NAT / Firewall
- `GET /nat/port-forwardings?page=1&pageSize=50`
- `GET /firewall`
- `GET /firewall/timeout/default`
- `GET /insight/port-forwarding/{type}`

### Gateway / WAN / Router Ports
- `GET /gateways/{gatewayMac}`
- `GET /gateways/{gatewayMac}/ports`
- `GET /gateways/{gatewayMac}/wan-status`
- `GET /gateways/{gatewayMac}/lan-status`
- `GET /internet/ports-config`
- `GET /internet/load-balance`
- `GET /internet/load-balance/status`
- `GET /health/gateways/{gatewayMac}/wans/details`

### Switches / APs
- `GET /switches/{switchMac}/ports`
- `GET /port-status-ports`
- `GET /poe-ports`
- `GET /aps/{apMac}`
- `GET /aps/{apMac}/ports`
- `GET /aps/{apMac}/port-vlans`
- `GET /aps/{apMac}/vlan`

## Script Commands

Use `scripts/omada_query.py` for quick diagnostics.

Supported commands:

```bash
python scripts/omada_query.py sites
python scripts/omada_query.py devices
python scripts/omada_query.py clients
python scripts/omada_query.py vlans
python scripts/omada_query.py dhcp-reservations
python scripts/omada_query.py port-forwards
python scripts/omada_query.py switch-ports <switch_mac>
python scripts/omada_query.py wan-ports
python scripts/omada_query.py wan-status
python scripts/omada_query.py router-ports
python scripts/omada_query.py router-summary
python scripts/omada_query.py summary
```

## Included References

- `references/api-endpoints.md` — compact endpoint reference
- `references/discovered-endpoints.md` — practical starting endpoints
- `references/all-endpoints.md` — categorized endpoint catalog
- `scripts/extract_endpoints.py` — regenerate endpoint catalog from an OpenAPI export

## Security Notes

- Prefer **Viewer** role for normal use
- Never paste secrets into chat
- Keep read-only diagnostics separate from any future admin/write skill
- If you later publish a write-capable version, use a separate Admin-scoped API app

## Troubleshooting

- **401 / auth failures**: verify Client mode, credentials, and `grant_type=client_credentials`
- **Invalid credential errors**: confirm exact `client_id`, `client_secret`, and `omadacId`
- **SSL errors**: local controllers with self-signed certs may require SSL verification disabled
- **Missing endpoints**: API coverage varies by controller version, model, and enabled features
- **Unexpected JSON/auth issues**: ensure request body is UTF-8 without BOM
