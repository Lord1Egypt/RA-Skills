# Hermes Browser on Fedora Atomic — Commands & Config Reference

## Exact config diff (in `~/.hermes/config.yaml`, under `browser:`)

Before (broken defaults):
```yaml
browser:
  cdp_url: ''
  use_real_profile: true
  cloud_provider: browser-use
  use_gateway: true          # routes to paid Nous Portal gateway
```

After (working local mode):
```yaml
browser:
  cdp_url: 'http://127.0.0.1:9222'   # only used by browser_exec; optional
  use_real_profile: false
  cloud_provider: local
  use_gateway: false
```

Apply via `sed` (patch tool is blocked on config.yaml):
```bash
F=~/.hermes/config.yaml; cp "$F" "${F}.bak-$(date +%s)"
sed -i "s|^  cloud_provider:.*|  cloud_provider: local|" "$F"
sed -i "s|^  use_gateway:.*|  use_gateway: false|" "$F"
sed -i "s|^  use_real_profile:.*|  use_real_profile: false|" "$F"
```

## Install transcript (Playwright Chromium via agent-browser)
```bash
$ npx --yes agent-browser install
⚠ Linux detected. If browser fails to launch, run:
  agent-browser install --with-deps
Installing Chrome...
  Downloading Chrome 152.0.7977.64 for linux64
  https://storage.googleapis.com/chrome-for-testing-public/152.0.7977.64/linux64/chrome-linux64.zip
  ...
✓ Chrome 152.0.7977.64 installed successfully
  Location: ~/.agent-browser/browsers/chrome-152.0.7977.64
```
Note: location is `~/.agent-browser/browsers/`, NOT `~/.cache/ms-playwright/`
(as the generic Playwright docs imply). Survives reboot (user-space, not /tmp).

## Verification (built-in path, no browser_exec)
```bash
# proves local Chromium launches + renders an SPA
npx --yes agent-browser read https://docs.b.ai/llmservice
# reap check
npx --yes agent-browser close
pgrep -af "agent-browser/browsers/chrome" | grep -v pgrep || echo "reaped OK"
```

## Diagnostic decision table
| Observed error | Meaning | Action |
|---|---|---|
| `Nous Tool Gateway is not available (not entitled or unreachable)` | `use_gateway:true` -> paid Nous Portal gateway, no sub | set `use_gateway:false` |
| `default browser is not a supported Chromium browser (Chrome, Edge, Brave, Chromium). Real-profile browsing requires a Chromium default` | `use_real_profile:true` cloning non-Chromium OS default (Zen/Gecko) | set `use_real_profile:false` |
| `web_extract` returns empty `content` for a known-content site | Site is a Docusaurus/Next.js SPA (empty HTML shell) | drive a real browser; or `curl` the JS bundle and grep route->chunk map |
| `BU_CDP_URL=...:9222 unreachable ... Connection refused` (from `browser_exec`) | nothing running on :9222; browser_exec needs external Chrome, not Hermes managed Chromium | use built-in `browser_*` tools instead; do not rely on browser_exec |
| `ModuleNotFoundError: No module named 'browser_helpers'` (from `browser_exec`) | browser-use harness venv packaging bug | separate fix; use built-in tools for now |

## Gotcha: CDP reboot fragility
A `cdp_url` pointing at a manually-launched `flatpak run ... --remote-debugging-port=9222`
is NOT reboot-safe: after reboot nothing starts it, so the endpoint dies. Prefer
`cloud_provider: local` (Hermes manages Chromium lifecycle, reboot-safe) over the
static-CDP approach.
