# LYGO TV

Free online TV player — and the player itself, to run on your own page.

**Watch:** https://chatagent.ca/sources/

**Embed:** three lines, any site:

```html
<link rel="stylesheet" href="https://chatagent.ca/assets/lygo-tv-ninja.css?v=8">
<div data-lygo-tv></div>
<script src="https://chatagent.ca/assets/lygo-tv-ninja.js?v=8" defer></script>
```

```bash
npx clawhub@0.23.3 install deepseekoracle/lygo-tv@1.3.1
python scripts/self_check.py
python scripts/lygo_tv.py plain
python scripts/lygo_tv.py embed
```

The player opens on the steward's Rumble room, walks about twelve thousand channels with Prev/Next, and takes
its channel list from https://chatagent.ca/sources/catalog.json in the visitor's browser. Embedding is active
web code, not a passive widget: it contacts chatagent.ca, cdn.jsdelivr.net (hls.js, only for HLS channels, and
SRI-pinned) and whichever platform the current channel belongs to. Read `embed/README.md` before pasting it
anywhere, and see the audit: https://clawhub.ai/deepseekoracle/skills/lygo-tv/security-audit

A whole branded page, disclosure included, is in `embed/lygo-tv-embed.html`; self-hosted copies of the player
are in `embed/`.

Channel tab = Excavationpro rooms. Public lists after Terms. The scripts in this folder do not fetch streams.

Official emblem: overlapping gold rings + cyan meridian (`emblem.svg`).

MIT-0 · keep the LYGO TV name and the link back.
Donate: [PayPal.me/ExcavationPro](https://www.paypal.com/paypalme/ExcavationPro)
