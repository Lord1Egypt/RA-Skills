# OpenProvider — Nameserver Management

> **Atlas Status:** Atlas uses the fixed nameserver group `dns-openprovider` for all domains. Direct nameserver management is NOT yet implemented but documented here for reference.

---

## List Nameserver Groups

### GET /dns/nameservers/groups

List all nameserver groups in the account.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/dns/nameservers/groups`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page |
| `offset` | integer | Pagination offset |
| `ns_group_pattern` | string | Wildcard search for group names |

**curl Example:**

```bash
curl -X GET "https://api.openprovider.eu/v1beta/dns/nameservers/groups?limit=100" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "code": 0,
  "desc": "",
  "data": {
    "results": [
      {
        "ns_group": "dns-openprovider",
        "nameservers": [
          { "name": "ns1.openprovider.nl", "ip": "37.60.231.108" },
          { "name": "ns2.openprovider.be", "ip": "37.123.101.100" },
          { "name": "ns3.openprovider.eu", "ip": "37.123.101.132" }
        ]
      }
    ],
    "total": 3
  }
}
```

---

## Get Nameserver Group

### GET /dns/nameservers/groups/{ns_group}

Get details of a specific nameserver group.

**Endpoint:** `GET https://api.openprovider.eu/v1beta/dns/nameservers/groups/{ns_group}`

**curl Example:**

```bash
curl -X GET https://api.openprovider.eu/v1beta/dns/nameservers/groups/dns-openprovider \
  -H "Authorization: Bearer $TOKEN"
```

---

## Create Nameserver Group

### POST /dns/nameservers/groups

Create a custom nameserver group.

**Endpoint:** `POST https://api.openprovider.eu/v1beta/dns/nameservers/groups`

**Request:**

```json
{
  "ns_group": "my-custom-ns",
  "nameservers": [
    { "name": "ns1.example.com", "ip": "1.2.3.4" },
    { "name": "ns2.example.com", "ip": "5.6.7.8" }
  ]
}
```

**curl Example:**

```bash
curl -X POST https://api.openprovider.eu/v1beta/dns/nameservers/groups \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ns_group": "my-custom-ns",
    "nameservers": [
      {"name": "ns1.example.com", "ip": "1.2.3.4"},
      {"name": "ns2.example.com", "ip": "5.6.7.8"}
    ]
  }'
```

---

## Update Nameserver Group

### PUT /dns/nameservers/groups/{ns_group}

Update nameservers in an existing group.

**Endpoint:** `PUT https://api.openprovider.eu/v1beta/dns/nameservers/groups/{ns_group}`

**Request:**

```json
{
  "nameservers": [
    { "name": "ns1.example.com", "ip": "10.20.30.40" },
    { "name": "ns2.example.com", "ip": "50.60.70.80" }
  ]
}
```

---

## Delete Nameserver Group

### DELETE /dns/nameservers/groups/{ns_group}

Delete a nameserver group. Cannot delete groups assigned to active domains.

**Endpoint:** `DELETE https://api.openprovider.eu/v1beta/dns/nameservers/groups/{ns_group}`

**curl Example:**

```bash
curl -X DELETE https://api.openprovider.eu/v1beta/dns/nameservers/groups/my-custom-ns \
  -H "Authorization: Bearer $TOKEN"
```

---

## Atlas Default

Atlas registers all domains with `ns_group: "dns-openprovider"`, which uses OpenProvider's managed DNS nameservers. This means DNS records are managed through the DNS zone API (`/dns/zones/`), not through custom nameservers.
