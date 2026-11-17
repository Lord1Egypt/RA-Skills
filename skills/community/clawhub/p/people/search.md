# Search — Making The Address Book Answer Questions

A record store is only worth its retrieval. The design question is not "what should we store" but "what questions must this answer", and every field and tag that does not serve a question is overhead.

**Read `~/Clawic/data/contacts/contacts.md` first for any recall question**, then open only the person files the index points at. Answering from conversation memory instead of the book is the failure this whole section exists to prevent (SKILL.md Output Gates).

**Contents:** [The Questions It Must Answer](#the-questions-it-must-answer) · [Tag Vocabulary](#tag-vocabulary) · [Query Patterns](#query-patterns) · [Answering Well](#answering-well) · [Fuzzy And Partial Recall](#fuzzy-and-partial-recall) · [When The Answer Is Not There](#when-the-answer-is-not-there)

## The Questions It Must Answer

If the book cannot answer these, the schema is wrong regardless of how much it holds.

| Question | Field it depends on | Failure if the field is missing |
|---|---|---|
| "What do I know about Sarah?" | The whole record | Nothing to brief from |
| "Who do I know at Acme?" | Role and employer, current | The user asks the network publicly instead |
| "Who lives in Berlin?" | City, current | A trip happens with nobody contacted |
| "Who have I not spoken to in six months?" | `Last contact` and tier | The overdue sweep cannot run at all |
| "Who does woodworking / climbs / speaks Portuguese?" | Interests and tags | The article, the job, the invitation goes to nobody |
| "Who introduced me to Ines?" | How we met | An introduction cannot be routed back |
| "Whose birthday is next month?" | The date index | `dates.md` |
| "Who was at the Berlin conference?" | The event debrief artifact | The next edition starts from zero |
| "Who knows both me and Tom?" | `## Groups` | An introduction is made that should not be, or a confidence leaks |
| "What did she tell me about her father?" | The log, with dates | The question gets asked again, painfully |
| Anything else | Whatever the record holds | Say what is missing rather than inferring it |

## Tag Vocabulary

Tags exist to answer the questions above and nothing else. A tag that has never been the subject of a query is deleted at the roster review.

- **Keep the vocabulary closed and small.** Ten to twenty tags for a roster of 150. The failure mode is fifty tags used once each, which is the same as no tags.
- **Four families, and no more**: relationship (`family`, `work`, `neighbor`, `climbing-group`), place (`madrid`, `berlin`), capability or interest (`lawyer`, `woodworking`, `portuguese`), state (`dormant`, `bounced`).
- **Tier is not a tag** — it is a field, because arithmetic runs on it.
- **Never tag a sentiment.** `favorite`, `annoying`, `high-value` are verdicts (`details.md`).
- **Singular, lowercase, kebab-case**, and one form per concept forever: `climbing`, never also `climb` and `Climbing`. Store the chosen vocabulary under `conventions.tags` in `config.yaml` so it stays stable across sessions.
- Places are tags *and* a field: the field is where they live now, the tag is where they can be found — someone who splits time between two cities carries both tags and one current city.

## Query Patterns

| Ask | How it resolves |
|---|---|
| By name, exact | Key lookup, then alias field — a name change means the old name only lives in the alias (`names.md`) |
| By employer | Role field, then the log; treat any employer over two years old as unverified and say so |
| By place | City field for current, place tags for reach; a stale city is the most common wrong answer this box gives |
| By interest or capability | Tags first, then `## Details` text; report the tag matches and the text matches separately |
| By silence | `Last contact` arithmetic, filtered by tier and by `do-not-surface.md` (`keeping-in-touch.md`) |
| By connection | `## Groups` plus the "how we met" field |
| By event | The debrief artifact, not the address book |
| By something they said | Log entries, which is why every entry carries a date |
| Anything else | Scan the address book, name the matches, and say explicitly what was searched |

## Answering Well

- **Answer from the book, then say what the book does not know.** "Three people at Acme: Maria (product, current), Tom (left in 2024), Ines (unverified since 2023)" is a useful answer; a bare list of three names is not.
- **Date the facts.** Every answer about a job, a city, or a partner carries how old the fact is. A confident stale answer is worse than an admitted gap, because the user acts on it.
- **Rank by usefulness**, not alphabetically: current beats former, recently contacted beats long-silent.
- **Never invent a link.** If the user asks who they know at a company and nobody matches, the answer is nobody, not the closest thing.
- Surfacing anyone on `do-not-surface.md` is allowed when the user asks about them directly and forbidden when the answer is a list of people to contact — the suppression is about proposing contact, not about denying facts (`privacy.md`).

## Fuzzy And Partial Recall

The most common real query is not a field lookup. It is "the woman from the conference who worked in packaging".

1. **Decompose into what the record would hold**: event, employer or field, gender, timeframe. Each becomes a filter.
2. **Search the event artifact first** when a place or occasion is named — that is precisely what debriefs are for (`capture.md`).
3. **Widen one filter at a time**, never all at once, and say which filter was dropped to produce the candidate.
4. **Offer at most three candidates with the distinguishing detail each**, so the user recognizes rather than verifies.
5. **A miss is a capture failure**, and it is worth naming as one: the person was met and not recorded, or recorded without the detail that would have found them.

Partial-name recall is a special case: check the alias field before concluding the person is absent, since a name change is the most frequent reason a search for someone who is definitely there returns nothing.

## When The Answer Is Not There

- Say what was searched and what was missing. "Nobody in the book is tagged `portuguese`; six people have Portugal in their notes" tells the user what to do next.
- Offer the fix once: the field or tag that would have answered it. Do not launch a data-collection interview (SKILL.md Rule 6).
- If the same question fails twice, the missing field is real and worth adding to the roster review checklist (`hygiene.md`).
- Never answer a recall question from anything other than the record, general knowledge included. A plausible fabrication about a person the user knows is the most damaging possible output of this skill.

**Write in the same turn**: any tag or field created to answer a question goes onto the person's record and, if it is a new tag, into `conventions.tags` in `~/Clawic/data/people/config.yaml`. A question the book failed twice goes into `## Roster Shape` in `~/Clawic/data/people/memory.md` as the gap to close at the next review (`memory-template.md`).
