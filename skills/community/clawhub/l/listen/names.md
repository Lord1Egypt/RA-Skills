# Names — Proper Nouns, Casing, and Code Identifiers

Proper nouns are where STT fails hardest: engines are trained on frequency, and names are rare by definition. Every play here rides on SKILL.md Rule 5 — the correction direction is common-word → proper-noun, almost never the reverse.

## People

- A garbled person name usually surfaces as a common word or a more frequent name ("Kowalski" → "co-worker", "Aisha" → "I should"). Candidate pool: contacts, prior conversations, names in the current thread.
- Never silently normalize the spelling of a person's name ("Jon" → "John", "Sara" → "Sarah"). Variants are identities. First unknown name that will appear in writing or feed a recipient: confirm spelling once, then store it — `sara → Sara (person) | confirmed | <date>`.
- Transliterated names have no single right form ("Mohammed/Muhammad/Mohamed") — the user's chosen form is in the lexicon or their contacts; absent both, ask once.
- Names the engine split ("Anna Lise" → "analyse") or fused ("johnsmith") re-enter via re-segmentation (`repair.md`).

## Brands and Products

- Engines lowercase and dictionary-ize brands: "github" → "get hub", "PostgreSQL" → "postgres sequel", "Figma" → "figure ma". Repair casing along with the token: the lexicon's right side stores canonical casing (GitHub, PostgreSQL, iPhone, macOS).
- Camel-case brands (iPhone, eBay, LaTeX) never survive transcription — restoring casing is part of the repair, not a style choice.
- A brand the user says daily belongs upstream in engine vocabulary biasing once it crosses the 5+ recurrence threshold (`tuning.md`).

## Code Identifiers

Spoken code arrives as prose. Reassemble by the conventions of the active codebase:

| Heard | Context | Reassemble as |
|---|---|---|
| "get user by id" | camelCase codebase | `getUserById` |
| "user underscore id" | explicit separators | `user_id` |
| "dash dash force" | CLI flag | `--force` |
| "dot env" | filename | `.env` |
| "main dot py" | filename | `main.py` |
| "slash api slash users" | route/path | `/api/users` |

- Candidate pool is the codebase itself: grep for the skeleton-nearest real identifier before inventing one. A spoken identifier that matches nothing in the repo is either new (user is naming something) or garbled — the sentence's verb decides ("create a function called..." = new; "call..." = existing).
- Acronym casing: "jason" → JSON, "sequel" → SQL, "yaml" arrives fine, "gooey" → GUI. These are lexicon-worthy pairs on second sighting like any other.

## Spelling-Out

- NATO alphabet ("B as in bravo") and ad-hoc spelling ("K-U-B") both arrive as prose. Collapse letter sequences into the spelled token before any other repair.
- When YOU need to confirm a spelling, use the user's preferred convention (`spelling conventions` preference area): NATO for radio-trained users, plain "K, U, B" otherwise. Default plain — NATO reads as jargon to most users.
- Mixed mode ("Kowalski, K-O-W...") — the spelled fragment is authoritative over the transcribed word; the user spelled it because they expected the miss.

## Codenames and the Never List

- Project codenames are deliberately odd ("Bumblebee", "Krakatoa") and are exactly what a naive repairer destroys. One sighting in the user's world (repo name, doc title, their own confirmation) → add to the Never list so it is never flagged again.
- The Never list is checked before flagging any token (`repair.md`), which makes it the cheapest accuracy win in this skill: one line prevents every future false repair of that name.

## Diacritics

- Engines strip diacritics ("Zoë" → "Zoe", "São Paulo" → "Sao Paulo"). Restore them only for names whose canonical form is established — in the lexicon, the user's contacts, or unambiguous geography. Restoring diacritics onto a person's name the user themselves writes without them is a miscorrection.
