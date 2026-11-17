# Quickstart

```bash
python scripts/self_check.py
python scripts/lygo_tv.py plain
python scripts/lygo_tv.py embed      # the code that runs the player on a website, and what it then contacts
python scripts/lygo_tv.py urls
python scripts/lygo_tv.py map
python scripts/lygo_tv.py bookmark
```

Install pinned: `npx clawhub@0.23.3 install deepseekoracle/lygo-tv@1.3.1`

**Watch:** bookmark / open https://chatagent.ca/sources/

Channel tab is always open. Public FAST/world lists need a Terms tick for the session.

**Put it on a site** — paste this and keep the LYGO TV name:

```html
<link rel="stylesheet" href="https://chatagent.ca/assets/lygo-tv-ninja.css?v=8">
<div data-lygo-tv></div>
<script src="https://chatagent.ca/assets/lygo-tv-ninja.js?v=8" defer></script>
```

It opens on the Rumble room, walks ~12,000 channels with Prev/Next, and reads
`https://chatagent.ca/sources/catalog.json`. The visitor's browser also contacts cdn.jsdelivr.net if an HLS
channel is played (hls.js, SRI-pinned) and the platform the channel belongs to. For a whole branded page see
`embed/lygo-tv-embed.html`; for self-hosting, the contacted origins, a working CSP and the limits, see
`embed/README.md`.
