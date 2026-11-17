# Security — lygo-tv v1.3.1

**This folder is a ClawHub pointer plus the player code to paste.** Isolation claims apply to the Python here:
installing this package fetches nothing and runs nothing. The *embed* is a different thing — browser code for
someone else's site — and its surface is listed below rather than folded into one "no network" claim.

| Surface | This package's scripts |
|---------|----------------|
| Network in scripts | **None** (no urllib/requests/http.client) |
| Subprocess / shell | **None** |
| Filesystem write | **None** |
| Stream proxy / CORS bypass | **No** |
| Pay-TV decrypt | **No** |
| Live Star Chart write | **No** |
| git / HF / ClawHub / social | **No** |

Printed URLs (player, catalog.json, terms, disclaimer, donate) are for **you** to open. If another skill fetches them, that skill must declare network.

## The embed (v1.3.0)

`embed/lygo-tv-ninja.js` + `embed/lygo-tv-ninja.css` are the player, and `embed/lygo-tv-embed.html` is a page
built on it. They are **code for the human's website**, not code this skill runs: the visitor's browser loads
the player and reads `https://chatagent.ca/sources/catalog.json`, which is served
`Access-Control-Allow-Origin: *` so any origin may read it. Embedding puts the channels on someone else's page
in their visitors' browsers — it does not proxy, decrypt, or store anything, and no stream passes through this
package or through the steward's servers. Loading a page is the human's decision on the human's site.

The live player is a static GitHub Pages page. Catalog class is **RESOURCE**. Dual ledgers remain **CANON**.

**Δ9Φ963 — point · do not proxy · do not invent channels.**


## The embed's surface (declared, not implied)

The embed runs in visitors' browsers on the embedding site. That is a wider boundary than the scripts, and the
ClawHub audit asked for it to be written down instead of hidden behind the scripts' isolation:

| Origin | When | Pinned |
|--------|------|--------|
| chatagent.ca | player JS/CSS + `sources/catalog.json` | assets carry `?v=`; the catalog is mutable by design |
| cdn.jsdelivr.net | hls.js 1.5.18, only for HLS channels | SRI `sha384-R2JqybiEexSXz60H6Zz28MdsqWWnMQlP+NDb7nIhDHWxx6sM7Otw7OWCq9EBCPsz` |
| rumble.com / player.kick.com / player.twitch.tv / youtube-nocookie.com | the channel's own platform | that platform's embed and terms |
| the stream's host | plain-stream channels only | https-only, no credentials, per the catalog |

Catalog entries are validated before use: https only, no credentials, and an embed must sit on its own
platform's domain (`urlAllowed` in the player, exposed as `window.LYGO_TV_ALLOWED_URL`). An entry cannot point
the frame or the video at an arbitrary origin. Nothing is proxied, decrypted, or stored, and no stream passes
through the steward's servers.

Install commands are pinned on both sides (`clawhub@0.23.3`, `lygo-tv@1.3.1`) so an install cannot silently
pick up newer code.
