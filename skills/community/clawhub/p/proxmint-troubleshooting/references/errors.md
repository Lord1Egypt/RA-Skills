# Gateway responses

## HTTP and HTTPS (port 823 and sticky ports)

The reason is in the status line, for example `HTTP/1.1 503 NO_RAY`.

| Response | Meaning | Fix |
|---|---|---|
| `400 Bad Request` | The proxy couldn't read the request | Check the proxy URL: host, port, and `username:password` |
| `403 SITE_PERMANENTLY_BLOCKED` | The site is on the network's blocked list | See the blocked websites page; some sites can be opened for one product through **Request an unblock** in the dashboard |
| `403 PORT_BLOCKED` | The destination port is closed | Use one of 80, 443, 8080, 8443, 8888, 8090, 53, 853, 5060 or 5228 |
| `403 HOST_BLOCKED` | The user blocked this host themselves | Remove it from **Blocked hosts** on the product page |
| `407 NO_USER` | The login isn't recognised: wrong or missing username, or the product no longer exists | Copy the credentials again from the dashboard |
| `407 TRAFFIC_EXHAUSTED` | The product's bandwidth is used up | Add bandwidth to the product; the same credentials work again |
| `407 THREADS_EXHAUSTED` | Too many connections at once | Stay under 2,000 concurrent connections per product |
| `407 USER_BLOCKED` | The proxy user was blocked, usually after many retries with a wrong password | Contact Proxmint support; the remaining bandwidth is kept |
| `407 PORT_NOT_ALLOWED` | A sticky port this product can't use | Use the ports the dashboard's proxy generator lists |
| `500 INTERNAL_SERVER_ERROR` | A fault on the network's side | Retry; check `https://proxmint.com/status` if it continues |
| `502 NO_HOST_CONNECTION` | The exit IP couldn't reach the site: it's down or unreachable from that network | Retry; a new connection or session gets a new IP |
| `503 NO_RAY` | No exit could take the request | If every site fails, no IP matches the targeting: drop the city, ZIP or ASN, or fix the spelling. If only some sites fail on the same line, generate fresh lines or switch to rotating |

How clients print a refused tunnel:

- curl: `CONNECT tunnel failed, response 403`
- Python requests: `Tunnel connection failed: 403 SITE_PERMANENTLY_BLOCKED`
- Chrome: `ERR_TUNNEL_CONNECTION_FAILED`
- Any client without credentials: `407 Proxy Authentication Required`

## SOCKS5 (port 824)

SOCKS5 has no room for a reason text, so the same causes show up as:

| Symptom | Likely causes |
|---|---|
| Login refused | Wrong username or password, bandwidth used up, or too many connections |
| Reply code `0x02`, "connection not allowed by ruleset" | A blocked site or a closed destination port |
| Connection closed right after login | No IP matches the targeting, or the exit couldn't reach the site |

When a SOCKS5 error is unclear, repeat the request over HTTP on port 823 and read the status line.
