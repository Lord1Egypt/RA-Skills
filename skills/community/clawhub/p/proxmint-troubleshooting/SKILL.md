---
name: proxmint-troubleshooting
description: Diagnose failing Proxmint proxy connections. Use when a request through Proxmint returns 407, 403, 500, 502 or 503, a CONNECT tunnel fails, SOCKS5 refuses a connection, the exit IP is in the wrong country, a sticky session changes IP, a browser leaks its real IP through DNS or WebRTC, or a site loads directly but not through the proxy.
---

# Proxmint troubleshooting

Find the cause from evidence, then give the smallest fix. Explicit instructions from the user take priority over
this skill.

## Inputs to gather

Ask only for what is missing:

1. The exact error text or status line, such as `HTTP/1.1 503 NO_RAY` or `Tunnel connection failed: 407`.
2. The tool or library, and HTTP (port 823 or a sticky port) or SOCKS5 (port 824).
3. The username with the real login replaced by `LOGIN`, for example `LOGIN__cr.us;city.newyork`.
4. The target host and port.
5. Whether every site fails or only some.

Never ask for the password. If the user pastes one, don't repeat it.

When the plugin's account tools are connected, look before asking: `get_account` shows each product's status and
bandwidth left (a used-up product answers `407 TRAFFIC_EXHAUSTED`), and `check_connection` sends one test request
through a product, optionally from a chosen country.

## Workflow

1. **Read the gateway's reason.** The proxy puts it in the status line. Look it up in `references/errors.md`.
   Most clients print it inside their own error, for example curl's `CONNECT tunnel failed, response 403`.
2. **SOCKS5 gives no reason text.** Map the symptom with the SOCKS5 section of `references/errors.md`, or ask the
   user to repeat the request over HTTP on port 823, where the status line names the reason.
3. **No status at all** (timeout, connection refused, DNS failure for `gw.proxmint.com`): check the host and port,
   then a local firewall or a corporate network blocking outbound port 823 or 824, then
   `https://proxmint.com/status`.
4. **The destination port.** The network reaches only ports 80, 443, 8080, 8443, 8888, 8090, 53, 853, 5060 and
   5228. Any other port fails with `403 PORT_BLOCKED` (SOCKS5 reply `0x02`).
5. **Blocked sites.** Banks, payment providers, government websites (`.gov`, `.gov.uk`, `.mil` and the like) and a
   short named list fail with `403 SITE_PERMANENTLY_BLOCKED` on every plan. The site checker on
   `https://proxmint.com/docs/blocked-websites` shows whether a host is listed. Some sites can be opened for one
   product after review, through **Request an unblock** in the dashboard; approval isn't guaranteed. Don't
   suggest workarounds.
6. **The site itself refuses the traffic** (its own 403 page, a CAPTCHA, a block page) while the gateway shows no
   error: the site decides who it serves. Say so, and suggest the site's official API or the owner's permission.
   Don't offer ways to defeat bot protection, CAPTCHAs or rate limits.

## Common symptoms

- **Wrong country.** A location key in the username replaces the product's saved Targeting entirely. A username
  without one uses the saved Targeting. Geolocation databases also disagree about residential and mobile IPs:
  compare at least two before concluding the exit is wrong.
- **IP changes during a sticky session.** The IP went offline, or `sessttl` ran out (1 to 120 minutes). Catch the
  error and continue with a new `sessid`.
- **IP doesn't change on the rotating port.** The client is reusing one connection (`requests.Session`,
  `httpx.Client`, a browser). Each new connection gets a new IP.
- **Targeting is ignored.** The tool cut the username at a semicolon or a length limit. Check the field kept the
  whole username.
- **Works in curl, fails in a browser automation tool.** Chromium can't read credentials embedded in a proxy URL:
  pass the username and password as separate fields (Playwright) or with `page.authenticate` (Puppeteer).
- **HTTP/3 or other UDP traffic fails over SOCKS5.** SOCKS5 here carries TCP only.

## DNS and WebRTC leaks

- **DNS:** use `socks5h://` rather than `socks5://` so hostnames resolve through the proxy. Over HTTP, CONNECT
  already sends the hostname to the proxy.
- **WebRTC in browsers** can reveal the machine's own IP over UDP outside the proxy. In Chromium, launch with
  `--force-webrtc-ip-handling-policy=disable_non_proxied_udp`. In Firefox, set
  `media.peerconnection.ice.proxy_only` to `true`. Antidetect browsers have their own WebRTC setting per profile.
- Check the result on a WebRTC leak test page: the only public IP shown should be the proxy's.

## Output

1. The most likely cause, and how confident you are.
2. The fix as a concrete change: a username, port, code or setting.
3. How to confirm it worked.
4. If it's outside the user's control (a blocked site, an outage), say who can act on it: Proxmint support at
   `https://proxmint.com/support`, or the site's owner.

## Links

- Docs: [proxmint.com/docs](https://proxmint.com/docs)
- Pricing: [proxmint.com/pricing](https://proxmint.com/pricing)
- Status: [proxmint.com/status](https://proxmint.com/status)
