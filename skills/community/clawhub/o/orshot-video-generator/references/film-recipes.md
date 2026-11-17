# Film recipes

One recipe per kind of video people make. Each is a beat sheet with timings that passed review, the cut family, the motion per scene and the fields that change per render. Times count from each scene's start. Field names and allowed values are in `orshot_get_design_spec` topic `film`, `orshot_get_design_spec` topic `template-json` and https://orshot.com/docs/orshot-studio/motion.md; this file only says what to build.

Every recipe follows the pacing rule in the skill: text is read at about 0.4 s per word from when each block starts entering, blocks in entrance order, then the scene holds about 1 s; the last arrival holds 2 s or more, and cuts take 0.9 to 1.2 s. If a scene feels slow, cut words. Never shorten the motion.

## 1. Chart or stat explainer

A video post format, returned by `orshot_plan_design` with the job and `duration_seconds` (stat, milestone or chart: number, chart, count). For a table of results, use the lineup timing there: rows land 0.1 s apart, then a long hold.

## 2. Tips or listicle reel

"3 tips for ...", "5 habits that ...". 9:16, 15 to 25 s.

| Scene | Length | What happens |
|---|---|---|
| Hook | 4 to 4.5 s | Full-bleed photo or clip of the subject with a slow Ken Burns, a dark gradient at the bottom, the claim on screen by 0.3 s. A kicker ("Perfume tips") above it. |
| One per tip | 4.5 to 5 s each | Tip number large, the tip in 6 words or fewer, one picture that shows it, and a supporting line or a small stat in the lower third ("Lasts 6 to 8 hours on skin"). The number counts or slides in; the line follows 0.3 s later, the support line 0.4 s after that. |
| Payoff or list | 5 to 7 s | All tips as a list in type large enough to read on a phone, rows landing 0.4 s apart, so the viewer can screenshot it. A small teaser card of the product sits in a corner. |
| End card | 3.5 to 4 s | Product or logo, one line, the CTA. |

- Cuts: `push` or `slide` left between tips (same grid, so never `fade`); one `grow` from the teaser card into the end card.
- Per render: `pageN@line`, `pageN@support` and `pageN@photo` per tip, the hook, the CTA.

## 3. Real estate listing reel

A video post format, returned by `orshot_plan_design` with the job and `duration_seconds` (real estate: status word, rooms, proof numbers, contact).

## 4. Launch teaser

A new app, feature or product launch. 9:16 or 16:9, 18 to 30 s.

| Scene | Length | What happens |
|---|---|---|
| Problem | 3 to 3.5 s | The pain in one line, acted out: a messy inbox, a spreadsheet, a red number. |
| The product | 4 s | App screen pull-back: the screen starts filling the frame and settles into a device or card over about 1.2 s; its UI lands 0.3 s later. |
| One per feature, 2 to 3 | 4 s each | A real screenshot or recording, one line of 6 words or fewer, one action on it (a fingertip tap with a press, a toggle, a counter). |
| End card | 3 s | Logo, the promise, the URL. The logo is a `match` from the last scene so it travels into place. |

- Cuts: `whip` for energy between features, `match` or `grow` into the end card.
- Screenshots, recordings and the logo come from the user. No screenshot yet? `orshot_render_library_template` with `templateId: "website-screenshot"` captures a page.
- Per render: lines and screens per feature, so the same template serves the next launch.

## 5. Product promo reel

A product intro, a flash sale or a seasonal offer. 9:16 or 4:5, 12 to 20 s.

| Scene | Length | What happens |
|---|---|---|
| Hook | 3 s | The product in use or the result, full frame, the claim by 0.6 s. |
| Benefits, 2 | 3.5 to 4 s each | Product photo with a cut-out or a clean background, one benefit each, a badge or pill popping in. |
| Offer | 4 s | The old price struck through, the new price swapping in, the end date. A stamp slams in (scale 1.7 to 1 with a blur that clears). |
| End card | 2.5 s | The shop name and the CTA, grown out of the stamp. |

- Cuts: `push` between scenes, then one `grow` from the stamp into the end card.
- Prices, dates and claims come from the user. Never invent a discount.
- Per render: product photo, name, price, old price, end date, CTA.

## 6. Brand line-art film

A new logo, an icon set or a brand board, animated. 1:1 or 4:5, 15 to 20 s. Everything is drawn SVG.

| Scene | Length | What happens |
|---|---|---|
| The mark | 4 to 4.5 s | The mark builds itself: strokes draw in (`drawIn`, 0.35 to 0.5 s per part), fills follow, then the mark scales down from large and moves aside while the wordmark reveals by character. |
| The idea | 7 s | One drawn scene that acts out the brand promise (a bowling ball rolls down a lane and the pins fall, an icon set draws itself one icon every 0.45 s at 1.1 s each). The headline reveals by word before the action, the answer line after it. |
| Applications | 6 to 9 s | Business cards, a menu or colored tiles land 0.45 s apart as groups, each with its own mark; contact lines rise in 0.15 to 0.25 s apart. |

- Cuts: `push` up and then left, 1 s, power3 in-out. Use `fade` only between scenes with different grounds.
- Keep one stroke width across the whole film.
- Loops (a blink, a bell ring) are one cycle plus `repeat: -1`, ending where they started.
- Preview every drawing with `orshot_preview_element` before it goes into a scene.

## 7. Occasion reel

Teacher's day, Eid, a team anniversary, a thank-you to customers. 9:16 or 1:1, 15 to 25 s.

| Scene | Length | What happens |
|---|---|---|
| Opening | 3.5 s | The occasion in the viewer's language, large, over a warm photo or a drawn motif that draws in. |
| Message, 2 to 3 lines | 4 to 5 s each | One sentence per scene, revealing by word; a small drawn motif (a pencil, a lantern, a heart) animates beside it. |
| Sign-off | 3 s | The organisation's name and logo, the date. |

- Cuts: `dip` (a breath) or `fade` between message scenes. This is the one recipe where a slow pace is right.
- Right-to-left languages: right-aligned text, reveal by word, a font that covers the script.
- Per render: the names, the message lines and the date, so the same film serves next year.

## 8. Testimonial or review film

A video post format, returned by `orshot_plan_design` with the job and `duration_seconds` (customer quote: the result, the words, the person).

## 9. Character dialogue

Two drawn characters talking ("the yogurt and the spoon"), for TikTok. 9:16, 15 to 30 s.

- One scene per line of dialogue, 3 to 5 s each by its word count. The speaker bounces or tilts once as its speech bubble pops; the listener blinks on a loop.
- Each character is one SVG with ids on eyes, mouth and arms. A blink is a short scale-y cycle with `repeat: -1` and a `repeatDelay` of 2 to 3 s; a mouth swaps between two shapes while its line reveals.
- Cuts: hard cuts with a `flash` overlay on the punchline, `push` otherwise.
- Per render: the lines of dialogue.
