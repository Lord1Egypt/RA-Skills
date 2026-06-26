---
name: Google Fonts
description: Load Google Fonts with proper performance, subsetting, and proven font pairings.
metadata: {"clawdbot":{"emoji":"🔤","requires":{},"os":["linux","darwin","win32"]}}
---

## Loading Mistakes

- Missing `display=swap` causes invisible text until font loads—always add it to URL
- Load only weights you use: `wght@400;600;700` not the entire family—each unused weight wastes ~20KB
- Missing preconnect slows load—add both: `<link rel="preconnect" href="https://fonts.googleapis.com">` and `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`

## Variable Fonts

- Inter, Roboto Flex, Montserrat, Open Sans have variable versions—one file for all weights
- Use `wght@100..900` syntax for variable—downloads single file instead of multiple
- CSS for variable: `font-weight: 450` works with any value in range
- Check "Variable" badge on font page—not all Google Fonts are variable

## Subsetting

- Default includes latin—only add `&subset=latin-ext` if you need Polish, Vietnamese, etc.
- CJK fonts (Noto Sans JP, etc.) are huge—Google serves them sliced, but still heavy
- Unused subsets = wasted bytes—check what characters you actually need

## Proven Pairings

**Serif + Sans-Serif (classic contrast):**
- Playfair Display (heading) + Source Sans Pro (body)
- Lora (heading) + Roboto (body)
- Libre Baskerville (heading) + Montserrat (body)
- Merriweather (heading) + Open Sans (body)

**Sans-Serif only (modern/clean):**
- Inter (both)—vary weight for hierarchy
- Montserrat (heading) + Hind (body)
- Poppins (heading) + Nunito (body)
- Work Sans (heading) + Open Sans (body)

**Tech/Startup:**
- Space Grotesk (heading) + Space Mono (code)
- DM Sans (heading) + DM Mono (code)
- IBM Plex Sans + IBM Plex Mono

**Display fonts (headings only):**
- Abril Fatface, Bebas Neue, Oswald—never use these for body text

## Font Selection by Purpose

- **Long-form reading:** Merriweather, Lora, Source Serif Pro, Crimson Text
- **UI/Interfaces:** Inter, Roboto, Open Sans, Nunito Sans (tall x-height, clear at small sizes)
- **Impact headings:** Playfair Display, Oswald, Bebas Neue (not for body)
- **Monospace:** JetBrains Mono, Fira Code, Source Code Pro

## Common Mistakes

- Loading 6+ weights "to be safe"—pick exactly the weights you use (usually 2-3)
- Using display fonts for paragraphs—Lobster, Pacifico, Abril Fatface are heading-only
- Two fonts too similar—Roboto + Open Sans look almost identical; just use one
- Missing font-weight in CSS—`font-weight: 600` won't work if you only loaded 400 and 700
- No fallback stack—always: `font-family: 'Inter', system-ui, sans-serif`

## Self-Hosting

- Self-host for GDPR compliance—Google Fonts loads from Google servers, logs IP addresses
- Use google-webfonts-helper to download files
- Same `font-display: swap` needed in your @font-face
- Self-hosted can be faster if your CDN is closer than Google's
