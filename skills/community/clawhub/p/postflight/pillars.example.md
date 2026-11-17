<!-- TEMPLATE — delete this line once you have edited the file. While it is present, the skill ignores this file and runs the default schedule. -->
# Pillar configuration — personal overlay

Copy this file to `postflight-state/pillars.local.md` — not next to this
one, which an upgrade overwrites — make it yours, and delete the TEMPLATE
line at the top. The full walkthrough is in
docs/CUSTOMIZE.md. How it works: your `## Pillars` list and `## Weekly
grid` below replace the defaults in CONTENT.md wholesale — so keep them
complete, don't write a diff. A pillar named here without its own
`## <pillar>` section below falls back to the same-named section in
CONTENT.md (that's how builds/insights/build-in-public inherit the stock
machinery).

Each pillar declares five properties (defined in CONTENT.md "Pillar
properties"): `weight` (slots/week), `media` (`generated`,
`photos:<dir>`, or `none`), `link` (`reply` or `none`), `register`
(`technical` or `personal`), `source` (`repos`, `news`, or `own-notes`).

Two rules worth knowing before you edit:

- Renaming a pillar resets its history — angle rotation and the weekly
  targets read the `pillar` field of past post-log entries by name.
- If you have no public repos yet, replace the builds cells with your
  other pillars; a `source: repos` pillar with nothing to sweep just
  falls back every turn.

## Pillars

Keep the total at 21 (3 posts/day × 7). Two personal pillars are sketched
below — replace them with topics you can write about firsthand.

- **builds** (8) — media: generated · link: reply · register: technical ·
  source: repos. Own-repo demos. Media-first: the body shows the thing,
  the repo link ships as the first reply, never in the body.
- **insights** (7) — media: none · link: none · register: technical ·
  source: own-notes. Opinions, lessons, hot takes from real work. Pure
  text, no links.
- **your-hobby** (4) — media: photos:media/photos/ · link: none ·
  register: personal · source: own-notes. A topic with photos you take
  yourself (hiking, cooking, a sport). Cells fall back until the photo
  library has photos in it.
- **your-craft** (2) — media: none · link: none · register: technical ·
  source: own-notes. A second firsthand topic, no photos needed: the
  thing you teach, the trade you know, the scene you're part of.

## Weekly grid

Every cell may carry a *(fb: pillar)* fallback, used when the cell's
pillar has no material this turn. Keep the two smoothing rules from
CONTENT.md: never two `link: reply` pillars in adjacent slots, never the
same pillar in adjacent slots.

| Day | Slot 1 | Slot 2 | Slot 3 |
|---|---|---|---|
| Mon | builds *(fb: insights)* | insights | your-hobby *(fb: insights)* |
| Tue | builds *(fb: insights)* | your-craft | insights |
| Wed | builds *(fb: insights)* | your-hobby *(fb: insights)* | insights |
| Thu | builds *(fb: insights)* | insights | your-craft |
| Fri | builds *(fb: insights)* | your-hobby *(fb: insights)* | insights |
| Sat | builds *(fb: insights)* | insights | your-hobby *(fb: insights)* |
| Sun | builds *(fb: insights)* | insights | builds *(fb: insights)* |

## your-hobby

What this pillar covers, in your words. Then its angles — the distinct
ways into the topic, so the account doesn't repeat itself:

1. the specific outing — where you went, the one detail worth telling
2. the gear or technique opinion — what you actually use and why
3. the thing beginners get wrong

Hard rules (what's off limits — be concrete):

- Written in the personal register, VOICE.md "Personal posts": one
  concrete detail, no links, no hashtags, the photo carries the post.
- Post AFTER leaving a location, never from it, and never same-day.
- Keep home-adjacent spots out of the photo library entirely.

## your-craft

Same shape: what it covers, angles, hard rules. Example angles for a
teaching-adjacent topic:

1. the thing students consistently get wrong, explained like a debrief
2. a cool fact a layperson can enjoy and a practitioner can nod along to
3. a tool or procedure demystified — "what it actually does"

Hard rules:

- Accuracy over specificity: never invent numbers, citations, or
  procedure details. Wrong instructional detail from a practitioner
  account is worse than no post.
- Firsthand framing beats encyclopedia framing: "what I tell students"
  over "did you know".
