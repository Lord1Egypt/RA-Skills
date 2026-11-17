# custom-html recipes — schema-safe freeform craft

Use **one** intentional `custom-html` beat when no layout covers the art — split posters, stamp stacks, typographic explosions. Prefer schema layouts (`ranked-list`, `streak-grid`, `metric-ring`, `chart`, `feature-grid` bento, `comparison`+`emphasis`) first. Never invent `custom-html` stickers for theme atmosphere (loud frames / neon chrome / paper grain belong to the theme).

**Rules**
- Theme tokens only: `var(--accent)`, `var(--bg)`, `var(--text)`, `var(--muted)`, `var(--border)`, `var(--heading-font)`, `var(--body-font)`, `var(--mono-font)`.
- Scripts / event handlers / `javascript:` URLs are stripped on render.
- PPTX approximates panels/text — ship HTML when the art is the point.
- Cap density: one hero composition per slide; keep type ≥18px equivalent.

## Split panels

```html
<div style="display:flex;gap:16px;align-items:stretch;height:100%;min-height:280px">
  <div style="flex:1;background:var(--accent);border-radius:16px;padding:28px;color:var(--bg);display:flex;flex-direction:column;justify-content:flex-end">
    <div style="font:800 64px/0.9 var(--heading-font);letter-spacing:-0.04em">01</div>
    <p style="margin-top:14px;font:500 15px/1.35 var(--body-font);opacity:.88">Accent panel — the number owns the beat.</p>
  </div>
  <div style="flex:1.35;border:2px solid var(--border);border-radius:16px;padding:28px;display:flex;flex-direction:column;justify-content:center;background:color-mix(in srgb,var(--bg) 92%,var(--accent))">
    <p style="font:700 32px/1.12 var(--heading-font);color:var(--text);letter-spacing:-0.03em;margin:0">Schema-safe HTML with frontend-slides energy.</p>
    <p style="margin:14px 0 0;font:400 15px/1.45 var(--body-font);color:var(--muted)">Keep Deck JSON · Studio · theme tokens. Art escapes without abandoning the product.</p>
  </div>
</div>
```

## Big number + hairline rule

```html
<div style="height:100%;min-height:280px;display:flex;flex-direction:column;justify-content:flex-end;padding:8px 4px 4px">
  <div style="font:800 clamp(72px,14vw,120px)/0.85 var(--heading-font);letter-spacing:-0.05em;color:var(--accent)">3.2×</div>
  <div style="height:3px;width:72px;background:var(--text);margin:18px 0 16px;border-radius:2px"></div>
  <p style="margin:0;max-width:28ch;font:600 22px/1.25 var(--heading-font);color:var(--text);letter-spacing:-0.02em">Faster close rate after the craft rewrite.</p>
  <p style="margin:10px 0 0;font:400 14px/1.45 var(--body-font);color:var(--muted)">One metric. One rule. No card chrome.</p>
</div>
```

## Poster stamp stack

```html
<div style="position:relative;height:100%;min-height:280px;padding:12px">
  <div style="position:absolute;inset:18px 24px auto auto;transform:rotate(8deg);padding:10px 14px;border:3px solid var(--accent);color:var(--accent);font:700 13px/1 var(--mono-font);letter-spacing:.14em;text-transform:uppercase;background:var(--bg)">SHIPPED</div>
  <div style="position:absolute;inset:auto auto 28px 20px;transform:rotate(-6deg);padding:10px 14px;border:3px solid var(--text);color:var(--text);font:700 13px/1 var(--mono-font);letter-spacing:.14em;text-transform:uppercase;background:var(--bg)">PROOF</div>
  <div style="height:100%;display:flex;flex-direction:column;justify-content:center;max-width:22ch">
    <p style="margin:0;font:800 40px/1.05 var(--heading-font);letter-spacing:-0.04em;color:var(--text)">Stamp the claim. Repeat the motif.</p>
    <p style="margin:16px 0 0;font:400 15px/1.45 var(--body-font);color:var(--muted)">Two rotated labels beat a sticker pile — one motif, loud once.</p>
  </div>
</div>
```

## Typographic explosion (wrap / launch)

```html
<div style="height:100%;min-height:280px;display:grid;grid-template-rows:auto 1fr auto;gap:18px">
  <p style="margin:0;font:600 12px/1 var(--mono-font);letter-spacing:.16em;text-transform:uppercase;color:var(--accent)">Year wrap</p>
  <p style="margin:0;font:800 clamp(36px,6vw,56px)/0.95 var(--heading-font);letter-spacing:-0.045em;color:var(--text)">We didn't ship slides.<br><span style="color:var(--accent)">We shipped a system.</span></p>
  <div style="display:flex;gap:10px;flex-wrap:wrap">
    <span style="padding:8px 12px;border-radius:999px;background:var(--accent);color:var(--bg);font:700 12px/1 var(--mono-font)">75 themes</span>
    <span style="padding:8px 12px;border-radius:999px;border:2px solid var(--border);color:var(--text);font:700 12px/1 var(--mono-font)">PPTX native</span>
    <span style="padding:8px 12px;border-radius:999px;border:2px solid var(--border);color:var(--text);font:700 12px/1 var(--mono-font)">MCP craft gates</span>
  </div>
</div>
```

## When NOT to use custom-html

| Impulse | Use instead |
|--------|-------------|
| Ranking bars | `ranked-list` |
| Day streaks | `streak-grid` |
| Circular KPI | `metric-ring` |
| Theme stickers / frames | Theme surface chrome (export already approximates) |
| Soft 3-up cards | `feature-grid` (+ `columns:"bento"` for 5) |
