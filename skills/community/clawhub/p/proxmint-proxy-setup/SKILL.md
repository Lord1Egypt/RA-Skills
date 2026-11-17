---
name: proxmint-proxy-setup
description: Configure Proxmint proxies in code and tools. Use when the user wants to route curl, Python (requests, httpx, aiohttp, Scrapy), Node.js, Go, Playwright, Puppeteer or Selenium traffic through Proxmint, choose between HTTP and SOCKS5, keep proxy credentials out of source code, or confirm which IP their requests exit from.
homepage: https://proxmint.com
source: https://github.com/proxmint/mcp
metadata:
  openclaw:
    requires:
      env:
        - PROXMINT_USERNAME
        - PROXMINT_PASSWORD
    primaryEnv: PROXMINT_PASSWORD
---

# Proxmint proxy setup

Produce a minimal, working proxy configuration for the user's tool. Explicit instructions from the user take
priority over this skill. When they conflict, follow the user and mention the trade-off once.

## Connection facts

| Setting | Value |
|---|---|
| Host | `gw.proxmint.com` |
| HTTP and HTTPS sites | port `823`, proxy URL scheme `http://` |
| SOCKS5 | port `824`, scheme `socks5h://` where the client supports it, so DNS resolves through the proxy |
| Login | the product's username and password, shown on the product's page in the Proxmint dashboard |

- Each product has its own username and password. The login picks the pool; the host is the same for all of them.
- The proxy URL starts with `http://` even when the target site is `https://`. The client opens a CONNECT tunnel
  and TLS runs end to end inside it.
- On ports 823 and 824 every new connection gets a new IP. Requests that reuse an open connection can share its
  exit.
- A server with a fixed IP can connect without a login: the user adds that IP on the product's **Access** tab.
  With no username, the product's saved **Targeting** decides the exit location.
- SOCKS5 carries TCP only. QUIC (HTTP/3), WebRTC media and other UDP traffic don't pass through it.
- A product allows up to 2,000 concurrent connections.

## Inputs to gather

When the plugin's account tools are connected, take the product's host, ports and username from `get_account`
instead of asking. It never returns the password. Ask only for what is still missing:

1. The tool or language, and whether it is a script, a crawler, a test suite or a browser.
2. The exit location, if any. The `proxmint-targeting` skill builds the username for it.
3. Rotating (a new IP per connection) or sticky (one IP for a whole task).
4. HTTP or SOCKS5. Default to HTTP on port 823 unless the tool needs SOCKS5.

## Workflow

1. Read credentials from the environment variables `PROXMINT_USERNAME` and `PROXMINT_PASSWORD`.
   - Never ask the user to paste their password into the chat, and never write it into code, config files or
     examples.
   - If the user shares a password anyway, don't repeat it. Suggest keeping it in their environment or a secrets
     manager.
2. Build the username: the login, then any targeting after two underscores (see `proxmint-targeting`).
3. Write the configuration from the matching snippet in `references/clients.md`. Keep the user's existing HTTP
   client and code style; don't swap libraries unless asked.
4. Set a timeout (30 seconds is a sensible start) and retry network errors a bounded number of times. Don't retry
   `407` or `403` gateway responses: they have fixed causes, covered by `proxmint-troubleshooting`.
5. If the password contains `@`, `:` or `/`, URL-encode it wherever it sits inside a proxy URL.
6. End with a one-line check against an IP echo service such as `https://api.ipify.org`, and say what to expect:
   an IP address, which changes on each new connection when the login is rotating.

## Choosing a pool

The login decides the pool, so switching pools means using another product's login. Match the pool to the task,
and don't promise results on any particular website.

- **Datacenter**: fastest and steadiest. For sites that accept datacenter traffic, API testing and bulk jobs.
- **Residential**: IPs from home internet providers. For geo-specific content, localization testing and ad checks.
- **Premium Residential**: residential IPs for work that targets states, cities, ZIP codes or ISPs a lot. It
  counts that targeting once against the bandwidth balance; the other pools count it twice.
- **Mobile**: IPs from mobile carriers. For mobile-specific content and app testing.

## Guardrails

- Don't help bypass a website's access controls, CAPTCHAs, rate limits or terms of service. If a site refuses proxy
  traffic, say so plainly and suggest the site's official API or the site owner's permission.
- Banking, payment and government websites are blocked on the network. Don't suggest ways around that.
- Keep concurrency and request rates reasonable for the target site.

## Output

1. The configuration or code change, reading the login from the environment.
2. The username format used, written with `LOGIN` in place of the real login and no password.
3. How to verify the setup, and the expected output.
4. One line on what to do if the check fails, pointing to `proxmint-troubleshooting`.

## Links

- Docs: [proxmint.com/docs](https://proxmint.com/docs)
- Pricing: [proxmint.com/pricing](https://proxmint.com/pricing)
- Status: [proxmint.com/status](https://proxmint.com/status)
