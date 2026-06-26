# Abuseipdb

AbuseIPDB MCP — wraps AbuseIPDB v2 API (api.abuseipdb.com/api/v2)

## check_ip

Check an IP address against the AbuseIPDB database. Returns abuse confidence score (0-100), ISP, usa

## report_ip

Report an abusive IP address to AbuseIPDB. Requires category IDs (e.g., "18,22" for DDoS + SSH brute

## get_blacklist

Get the AbuseIPDB blacklist of the most-reported IP addresses. Returns IPs with their abuse confiden

```json
{
  "mcpServers": {
    "abuseipdb": {
      "url": "https://gateway.pipeworx.io/abuseipdb/mcp"
    }
  }
}
```
