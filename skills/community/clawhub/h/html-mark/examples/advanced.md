# Example — Advanced: generate a self-contained bookmarklet

For reviewing pages where you don't control the HTML — a staging URL, a competitor's landing page, a deployed product — you can't inject `<script>`. Use a bookmarklet instead: drag it to your bookmarks bar, click on any page → mark mode loads.

## Why "self-contained"?

The simple bookmarklet pattern fetches the script from an external URL:

```javascript
javascript:(function(){var s=document.createElement('script');s.src='https://example.com/html-mark.js';document.head.appendChild(s);})();
```

This works, but requires you to host `html-mark.js` somewhere (GitHub Pages / gist / Vercel / Cloudflare Pages). For a one-off review, that's friction. The base64 self-contained version embeds the entire runtime in the URL — no host needed.

## Prompt

```
Generate a self-contained html-mark bookmarklet I can drag to my browser
```

## What the skill does

It runs:

```bash
echo "javascript:$(python3 -c "
import urllib.parse
js = open('$HOME/.claude/skills/html-mark/html-mark.js').read()
print(urllib.parse.quote(js, safe=''))
")"
```

…then wraps the output in an IIFE guard so re-clicking the bookmarklet on the same page doesn't reload the runtime:

```javascript
javascript:(function(){if(window.__markModeLoaded)return;<URL-ENCODED-RUNTIME>})();
```

The result is a single very long string starting with `javascript:` — about 35 KB.

## Installing the bookmarklet

1. Copy the entire output (it's one line, no whitespace).
2. In your browser, **right-click bookmarks bar → Add page…**
3. Name it `📍 HTML Mark`, paste the `javascript:…` string into the URL field, save.
4. Visit any web page → click the bookmark → mark mode activates.

## Hosted variant (when self-contained is too long)

Some browsers truncate bookmarklets above ~64 KB. If you hit that limit, host the script and use the short variant:

1. Push `html-mark.js` to a GitHub repo
2. Use jsDelivr or raw.githubusercontent.com as the CDN

```javascript
javascript:(function(){if(window.__markModeLoaded)return;var s=document.createElement('script');s.src='https://cdn.jsdelivr.net/gh/YOUR_USER/YOUR_REPO@main/html-mark.js';document.head.appendChild(s);})();
```

Replace `YOUR_USER/YOUR_REPO` with your fork path. Pin to a tag (`@v1.0.0`) instead of `@main` if you want reproducible behavior.

## Limitations

- **CSP-strict sites** (e.g. GitHub, Google Docs) block inline scripts and external scripts via Content Security Policy. The bookmarklet won't run there. Use a browser extension or the page's own dev tools instead.
- **Iframes**: the script only injects into the top frame. To mark inside an iframe, open the iframe URL directly in a new tab.
- **State**: pins live in DOM only — they vanish on page reload. Copy annotations *before* refreshing.
