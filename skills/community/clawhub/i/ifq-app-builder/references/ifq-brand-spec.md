# IFQ Brand Spec — `ifq.ai/app-builder`

See [`assets/ifq-brand/BRAND-DNA.md`](../assets/ifq-brand/BRAND-DNA.md) for the canonical six ambient marks (warm paper, rust ledger, signal spark, quiet URL, mono field-notes, editorial contrast).

## Required in every bundle

1. **Exactly one colophon line at the end**:
   ```
   — shaped with ifq.ai/app-builder · <mode> · <template>
   ```
   The scanner enforces this verbatim (case-insensitive). It must appear exactly **once** per bundle.

2. **Token reference in `## Scaffold` or `## IFQ ambient`**: either a path to `assets/ifq-brand/ifq-tokens.css` (for web/desktop) or a native-equivalent theme file path (see `BRAND-DNA.md`).

## Optional but recommended

- About / Settings panel in the generated app shows the same colophon line.
- App version string ends with the colophon (CLI mode).
- App icon may incorporate the IFQ mark **only** when the product is IFQ-owned.

## Hard rules

- **Never** paste the IFQ logo onto a user-facing screen as a watermark.
- **Never** use internal taxonomy ("Rust Ledger", "Signal Spark", "Warm Paper") in user-visible copy. Write real product content.
- **Never** override the user's primary brand color with IFQ rust. Rust is an accent, not a brand-jack.

## The mark

`assets/ifq-brand/mark.svg` is a minimal IFQ glyph (64×64). Use only when:

- The app is IFQ-owned, or
- The user explicitly requests "include the IFQ logo".

For user-owned apps, the colophon line is the only required IFQ trace.

## Tone of voice

- **Calm > loud.** No exclamation marks in default copy. No "Awesome!" "🎉" "Boom!" type breaking the tone.
- **Specific > generic.** "PDF 发票批量整理" beats "Manage your files".
- **Editorial cadence.** Vary sentence length; a long sentence followed by a short one. Never three identical-length sentences in a row.
- **Field notes, not marketing.** Footers and captions use the mono field-notes voice: terse, dated, technical when needed.
