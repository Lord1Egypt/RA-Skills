# Security — LYGO Site Card v1.0.0

## Trust boundary

Scripts in this folder:

- HTTPS GET of a URL **you pass**
- Optional read of a local HTML `--file`
- Optional `--write` JSON with `--i-consent`

They do **not** POST, spawn a shell, follow redirects off HTTPS/public IP, or write the live Star Chart.

## Controls

| Threat | Control |
|--------|---------|
| SSRF | HTTPS only, no userinfo, no loopback/RFC1918/link-local, redirects re-checked |
| Cookie leak | No cookie jar; default urllib Request |
| Huge pages | Body cap 400 KB |
| HTTP downgrade | `http://` refused |
| Auto-publish | Forbidden |

## Operator

1. `python scripts/self_check.py` (offline)
2. Pass only public URLs you are allowed to GET
3. Do not point at internal admin panels

**Δ9Φ963**
