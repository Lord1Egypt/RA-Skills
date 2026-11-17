# Webpage integration for dynamic Open Graph images

Read this reference when adding or reviewing webpage metadata for an HCTI Open Graph configuration.

## Build the public image URL

The `create_og_config` response contains both `id` and `domain_id`. Use `domain_id` in public image URLs:

```text
https://hcti.io/v1/og/{domain_id}{source_page_pathname}
```

The pathname after `domain_id` is loaded from the configuration's `base_url`:

```text
base_url:    https://example.com
source page: https://example.com/products/widget
image URL:   https://hcti.io/v1/og/DOMAIN_ID/products/widget
```

Use the same pathname as the source page. Do not include the source origin again. Query strings do not produce separate images; use `hcti:content_version` when a page's render inputs need an explicit version change.

## Screenshot configuration example

For an `html_css` configuration with `extract_values: true`, place the standard preview metadata and HCTI rendering metadata in the initial HTML `<head>`:

```html
<head>
  <meta property="og:title" content="Product launch">
  <meta property="og:description" content="See what is new in this release.">
  <meta property="og:image" content="https://hcti.io/v1/og/DOMAIN_ID/articles/product-launch">
  <meta property="og:image:alt" content="Product launch announcement">

  <meta property="hcti:selector" content="#social-card">
  <meta property="hcti:viewport_width" content="1200">
  <meta property="hcti:viewport_height" content="630">
</head>
```

The matching page must contain the selected element:

```html
<section id="social-card">
  <!-- Content HCTI should capture -->
</section>
```

Use `property` for the examples below. HCTI also accepts `name` for `hcti:*` fields. Keep these tags inside `<head>` and render them into the server response; HCTI does not rely on client-side JavaScript to discover them.

## Template configuration example

For a `templated` configuration, publish template values using `html:tv:{template_key}`:

```html
<head>
  <meta property="og:title" content="Product launch">
  <meta property="og:description" content="See what is new in this release.">
  <meta property="og:image" content="https://hcti.io/v1/og/DOMAIN_ID/articles/product-launch">
  <meta property="og:image:alt" content="Product launch announcement">

  <meta property="html:tv:headline" content="Product launch">
  <meta property="html:tv:author.name" content="Ada Lovelace">
</head>
```

Dots in the template key create nested values, so `html:tv:author.name` supplies `author.name`. A content value is parsed as JSON when it is valid JSON; otherwise it remains a string.

A configuration mapping can reuse existing metadata instead of requiring an `html:tv:*` tag. Examples:

- Map `headline` with `fallback: titles` to use `<title>`, `og:title`, or `twitter:title` in that order.
- Map `summary` with `fallback: descriptions` to use `description`, `og:description`, or `twitter:description` in that order.
- Map `price` with `meta_key: product:price` and publish `<meta property="product:price" content="$19.00">`.

When both a mapping and `html:tv:*` provide the same template key, the direct `html:tv:*` value wins.

## Twitter Card metadata

Use the same HCTI endpoint for Twitter/X previews. Standard Twitter fields conventionally use `name`:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Product launch">
<meta name="twitter:description" content="See what is new in this release.">
<meta name="twitter:image" content="https://hcti.io/v1/og/DOMAIN_ID/articles/product-launch">
<meta name="twitter:image:alt" content="Product launch announcement">
```

The configuration's `optimization_mode` controls whether HCTI preserves one size, post-processes one render, or renders with crawler-specific viewports.

## Webpage `hcti:*` fields

Page-level values override matching defaults from an `html_css` configuration. Boolean values use `true` or `false`.

### Capture and content

| Field | Purpose |
| --- | --- |
| `hcti:selector` | Crop to the element matching a CSS selector; prefer a stable unique ID. |
| `hcti:css` | Inject page-specific CSS after the page loads. |
| `hcti:full_screen` | Capture the entire scrollable page instead of the initial viewport. |
| `hcti:transparent_background` | Render without a background; use a format that supports alpha. |
| `hcti:disable_twemoji` | Use native Linux emoji rather than HCTI's Twemoji fallback. |
| `hcti:content_version` | Integer version included in the content identity; increment it to force changed inputs at the same pathname. |

### Viewport and output scale

| Field | Purpose and constraints |
| --- | --- |
| `hcti:viewport_width` | Viewport width from 1 to 6000 pixels; set with `viewport_height`. |
| `hcti:viewport_height` | Viewport height from 1 to 6000 pixels; set with `viewport_width`. |
| `hcti:device_scale` | Pixel ratio from 0.1 to 3; higher values increase output dimensions, file size, and render time. |
| `hcti:viewport_mobile` | Enable mobile viewport behavior. |
| `hcti:viewport_landscape` | Enable landscape viewport orientation. |
| `hcti:viewport_touch` | Report touch capability to the page. |
| `hcti:jumbo_max_width` | Advanced jumbo width; must be supplied with `jumbo_max_height` and consumes additional renders. |
| `hcti:jumbo_max_height` | Advanced jumbo height; must be supplied with `jumbo_max_width` and consumes additional renders. |

For jumbo mode, both dimensions must be greater than zero and no more than 80,000, at least one must exceed 8,000, and their total area cannot exceed 400,000,000 pixels.

### Timing and lifecycle

| Field | Purpose and constraints |
| --- | --- |
| `hcti:ms_delay` | Extra delay before capture, from 0 to 10,000 milliseconds. |
| `hcti:max_wait_ms` | Limit for otherwise-irrelevant page loading activity, from 500 to 10,000 milliseconds and subject to the plan. |
| `hcti:render_when_ready` | Wait for the page's explicit HCTI readiness signal; use only when the page reliably sends it. |

### Browser context

| Field | Purpose and accepted values |
| --- | --- |
| `hcti:color_scheme` | Emulate `light` or `dark` color preference. |
| `hcti:timezone` | Use an IANA timezone such as `America/New_York` or `UTC`. |
| `hcti:media_type` | Render with `screen` or `print` CSS media rules. |
| `hcti:block_consent_banners` | Attempt to dismiss cookie or consent banners. |
| `hcti:identify_as_hcti` | Send `X-HCTI-SCREENSHOT: 1` on the top-level page request. |

## Standard social metadata

Keep ordinary preview metadata alongside the HCTI image URL. Common fields include:

- `og:title`, `og:type`, `og:description`, `og:url`, and `og:site_name`
- `og:image` and `og:image:alt`
- `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, and `twitter:image:alt`

Only publish `og:image:width`, `og:image:height`, and `og:image:type` when those values accurately describe every response from the configured endpoint. Crawler-specific optimization can make fixed dimensions misleading.

## Verification checklist

- Fetch the source page and confirm the tags appear in the initial `<head>`.
- Confirm the HCTI URL uses `domain_id`, not the management `id`.
- Confirm its pathname matches the source page pathname.
- Open the HCTI image URL directly and inspect the rendered result.
- If the result is stale, review the refresh interval, source cache headers or ETag, and `hcti:content_version`.
- Test the final public page in the relevant platform's link-preview debugger when available; platform caches are separate from HCTI's cache.

Authoritative guides:

- [Dynamic Open Graph image setup](https://docs.htmlcsstoimage.com/getting-started/og-images/)
- [Supported page metadata](https://docs.htmlcsstoimage.com/getting-started/og-images/supported-parameters/)
- [Caching and refresh behavior](https://docs.htmlcsstoimage.com/guides/debugging/og-image-caching/)
- [Platform and framework guides](https://docs.htmlcsstoimage.com/guides/og-images/)
