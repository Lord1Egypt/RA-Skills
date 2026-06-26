# Media, Code, Callout, and Custom Block Rendering

## :::image

    <figure data-component="image" class="report-image report-image--[layout]">
      <img src="[src]" alt="[alt]" loading="lazy">
      <figcaption>[caption]</figcaption>
    </figure>

layout=left: float left, max-width 40%, text wraps right.
layout=right: float right, max-width 40%, text wraps left.
layout=full (default): full width, centered.

## :::code

    <div data-component="code" class="code-wrapper">
      <div class="code-title">[title if provided]</div>
      <pre><code class="language-[lang]">[HTML-escaped code content]</code></pre>
    </div>

Add `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github.min.css">` and `<script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/highlight.min.js"></script>` + `<script>hljs.highlightAll();</script>` in head (or inline the full highlight.js CSS and JS if `--bundle` mode).

For dark-tech theme use `github-dark.min.css` instead of `github.min.css`.

## :::callout

    <div data-component="callout" class="callout callout--[type] fade-in-up">
      <span class="callout-icon">[icon or default]</span>
      <div class="callout-body">[content]</div>
    </div>

Default icons: note→ℹ, tip→💡, warning→⚠, danger→🚫

`icon` overrides must be normalized before rendering:

- Allowed whitelist: `ℹ`, `💡`, `⚠`, `🚫`, `✓`, `!`, `→`
- Strip U+FE0F if present.
- If the icon is still outside the whitelist after normalization, ignore it and fall back to the default icon for that callout type.

## Custom Blocks

For each `:::tag-name` matching a key in frontmatter `custom_blocks`:
1. Get the HTML template string from `custom_blocks.[tag-name]`
2. Parse block body as YAML to get field values
3. Replace `{{field}}` with the value
4. Replace `{{content}}` with any non-YAML plain text lines in the block
5. For `{{#each list}}...{{this}}...{{/each}}`, iterate the array and repeat the inner template
6. Wrap result in: `<div data-component="custom" data-tag="[tag-name]">[expanded HTML]</div>`
