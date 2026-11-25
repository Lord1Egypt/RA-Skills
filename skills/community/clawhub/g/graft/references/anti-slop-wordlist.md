# Anti-Slop Wordlist

## Purpose

This is a mechanical enforcement list, not a style guide. After generating any output (change plans, reports, reasoning), run a literal grep against the file for each term below. A hit that is used as a **genuine positive descriptor** is a failure — rewrite that passage with something specific (cite a px value, hex color, ratio, or concrete trade-off), re-check, and repeat until the grep returns 0 hits against genuine descriptors.

## Exemption

A hit **inside a quoted foil** is fine. Example:

> "Could have gone for a generic *modern* look, but instead chose 2px radii consistently across all 47 interactive elements to signal engineering precision."

Here "modern" is the rejected alternative, not a descriptor of the analyzed site. This is acceptable.

## Banned Terms

When used as positive descriptors of the design being applied, these terms are banned:

```
clean
modern
sleek
visually appealing
user-friendly
intuitive
seamless
elegant
minimalist
polished
refined
sophisticated
premium feel
```

## Grep Command

Run this after every output file is written. Adjust the filename as needed:

```bash
grep -inE "clean|modern|sleek|visually appealing|user-friendly|intuitive|seamless|elegant|minimalist|polished|refined|sophisticated|premium feel" {output-file}
```

If any line matches:
1. Read the matching line in context
2. If the term is a **genuine descriptor** (not inside a quoted foil/rejected alternative), rewrite it
3. Replace the vague term with a **specific measurement or trade-off** — e.g. replace "now it looks more modern" with "now the border-radius signals precision, matching {source}'s restraint principle (2px across 47 elements)"
4. Re-run the grep
5. Repeat until 0 genuine-descriptor hits

## Why This Exists

"Now it looks more modern" is the graft equivalent of slop. Every change-plan reasoning and every report line must cite the **specific taste principle** from the source `{domain}.json` that justifies the change, with concrete before/after values.

The test: **"Could I have written this reasoning without having the source taste profile?"** If yes, it's slop. Rewrite it.
