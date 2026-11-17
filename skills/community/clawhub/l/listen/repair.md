# Repair — From Suspect Token to Candidate

The full version of the Repair Procedure in SKILL.md. Work token-first; every step is a check, not a guess.

## Flagging Suspect Tokens

A token is suspect when it breaks one of these, in descending reliability:

| Break | Signal | Example |
|---|---|---|
| Domain | Common word where the sentence needs a term of art | "deploy the **communities** cluster" |
| Collocation | Words that never co-occur in this user's world | "open a **poll request**" |
| Register | Casual word inside technical instruction, or vice versa | "run the **jest** suite" vs "tell him a **Jest**" |
| Grammar | Sentence parses only if the token is something else | "**sign** wave input" |
| Reference | Pronoun or name pointing at nothing in context | "ask **Mark**" when no Mark exists anywhere in the user's world |

Grammar-clean sentences still hide errors: homophones pass every syntactic check. Test intent, not syntax.

Before flagging anything, check the lexicon's `never` list — deliberately odd codenames live there and are exempt.

## Candidate Generation (priority order)

1. **Lexicon match** — the wrong side of a stored pair matches the token. `confirmed` entries apply pre-emptively without scoring.
2. **Phonetic neighbors** — skeleton test (below) against the candidate pool: session vocabulary, open files and repo identifiers, recent topics, contacts and names the user has used, lexicon right-hand column.
3. **Re-segmentation** — splits and joins (below) before declaring the token unknown.
4. **Homophone table** — the catalog at the bottom, for tokens that fit grammar but not intent.

Never draw candidates from general vocabulary: a phonetic neighbor the user has no connection to fails the context signal by construction (SKILL.md Rule 4).

## Phonetic Skeleton Test (Rule 4, expanded)

A simplified Soundex/Metaphone: enough to catch STT confusions without a library.

1. Fold sound classes: C/K/Q→K · S/Z/soft-C→S · F/PH/V→F · J/G-soft→J · D/T→T · B/P→P. Unlisted letters stay themselves.
2. Strip vowels (keep a leading vowel).
3. Collapse doubled letters.
4. Compare skeletons: edit distance ≤2 = phonetic neighbor.

Silent letters inflate distance ("sign" → SGN vs "sine" → SN reads as 1, not 0) — true homophones are caught by the catalog below, not the skeleton.

Worked examples:

| Heard | Skeleton | Candidate | Skeleton | Distance | Verdict |
|---|---|---|---|---|---|
| web look | WPLK | webhook | WPHK | 1 (L/H) | neighbor |
| communities | KMNTS | Kubernetes | KPRNTS | 2 (insert P, M/R) | neighbor |
| sine | SN | sign | SGN | 1 | neighbor (homophone; catalog catches it at 0) |
| pull | PL | Perl | PRL | 1 | neighbor — context decides |
| coffee | KF | Kafka | KFK | 1 | neighbor — context decides |
| meeting | MTNG | Mitting (surname) | MTNG | 0 | neighbor — direction check (Rule 5): rare word wins only if context demands it |

Distance ≤2 qualifies; it never confirms. The context signal (term already in the user's domain) is always required on top.

## Re-segmentation

STT segments by acoustics, not meaning. Before treating a token as unknown, try:

- **Join**: adjacent tokens that fuse into a domain term — "web hook" → webhook, "get hub" → GitHub, "type script" → TypeScript, "a track" → attack.
- **Split**: one token that hides two words — "attackvector" is rare; more common is a fused proper noun: "johnsmith" → John Smith.
- **Boundary shift**: move one syllable across the space — "an ice cream" / "a nice cream"; "the sky" / "this guy".

Re-segmented results re-enter the pipeline as normal candidates: skeleton + context, same two-signal bar.

## Scoring Context Fit

Rank surviving candidates by source strength:

1. Lexicon `candidate` entry (already seen once)
2. Term used earlier in this session
3. Identifier in open files, repo, or active project
4. Term from the user's stored vocabulary domain (config preference area)
5. Name from the user's contacts or prior conversations

Tie between two candidates from the same tier = offer both (Rule 2 allows 2, never 3). A candidate with phonetic distance 0-1 from tier 4 beats distance 2 from tier 2 only when the sentence's domain demands it — when in doubt, the more recent source wins.

## Homophone Catalog (grammar-proof errors)

High-frequency STT confusions in technical and business dictation. These pass grammar checks — flag them only when intent breaks:

| Heard | Often meant | Domain tell |
|---|---|---|
| sine | sign | contracts, documents |
| cash | cache | performance, browsers, CDN |
| sequel | SQL | databases |
| poll / pole | pull | git, requests |
| four / for / fore | 4 | counts, versions (`numbers.md`) |
| to / too | 2 | counts, versions (`numbers.md`) |
| right | write | file operations |
| read | red / reed | status colors vs I/O |
| male | mail | email flows |
| week | weak | schedules vs quality |
| higher | hire | recruiting |
| principal | principle | finance vs argument |
| accept | except | conditions, filters |
| new | knew | features, releases |
| sent | cent | messaging vs money |
| billed | build | invoicing vs CI |

The table is a candidate source, not an auto-correct list: every substitution still needs the context signal.

## Multi-Token Damage

- 2 suspect tokens: repair each independently; if the repairs interact (one changes the reading of the other), confirm the whole clause instead.
- 3+ suspect tokens: SKILL.md Rule 8 — stop token repair, quote your full interpretation for a yes/no, and open `degraded.md` (mic, noise, crosstalk).

## End-to-End Example

Transcript: "can you push the fix to the coffee branch and tag it be one"

1. Suspects: "coffee" (domain break — no coffee in a git sentence), "be one" (register break after "tag it").
2. Candidates: "coffee" → skeleton KF; repo has branch `kafka-consumer` → "kafka" KFK, distance 1, context tier 3. "be one" → re-segmentation join → "b1"; tag pattern `v1`/`b1` exists in repo → context tier 3.
3. Both pass two signals. Push+tag = side effects → Rule 1 says confirm, Rule 2 says with candidates: "Pushing to `kafka-consumer` and tagging `b1` — right?"
4. On yes: act, then log `coffee → kafka | candidate | <date>` and `be one → b1 | candidate | <date>` to the lexicon.
