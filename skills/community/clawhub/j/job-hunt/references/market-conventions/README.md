# Market conventions

What a market screens on that the posting does not say.

This table is the one thing in an assessment that is not derived from the CV or the
posting, and it is deliberately the only one. Every other conclusion cites an evidence
block; a market convention has nothing to cite, which is why it is written here by a
person, dated, and rendered to the reader **verbatim** rather than restated by the
model. The model may say where this CV stands against a convention — that sentence
cites CV blocks like any other — but it may not author, strengthen or extend the
convention itself.

Nothing automated can check that an entry is true. `why` and `added` exist so a person
can review it. `scripts/check_conventions.py` checks only the things a program can
decide. **Named residual risk: an entry can be substantively wrong rather than
numerically stale, and nothing here detects that. Only human review does.**

## Market keys

`cn`, `nl`, `de`, `uk`, `us`. A posting whose market is none of these gets
「本市场无惯例数据」 and no convention card at all. Never substitute a neighbouring
market's conventions: a wrong market card reads exactly like a right one, and the
reader has no source text to check it against.

## Entry shape

```yaml
market: cn
conventions:
  - id: cn-boss-profile-is-the-screen      # unique in the file, [a-z0-9-]+
    text_en: |-
      The sentence the reader sees, in English.
    text_zh: |-
      读者看到的那句话，中文。
    applies_when: "The condition under which this card renders at all."
    added: "2026-08-09"
    review_by: "2027-02-09"
    source:
      kind: published                       # published | maintainer
      publisher: "Who published it"
      title: "The document's title"
      url: "https://..."
      retrieved: "2026-08-09"
      quote: "verbatim string from the source that supports this entry"
      also:                                 # optional further citations, same shape
        - publisher: "..."
          title: "..."
          url: "https://..."
          retrieved: "2026-08-09"
          quote: "..."
    why: "Why a candidate cannot see this from the posting."
    protected_trait_note: "..."             # required ONLY if a protected trait appears
unverified:
  - note: "What could not be sourced."
    disclaims: [cn-boss-profile-is-the-screen]
```

## How a run reads a table

An assess run does not open these files. `scripts/convention_cards.py --market <key>`
prints each entry's `id`, `applies_when`, `review_by` (flagging a passed date with the
stale banner) and `text_en` / `text_zh`, verbatim. `source`, `why`, `added`,
`protected_trait_note` and `unverified` are for the person reviewing the entry and never
reach a run. A new field that a run must see has to be added to that script too, or no
run will ever read it. `check_assessment.py` still reads the YAML itself, so the gate
compares a card against the table, not against the script's output.

## Rules for adding an entry

- **No numbers.** A statistic here cannot be sourced and must not be invented.
  `check_conventions.py` fails on a digit or a percent sign in `text_en`, `text_zh`,
  `applies_when`, `why`, `source.publisher` or `source.note`. Write "look the current
  amount up on <the official page>", never the amount.
- **`url`, `title`, `retrieved` and `quote` are exempt from the digit ban.** A cited
  document's title is an identifier, not a claim, and statutes are numbered — that is
  how they are named. Banning digits there would only force the citation to be wrong.
- **Proper nouns that are the entry's only handle are exempt**, from a closed list in
  the script (`H-1B`, `Form I-9`, `Form I-983`). Do not "fix" a lint hit by deleting
  one — a reader cannot find the rule without its name. Extend the list in code, with a
  comment, or do not use the name.
- **Never hide a threshold behind a blank.** "The figure is set in the rule" is a
  lint-dodge, not compliance: the reader cannot act on it. Point at the exact source to
  read the number in.
- **Every entry says where it came from.** `source.kind` is `maintainer` when the person
  maintaining this table has worked in that market and is stating what they saw, or
  `published` when it rests on something citable, in which case it carries `publisher`,
  `title`, `url` and the date the url was checked. The two deserve different weight.
  A citation proves a claim was *published* — not that it is true, still current, or
  applicable to this reader. `retrieved` dates the check; it does not keep it fresh.
- **No protected traits.** Age, nationality, country of education, gender, ethnicity,
  religion, disability and institutional prestige stay out. Where the fact genuinely
  *is* a citizenship or national-origin rule — a right-to-work check, a
  citizenship-discrimination complaint route — the entry must carry a
  `protected_trait_note` saying so. That field makes the exception a decision someone
  made rather than a slip nobody noticed.
- **No CV layout.** Length, photographs and date formatting are tailoring instructions,
  not market screening facts. This table is about what the market weighs.
- **Nothing already covered elsewhere.** A third telling of the same fact is the
  repetition the requirement rows already prevent.
- **Both languages, always.** A claim shipped in only one language is a claim no
  reviewer compares. Reviews have repeatedly caught the Chinese saying more than the
  English (source says "encourages", zh says 「被要求」; a statute limiting the scope of
  a right, zh saying it does not exist at all). The lint warns on a length-ratio
  outlier and on modal-verb asymmetry, and **that is a hint, not a guarantee: semantic
  drift is not scriptable, and reviewing it is a person's job.**
- **`review_by` is mandatory** and is derived from staleness: an entry whose underlying
  fact is re-issued yearly gets three months; one that moves with practice gets six;
  a statute or a stable mechanism gets twelve. An expired `review_by` **fails this
  lint** (so CI catches it), while at runtime the card still renders with a
  「已过复核期」 / "past its review date" banner (the card follows the user's language)
  — a date passing without the code changing should not stop the skill working.
- **`unverified` must name what it disclaims.** Every assertion an `unverified` note
  disclaims must be **removed from the rendered text**, not footnoted. The reader never
  sees `unverified`, so a footnote there protects nobody. The lint warns when a note
  and the text it disclaims share vocabulary, because that is what that defect looks
  like.
