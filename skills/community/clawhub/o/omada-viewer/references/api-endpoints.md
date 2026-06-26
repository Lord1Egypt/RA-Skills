# Omada Northbound API Endpoints Reference

Full endpoint reference for the TP-Link Omada Northbound API.

Base URL structure: `{controller_url}/openapi/v1/{omadacId}`

## Authentication

### Get Access Token
```
POST /openapi/authorize/token
Content-Type: application/json

{
  "grantType": "client_credentials",
  "clientId": "<client_id>",
  "clientSecret": "<client_secret>"
}
```

Response:
```json
{
  "errorCode": 0,
  "result": {
    "accessToken": "...",
    "tokenType": "Bearer",
    "expiresIn": 3600
  }
}
```

### Using the Token
Add header to all subsequent requests:
```
Authorization: AccessToken=<accessToken>
```

---

## Controller & Sites

### List Controllers
```
GET /openapi/v1/controllers
```

### List Sites
```
GET /openapi/v1/{omadacId}/sites
```

### Get Site Details
```
GET /openapi/v1/{omadacId}/sites/{siteId}
```

---

## Devices

### List All Devices
```
GET /openapi/v1/{omadacId}/sites/{siteId}/devices
```

### Get Device Details
```
GET /openapi/v1/{omadacId}/sites/{siteId}/devices/{deviceMac}
```

### List Gateways
```
GET /openapi/v1/{omadacId}/sites/{siteId}/gateways
```

### List Switches
```
GET /openapi/v1/{omadacId}/sites/{siteId}/switches
```

### List Access Points (EAPs)
```
GET /openapi/v1/{omadacId}/sites/{siteId}/eaps
```

---

## Clients

### List Connected Clients
```
GET /openapi/v1/{omadacId}/sites/{siteId}/clients
```

Query params:
- `page` (int): Page number
- `pageSize` (int): Items per page (max 1000)

### Get Client Details
```
GET /openapi/v1/{omadacId}/sites/{siteId}/clients/{clientMac}
```

---

## Switch Ports

### List Switch Ports
```
GET /openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}/ports
```

### Get Port Details
```
GET /openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}/ports/{portId}
```

---

## Gateway / WAN

### List Gateway Ports
```
GET /openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}/ports
```

---

## LAN Networks (VLANs)

### List LAN Networks
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/lan/networks
```

### Get Network Details
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/lan/networks/{networkId}
```

---

## DHCP

### Get DHCP Settings
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/lan/networks/{networkId}/dhcp
```

### List DHCP Reservations
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/lan/networks/{networkId}/dhcp/reservations
```

---

## Firewall / Port Forwarding

### List Port Forwarding Rules
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/firewall/portforwarding
```

---

## Wireless

### List SSIDs
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/wlans
```

### Get SSID Details
```
GET /openapi/v1/{omadacId}/sites/{siteId}/setting/wlans/{wlanId}
```

---

## Common Response Structure

All responses follow this pattern:
```json
{
  "errorCode": 0,
  "msg": "Success",
  "result": {
    "data": [...],
    "totalRows": 123,
    "currentPage": 1,
    "currentSize": 25
  }
}
```

Error codes:
- `0`: Success
- `-1`: Generic error
- `-40101`: Invalid token
- `-40301`: Access denied (check permissions)
- `-40401`: Resource not found

---

## Regional API URLs

Cloud-managed controllers use regional endpoints:
- **Europe**: `euw1-northbound-omada-controller.tplinkcloud.com`
- **US**: `use1-northbound-omada-controller.tplinkcloud.com`

Find your endpoint: Settings > Platform Integration > Open API > View > Interface Access Address

Self-hosted controllers use your controller's URL directly.
