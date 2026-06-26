## Appendix

### Naming guidance for larger projects

If the project will contain many screens, use stable ordered titles from the start.

Recommended pattern:

- `01 Onboarding - Welcome`
- `02 Onboarding - Personal Info`
- `10 Today - Main`
- `20 Progress - Overview`
- `30 History - Browse`
- `40 Settings - Profile`

This improves canvas scanning and reduces later cleanup.

### What a good Stitch pass should produce

A successful pass should leave the session with:

- one clearly identified target project
- one clearly identified canonical screen or small set of candidate screens
- the exact prompt or edit intent that produced the result
- a short judgment on whether the result is accepted, rejected, or needs another small iteration

After each generate/edit/variants, report to the user:
- the project and screen IDs
- the output location (if artifacts were saved)
- a short design assessment
- the recommended next step

If those artifacts are missing, slow down and re-establish state before continuing.

### Not recommended

- copying browser-product claims into MCP instructions without revalidation
- starting with a "blank page, no design system" prompt
- skipping the empathy step and jumping straight to colors and layouts
- using Space Grotesk for headlines (labels and timestamps only)
- treating copywriting as a final polish step instead of a structural design element
- picking one variant winner instead of composing from multiple variant elements
- using design boards or mood boards as substitutes for real app screens in a product redesign
- attempting to redesign a whole app from memory in a single prompt
- exporting 5+ complex pages to AI Studio all at once (causes overloading and missing content)
- forgetting to select all screens before exporting to AI Studio
- moving into implementation code before the design family is coherent
- trusting the heat map output without verifying which screen it actually analyzed
- rebuilding an accepted greenfield Stitch design from screenshots when a usable export already exists
- using exact structural descriptions instead of mood adjectives in prompts
- taking section-by-section screenshots for redesign — use full-page captures instead
- uploading a screenshot and asking Stitch to add something to it — Stitch regenerates the entire screen, losing consistency. Instead: generate the addition in isolation, integrate elsewhere (Figma or code)
- using multiple screens in one prompt — produces broken theming, incomplete outputs, errors. One prompt = one screen or one component
- using Reimagine/NanoBanana for small changes — it redesigns everything. Use for full overhauls only
- trusting generated content blindly — Stitch invents copy, subtexts, badges, status labels that weren't requested
- accepting broken generated image assets in core UI — replace with robust local tokens or request a constrained edit
- long prompts over 5000 characters — Stitch truncates or omits elements. Keep focused, iterate instead
- letting design drift across edits — after 3+ edits in a session, add: "Use the existing design system established in this project. Do not create new styles."

### Google screenshot URL size parameters

Stitch returns screenshot URLs on `lh3.googleusercontent.com`. Append these suffixes to control resolution:

| Suffix | Result |
|--------|--------|
| `=w780` | Full mobile design width (good default) |
| `=w1440` | Full desktop design width |
| `=s2000` | Max 2000px on longest side |
| (no suffix) | Thumbnail only (~168px wide) |

### Optional local workflow enhancements

If you want aliases, execution artifacts, derivation history, or last-active-screen state, use [`local-workflow-conventions.md`](../local-workflow-conventions.md).

These are useful for traceability, but they are optional and not part of the Stitch MCP contract.

### References

- Prompt reference: [`prompt-structuring.md`](../prompt-structuring.md)
- Visual review and artifacts: [`visual-review-and-artifacts.md`](../visual-review-and-artifacts.md)
- Redesign prompt patterns: [`redesign-prompt-patterns.md`](../redesign-prompt-patterns.md)
- Local workflow conventions: [`local-workflow-conventions.md`](../local-workflow-conventions.md)
- Style keywords: see the Style keyword reference table in the Prompting & Generation section

Keep the main skill focused on operating rules. Use the prompt reference only when the request needs prompt shaping or prompt repair.
