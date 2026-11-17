# Source Extraction

This reference applies when the user provides materials, a link, or a research topic, and this skill must turn raw input into video-ready facts before writing the prompt.

## Priority Of Sources

1. Materials the user supplied directly: pasted text, attached image, attached document.
2. Links the user supplied: official product site, official docs, GitHub repo, release notes.
3. Primary or authoritative sources for non-product topics: papers, organization sites, government archives, museum records.
4. Reputable background sources, preferring English-language coverage for technical and global topics.

Do not pull from sources the user did not ask for if they would dilute or contradict the brief. Do not fabricate sources.

## Ten Items To Extract

For any subject, try to extract these ten items. Missing **factual** items (a real feature, a real number, a real UI label, a real command) are omitted or turned into a question for the user — they are **not** tagged as creative assumptions. Only **staging choices** (camera, layout, lighting, generic visual treatment, transition copy) may be tagged `[creative assumption]` when the source does not pin them.

1. **Name** — exact name with correct casing (e.g. `HiAPI`, not `Hi API`).
2. **Plain-language definition** — one sentence a viewer with no background understands.
3. **Top three to six core functions** — what it does, in user-facing verbs.
4. **User actions** — the literal actions a user takes (commands typed, buttons clicked, files uploaded).
5. **Outputs produced** — what the user gets back (image, video, JSON, file, dashboard row).
6. **Differentiator** — the one thing the subject does that adjacent things do not.
7. **Evidence** — numbers, dates, versions, throughput, latency, counts. Cite the source.
8. **Visual hooks** — interfaces, logos, screenshots, charts, maps, characters, devices that can fill the frame.
9. **Exact on-screen text** — command strings, button labels, menu items, status messages, taglines.
10. **Constraints** — claims the subject should not make, features the product does not have, tone to avoid.

## Converting Facts Into Video Elements

| Fact type | Becomes |
| --- | --- |
| A function | A typed command, a UI card, or one narration line |
| A workflow step | A click, an upload, a progress marker |
| A number | A large stat, a badge, a counter |
| A document | A page preview or a source card |
| A date or event | A date marker, a map pin, a symbol |
| A differentiator | A side-by-side comparison or a single hero shot |
| A constraint | An item in the Negative Constraints section, not on screen |

## Weak Or Missing Sources

When sources are weak or absent:

- Mark plausible **staging** (camera, layout, lighting, mood) as `[creative assumption]` in the Source Extraction Summary so the user can correct it. Do not tag invented **facts** that way — drop them or ask the user.
- Frame uncertain claims as directional (`"faster onboarding"`) rather than factual (`"3.4x faster onboarding"`) unless a source supports the number.
- For real UIs, preserve real button labels and menu items. Do not invent screen text that the product does not have.

## Minimum Pre-Write Summary

Before writing the prompt, this skill should be able to answer these six questions in one bullet each:

1. **Topic** — what the video is about, in five words or fewer.
2. **Target audience** — who is watching and what they already know.
3. **Key facts** — three to six facts that must survive into the prompt.
4. **Required on-screen text** — exact strings to render.
5. **Visual assets** — images, screenshots, logos, or shots to feature.
6. **Claims to avoid** — what the brief or the product cannot honestly say.

This six-line summary feeds directly into the Source Extraction Summary and Negative Constraints sections of the final prompt.

## Handling GitHub Repositories

When the user provides a GitHub URL:

- Pull the repo name, the one-sentence description, the top three README features, the install command, and one example command.
- If the README has a hero image or a logo, treat it as a visual hook.
- Do not invent stars, forks, or download counts. If they are not in the brief, leave them out.

## Handling Product URLs

When the user provides a product site:

- Pull the product name, the hero headline, the top three feature names, the call-to-action label, and the primary color.
- Treat the hero illustration as a visual hook, but do not promise the model can recreate it exactly.

## Handling Research Topics

When the user provides only a topic (no URL):

- Find one or two authoritative sources before drafting.
- Pull three to five concrete facts with dates or named actors.
- If you cannot find authoritative facts, ask the user for sources before writing the prompt. Do not stage invented history.
