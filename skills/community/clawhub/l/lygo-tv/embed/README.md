# LYGO TV — embed the player

Two ways in. The hosted one is three lines and stays current by itself; the vendored one is yours to review
and pin. Either way the player is **active web code**, not a passive widget — read *What the visitor's browser
contacts* below before you paste it anywhere you care about.

## 1. Hosted (recommended for ordinary sites)

```html
<link rel="stylesheet" href="https://chatagent.ca/assets/lygo-tv-ninja.css?v=8">
<div data-lygo-tv></div>
<script src="https://chatagent.ca/assets/lygo-tv-ninja.js?v=8" defer></script>
```

The player opens on **Excavationpro Rumble LIVE** (`rumble_live`), walks the pool with **Prev / Next** — about
**12,000 channels**, counter `title · 3 / 12156` — carries a **Sound** button (sound starts off: browsers block
unmuted autoplay with no gesture), and links back to the full player at https://chatagent.ca/sources/.

## 2. Vendored (self-hosted, for sites that must pin)

`lygo-tv-ninja.js` and `lygo-tv-ninja.css` in this folder are the player, byte-for-byte what the site serves:

```
lygo-tv-ninja.js    sha256-5t6Gc5TAM3WvRTF51cBuqA3PjiS65GJmhMvsoGsVdBQ=
lygo-tv-ninja.css   sha256-oqJabOyasBTBrwHmXHihIInv7XjlpAHc1NqpFhuhe0o=
```

Verify after copying — `sha256sum lygo-tv-ninja.js` on Linux/macOS, `Get-FileHash -Algorithm SHA256` on Windows.
Copy them beside your page and point the tags at your copies:

```html
<link rel="stylesheet" href="/assets/lygo-tv-ninja.css">
<div data-lygo-tv></div>
<script src="/assets/lygo-tv-ninja.js" defer></script>
```

The player still reads the catalog from chatagent.ca — self-hosting the code does not cut the feed, and a
vendored copy goes stale on its own. Pin the catalog too (see *Pinning the feed*) if the channel list has to
be something you reviewed.

## What the visitor's browser contacts

| Origin | When | Pinned? |
|--------|------|---------|
| `chatagent.ca` | always — player JS/CSS, and `sources/catalog.json` for the channel list | version query on the assets (`?v=8`); the catalog is mutable by design |
| `cdn.jsdelivr.net` | only when an HLS channel is played — hls.js 1.5.18 | **Subresource Integrity**: `sha384-R2JqybiEexSXz60H6Zz28MdsqWWnMQlP+NDb7nIhDHWxx6sM7Otw7OWCq9EBCPsz`. Every other channel type never loads it |
| `rumble.com`, `player.kick.com`, `player.twitch.tv`, `youtube-nocookie.com` | whichever platform the current channel is | that platform's own embed, that platform's terms |
| the HLS stream's host | only for a plain-stream channel | named by the catalog; https only, no credentials |

Nothing is proxied, nothing is decrypted, and no stream passes through our servers. The catalog is a public
read; the FAST/world lists inside the player UI wait for a per-session Terms tick, and the embed neither adds
nor bypasses a gate.

**Catalog entries are validated, not trusted.** Before anything is framed or played, each entry's URL must be
https, without credentials, and an embed must sit on its own platform's domain. A catalog entry cannot point
the frame or the video at an arbitrary origin. The check is `window.LYGO_TV_ALLOWED_URL(url, kind)` if you want
to run it yourself.

## Pinning what you can

If the page has a Content Security Policy, the embed works under one — list the origins rather than opening
everything:

```
Content-Security-Policy:
  script-src 'self' https://chatagent.ca https://cdn.jsdelivr.net;
  style-src  'self' https://chatagent.ca;
  frame-src  https://rumble.com https://player.kick.com https://player.twitch.tv https://www.youtube-nocookie.com;
  media-src  https:;
  connect-src https://chatagent.ca;
```

For a strict site, also: self-host the player (above), mirror `catalog.json` to your own origin and edit the
copy's `TV_PAGE`/catalog path, and set `frame-src` to only the platforms you allow. Disclose the embed to your
visitors — the sample page shows the wording to copy.

## A whole page, branded and ready

`lygo-tv-embed.html` is a complete, styled page with a visible disclosure section. Serve it as-is or paste from it.

## Theme it

The stylesheet inherits your variables, so the player matches your site without editing it:

| Variable | Use |
|----------|-----|
| `--bg` | player background |
| `--fg` | player text |
| `--line` | borders |
| `--gold` / `--accent` | kicker, buttons, links |
| `--muted` | meta line, hints |

## Honest limits

- **Autoplay:** sound is off until the visitor presses Sound. No page can override that; it is the browser's rule.
- **Geo-blocks and dead rooms:** some channels refuse some countries, and streams come and go. The player names a
  miss rather than faking a channel.
- **Third-party platforms:** Rumble, Kick, Twitch and YouTube rooms load as their own embeds, so their terms
  apply to their content.
- **No proxy, no decrypt, no XXX list.** Do not wrap this player in one. If a channel will not embed, link it.

## Licence and brand

MIT-0: use it, restyle it, ship it. Keep the LYGO TV name and the link to https://chatagent.ca/sources/ in
place — that link is the whole payment for the feed. Do not present it as your own player, and do not sell
access to it.
