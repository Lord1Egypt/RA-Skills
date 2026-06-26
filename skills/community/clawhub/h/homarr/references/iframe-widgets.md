# Homarr iFrame widgets

Use this reference for Homarr iframe embeds, transparent mini-widgets, iframe headers, and `homarr-iframes`-style pages.

## Core iframe rule

Homarr's iFrame widget embeds a browser `<iframe>`.

```text
Homarr does not proxy iframe traffic. The iframe URL must be reachable from the user's browser/client.
```

A server-side curl from the Homarr host is not enough: check browser/client access too.

## Common iframe blockers

Check these when an iframe is blank, blocked, or redirects strangely:

- HTTPS Homarr embedding HTTP iframe -> mixed-content block;
- `X-Frame-Options: DENY` or `SAMEORIGIN`;
- CSP `frame-ancestors` excluding the Homarr domain;
- reverse proxy blocks framing;
- auth page cannot be framed;
- URL reachable from server but not from browser/client.

Header check:

```bash
curl -I '<iframe-url>' | grep -iE 'x-frame-options|content-security-policy|content-type|location'
```

Use `https://iframetest.com` for a quick frame permission check.

For owned services, allow framing via CSP `frame-ancestors` for the Homarr domain; configure app/reverse proxy as appropriate.

## Enable only needed iframe permissions

Homarr iframe options include fullscreen, scrolling, payment, autoplay, microphone, camera, geolocation, and modals. Enable only what the embedded page needs.

## Transparent iframe baseline

Official minimal idea:

```html
<html style="color-scheme: dark;">
<body style="background: none; display: flex; justify-content: center; align-items: center;">
  <img src="https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/homarr.svg" width="90" height="90" />
</body>
</html>
```

Production baseline:

```html
<!doctype html>
<html lang="en" style="color-scheme: dark;">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="dark" />
  <style>
    html,
    body {
      margin: 0;
      padding: 0;
      width: 100%;
      min-height: 100%;
      background: transparent !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
  </style>
</head>
<body>
  <!-- content -->
</body>
</html>
```

For full-card embeds:

```css
html,
body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
```

## Theme handling

If the iframe service supports theme query params, support/pass:

```text
?theme=dark
?theme=light
```

For dark Homarr boards, explicitly use `?theme=dark`. Do not rely on auto-detect for separately hosted iframe services.

Set browser color scheme:

```html
<meta name="color-scheme" content="dark">
```

This affects native controls and scrollbars.

## Decide who draws the card

### Pattern A: Homarr draws the card

Use for simple status/count/list mini-widgets inside a Homarr item. The iframe app draws only content; no inner card.

```css
html,
body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  min-height: 100vh !important;
  background: transparent !important;
  background-color: transparent !important;
  background-image: none !important;
  overflow: hidden !important;
}

.widget {
  width: 100% !important;
  min-height: 100vh !important;
  margin: 0 !important;
  padding: 14px !important;
  overflow: hidden !important;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
```

Avoid on the inner wrapper:

```css
background: #25262b;
background: rgba(...);
border: 1px solid ...;
border-radius: 10px;
box-shadow: ...;
backdrop-filter: blur(...);
linear-gradient(...);
```

Otherwise it becomes a card inside Homarr's card.

### Pattern B: iframe draws internal cards

Use for list-like iframe apps, such as `homarr-iframes` Linkwarden/Vikunja. Body remains transparent; each item is a local card.

```css
body {
  background: transparent !important;
  margin: 0;
  padding: 0;
}

.item-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 8.5px;
  min-height: 84px;
  border-radius: 10px;
  border: 1px solid rgba(56, 58, 64, 1);
  overflow: hidden;
}

.background-image {
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background-image: url(...);
  background-position: center;
  background-size: cover;
  filter: brightness(0.3);
}
```

```html
<div class="item-container">
  <div class="background-image"></div>
  <div class="content">...</div>
</div>
```

Text truncation:

```css
.text-wrap {
  flex-grow: 1;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 1px !important;
}
```

## homarr-iframes reference

Third-party reference: `https://github.com/diogovalentte/homarr-iframes`.

Check:

```text
src/routes/iFrame.go
src/sources/base_source.go
src/sources/linkwarden/linkwarden.go
src/sources/vikunja/vikunja.go
src/sources/cinemark/cinemark.go
src/sources/media/media.go
```

Common behavior:

- endpoints accept `theme=dark|light`;
- many endpoints default to `light`;
- wrong theme can show white backgrounds;
- data state often uses transparent body;
- empty fallback may use solid backgrounds: light `#ffffff`, dark `#25262b`;
- card backgrounds often use image + `filter: brightness(0.3)`.

Background args may need URL encoding:

```text
background_position=50%25%2049.5%25
background_size=105%25
background_filter=brightness(0.3)
background_filter=blur(5px)
```

Dark scrollbar pattern:

```css
::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-thumb { background-color: #484d64; border-radius: 2.3px; }
::-webkit-scrollbar-track { background-color: transparent; }
::-webkit-scrollbar-track:hover { background-color: rgba(37, 40, 53, 1); }
```

## Visual diagnostics

### White background

Check:

1. Missing `?theme=dark` on dark Homarr board.
2. Missing `body { background: transparent !important; }`.
3. Inner `.card`, `.container`, `.main` has `background: white/#fff`.
4. Empty-state fallback uses light theme.
5. Browser mixed content or blocked iframe fallback.

### Dark solid rectangle

Usually caused by global `background: #25262b` on `html`, `body`, or `.card`. This kills glass/blur transparency.

### Transparent edges but dark inner card

Inner wrapper has `background`, `linear-gradient`, or `backdrop-filter`. Remove if Homarr should draw the card.

### Inner border / card inside card

Inner wrapper has `border`, `border-radius`, or `box-shadow`. Remove if embedding inside Homarr's existing card.

### Light scrollbar or controls

Add/check `<meta name="color-scheme" content="dark">`.

## Useful checks

```bash
curl -I '<iframe-url>'
curl -s '<iframe-url>?theme=dark' | head
curl -s '<iframe-url>?theme=dark' \
  | grep -niE 'background|theme|card|body|html|border|backdrop|linear-gradient|box-shadow|color-scheme' \
  | head -120
```
