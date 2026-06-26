# Practical Omada Endpoints

Use this file as the quick-start reference for common Omada diagnostics.

## Base Patterns

Controller-local discovery:
- `GET /api/info`

Authenticated site-scoped pattern:
- `/openapi/v1/{omadacId}/sites/{siteId}/...`

## Commonly Useful Endpoints

### Devices and Clients
```text
GET /openapi/v1/{omadacId}/sites/{siteId}/devices
GET /openapi/v1/{omadacId}/sites/{siteId}/devices/{deviceMac}
GET /openapi/v1/{omadacId}/sites/{siteId}/clients
GET /openapi/v1/{omadacId}/sites/{siteId}/clients/{clientMac}
```

### LAN / VLAN / DHCP
```text
GET /openapi/v1/{omadacId}/sites/{siteId}/lan-networks
GET /openapi/v1/{omadacId}/sites/{siteId}/lan-networks/{networkId}
GET /openapi/v1/{omadacId}/sites/{siteId}/networks/vlans
```

### NAT / Firewall
```text
GET /openapi/v1/{omadacId}/sites/{siteId}/nat/port-forwardings
GET /openapi/v1/{omadacId}/sites/{siteId}/firewall
GET /openapi/v1/{omadacId}/sites/{siteId}/firewall/timeout/default
GET /openapi/v1/{omadacId}/sites/{siteId}/insight/port-forwarding/{type}
```

### Gateway / WAN / Router Ports
```text
GET /openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}
GET /openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}/ports
GET /openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}/wan-status
GET /openapi/v1/{omadacId}/sites/{siteId}/gateways/{gatewayMac}/lan-status
GET /openapi/v1/{omadacId}/sites/{siteId}/internet/ports-config
GET /openapi/v1/{omadacId}/sites/{siteId}/internet/load-balance
GET /openapi/v1/{omadacId}/sites/{siteId}/internet/load-balance/status
```

### Switches / APs
```text
GET /openapi/v1/{omadacId}/sites/{siteId}/switches/{switchMac}/ports
GET /openapi/v1/{omadacId}/sites/{siteId}/port-status-ports
GET /openapi/v1/{omadacId}/sites/{siteId}/poe-ports
GET /openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}
GET /openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/ports
GET /openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/port-vlans
GET /openapi/v1/{omadacId}/sites/{siteId}/aps/{apMac}/vlan
```

## Notes

- Endpoint availability varies by controller version and hardware features
- Start with `devices`, `clients`, `lan-networks`, `nat/port-forwardings`, and gateway WAN/port endpoints
- If a controller exposes `v3/api-docs`, regenerate the broader catalog with `scripts/extract_endpoints.py`
