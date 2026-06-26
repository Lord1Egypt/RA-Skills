---
name: product-tour-capture
version: 1.0.0
description: Capture product tour video segments using browser automation and screen
  recording. Coordinates timing between UI interactions and narration cues for demo
  and walkthrough videos.
metadata:
  openclaw:
    emoji: 🎥
    requires:
      bins:
      - ffmpeg
    network:
      outbound: true
      reason: Fetches pages via browser automation for screen capture.
---

# SKILL: Product Tour Capture
**Last used:** 2026-03-24
**Memory references:** 1
**Status:** Active
_Version: 1.0 · Author: Loki · Created: 2026-03-24_
_Proven on: Reddi Agent Protocol (14 steps, agent-protocol.reddi.tech/tour)_

## What this skill does

Captures a series of Playwright screenshots from a live web app, builds a full-screen clickable slideshow page (`/tour`), and deploys it. Gives any web app a polished "product tour" in one playbook run.

## Inputs

```typescript
interface TourPlaybookInput {
  appRepo: string          // local path to Next.js repo
  baseUrl: string          // deployed app URL (https://...)
  outputDir: string        // public/tour/ relative to repo
  tourPagePath: string     // app/tour/page.tsx relative to repo
  steps: TourStep[]
}

interface TourStep {
  id: string               // e.g. "01-landing" — used as filename
  url: string              // path on the app, e.g. "/"
  title: string            // sidebar label
  caption: string          // 1-sentence description shown in tour
  scroll?: number          // pixels to scroll after load
  clickTab?: string        // text of a tab to click (shadcn Tabs)
  click?: string           // text of element to click
  fill?: string            // text to fill into first textarea
  wait?: number            // ms to wait after fill/click
}
```

## Outputs

```typescript
interface TourPlaybookOutput {
  screenshotsCapured: number
  screenshotsFailed: string[]   // IDs of failed captures
  tourUrl: string               // live URL of the tour page
  deployedAt: string            // ISO timestamp
}
```

## Multi-agent playbook

### Agent roles

| Agent | Task | Input | Output |
|---|---|---|---|
| **Orchestrator (Loki)** | Receive request, construct step list, spawn agents | User brief | TourPlaybookInput |
| **Capture agent (Kit/Finn)** | Run Playwright, capture screenshots | TourPlaybookInput | screenshotManifest[] |
| **Builder agent (Kit)** | Generate /tour page from template + manifest, build, deploy | screenshotManifest[] + TourPlaybookInput | tourUrl |
| **QA agent (Oli)** | Spot-check screenshots (blank? matching captions?) | screenshotManifest[] | pass/warn/fail report |

### Handoff pattern

```
Loki constructs TourPlaybookInput
  → spawn Kit (capture)
      → node scripts/capture-tour.mjs
      → returns: { captured: 14, failed: [], manifest: [...] }
  → spawn Kit (build)
      → writes app/tour/page.tsx from TOUR_STEPS template
      → npm run build → vercel deploy
      → returns: { tourUrl, httpStatus: 200 }
  → spawn Oli (QA)
      → checks each screenshot isn't blank (file size > 5KB)
      → spot-checks 3 captions match visible page content
      → returns: pass / conditional-pass / fail
```

## Capture script template

Location: `scripts/capture-tour.mjs` in the target repo.

Key patterns:
- `page.goto(url, { waitUntil: 'networkidle', timeout: 20000 })`
- Tab clicks: `page.getByRole('tab', { name: tabName }).first()`
- Scroll: `page.evaluate(y => window.scrollTo(0, y), scrollY)`
- Fill + trigger: `textarea.fill(text)` → `button[generate].click()` → `waitForTimeout(ms)`
- Always `waitForTimeout(600)` after navigation before screenshot
- Viewport: `1280 x 800` (16:10, clean for sidebar layout)

## Tour page template

Full-screen layout (no scroll):
- Top bar: "Product Tour · X of N" + auto-play toggle + "Try it live →" CTA
- Main: screenshot panel (with prev/next chevrons) + right sidebar (step info + list)
- Progress bar: Solana purple → green gradient

Template component lives in `app/tour/page.tsx`. TOUR_STEPS is the only thing that changes per app.

## When to use this skill

- Any web app that needs a "product tour" page for demos, hackathons, or onboarding
- After a major UI rebuild (re-capture to keep tour current)
- For hackathon submissions — judges can self-tour without a live demo session

## Lessons learned (from Reddi Agent Protocol run)

1. **Tab clicks need `getByRole('tab')`** — generic `getByText` can hit non-tab elements
2. **Demo pipeline screenshots:** `fill + click + wait(7000)` for mid-pipeline, `wait(13000)` for complete
3. **23 files in public/tour/** after a re-run — old screenshots persist, that's fine (overwritten)
4. **Build command:** use `node node_modules/next/dist/bin/next build` not `npx next build` — the `.bin/next` shim has path issues on Node 24 in some environments
5. **Auto-play at 4s** is the right pace — slow enough to read captions, fast enough to feel dynamic
6. **14 steps is the sweet spot** — fewer feels thin, more feels exhausting for a tour

## Playbook architecture notes

This skill is a good test case for the playbook architecture because:
- Clear 3-agent handoff with defined I/O at each step
- Capture agent is stateless (just runs a script)
- Builder agent has a fixed template, only data changes
- QA agent has a simple pass/fail rubric (file size + caption spot-check)
- Total runtime: ~5-8 minutes end-to-end
- Fully parameterisable — works for any Next.js app with any step list

## Future extensions

- **v2:** Accept a Figma URL or sitemap and auto-generate the step list (Archie researches the app first)
- **v2:** QA agent uses vision model to verify screenshot content matches caption
- **v3:** Video export — stitch screenshots into a 60s walkthrough video (Finn)
- **v3:** Embed tour as a modal on the landing page (not just /tour route)
