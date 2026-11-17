## VirtualPerson Integration

For platforms that remain blocked after VPN (Tock, Yelp, OpenTable), VirtualPerson provides a real Chrome browser on a virtual display, routed through VPN. See `references/virtualperson-integration.md` for full setup.

**Patched files** are in `references/virtualperson-patches/`:
- `docker-compose.yml`, `launch-chrome.sh`, `entrypoint.sh` — VPN Gate variants
- `vpn-socks5-bridge.sh` — SOCKS5 proxy on host routing through tun0
- `DEPLOY.md` — Full deployment guide

**Quick connect from ocas-spot:**
```python
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
```