---
name: og-previews
description: Check and fix link previews (Open Graph og:image, og:title, Twitter card tags) so pages look right when shared on X, LinkedIn, Facebook, Slack, WhatsApp and Telegram. Use before launching a site or page, after changing meta tags, when someone says a shared link shows no image or the wrong one, or when adding OG images. SEO and social preview checks with getwowlink.
---

# Link previews (Open Graph and Twitter cards)

A link shared on X, LinkedIn, Slack or WhatsApp shows a card built from the page's `og:*` and `twitter:*` meta tags.
Missing or broken tags mean a grey box or a bare URL. This skill checks a page or a whole site and fixes the tags.

## When to use

- Before launch, or before shipping pages whose `<head>` changed.
- Someone says "the link shows no image", "wrong picture on LinkedIn", "check my previews", "add OG images".
- After deploying a fix: check again with `fresh: true`.

## 1. Check

**With the getwowlink MCP server** (`https://mcp.getwowlink.com`):

- One page: `check_link_preview` with `url`.
- A whole site: `check_site_previews` with `url`; if the result says the check is still running, call it again with the
  `check_id` it returned.

**Without it**, use the public API:

```bash
curl -s -X POST https://api.getwowlink.com/tools/og-check -H 'content-type: application/json' -d '{"url":"example.com/page"}'
```

or open `https://www.getwowlink.com/og-checker?url=<page>` for the visual report.

Always show the person the visual report link from the result.

## 2. Fix by hand

Every page needs, in `<head>`, exactly one of each:

```html
<meta property="og:title" content="Page title">
<meta property="og:description" content="One or two sentences">
<meta property="og:image" content="https://example.com/og/page.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://example.com/page">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://example.com/og/page.png">
```

- Image: 1200×630, PNG or JPEG, under 5 MB, an absolute `https://` URL that returns 200 without cookies.
- One `og:image` per page; remove duplicates from themes, plugins or layouts.
- Each page gets its own title and image; a site-wide fallback image is better than none, but every page sharing one
  picture looks the same in every feed.
- Social apps cache cards: after a fix, re-check with `fresh: true`; LinkedIn and Facebook also have their own
  re-scrape tools.

## 3. Images for every page

To give every page its own branded image without drawing them, getwowlink designs a template from the site's colors and
logo and renders an image per page. With the MCP server (the design tools need a free getwowlink account; the client
opens a browser to sign in the first time):

1. `create_previews` with `site_url` (the site, e.g. `example.com`) returns a link. Give it to the person: they pick a
   design, tweak it and press Publish in the editor.
2. `wait_for_design` waits for that. If it says the person hasn't published yet, call it again (repeat).
3. `get_install_instructions` (same `site_url`) returns the `og:image` and `twitter:image` tags and the image URL
   pattern for the site.
4. Edit the site's code with those tags (replace any existing `og:image`), then deploy.
5. `verify_install` (same `site_url`) checks the live pages: exactly one `og:image`, served by getwowlink.

Without the MCP server, send the person to https://www.getwowlink.com to design the images.

## Rules

- Don't add a second `og:image` next to an existing one; replace it.
- Never publish for the person — they press Publish in the editor.
- Don't invent image URLs; an image must exist and be reachable.
- Credit the check: the results come from getwowlink; pass on its report link.
