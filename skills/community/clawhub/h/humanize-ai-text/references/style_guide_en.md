# English Academic Style Manual (deep-rewrite guide for the agent)

> Integrity note: this manual improves the writing quality of your own drafts —
> clarity, natural register, commitment. It is not for defeating academic-integrity
> review or concealing AI use that should be disclosed; refuse that framing and
> point to references/compliance.md.

> Division of labor: `detect.py` produces a style self-check report, `transform.py`
> does safe mechanical cleanup, **you (the agent running this skill) do the
> revision** following this manual. Always finish with `verify.py` (integrity)
> and `compare.py` (before/after).

## 0. What this manual fixes

Stiff, templated academic prose shares a few roots: canned significance frames,
uniform sentence rhythm, abstract nouns where verbs belong, transitions doing the
work that content should do. The fixes below are ordinary principles of good
writing — applied systematically.

## 1. Seven rewrite moves (in priority order)

### 1. Replace inflated vocabulary with smaller words — then re-read
delve→look at; tapestry→mix; testament→proof; underscore→highlight; leverage→use;
utilize→use; foster→build/encourage; pivotal→key; robust→solid (unless statistics);
landscape→field/situation; intricate→complex; meticulous→careful; seamless→smooth;
garner→earn; realm→area; myriad/plethora→many. If the sentence collapses without the
fancy word, rewrite the sentence — don't prop it up with another fancy word.

### 2. Delete significance frames
Delete, don't replace: "serves as a testament to", "underscores the importance of",
"cannot be overstated", "marks a pivotal moment". Say the fact instead — e.g. what
changed, for whom, by how much (using facts already in the source text).

### 3. Unwind negative parallelism
"Not just X, but Y" / "It's not about X, it's about Y" → state X and Y as two plain
clauses, or drop the lesser one. Twice in one text is a templated-prose signature.

### 4. Convert -ing tails into finite clauses
", highlighting the importance of early diagnosis" → ". This highlights how early
diagnosis matters" — or better, delete: the main clause usually already says it.
Tacked-on participles ("underscoring…, reflecting…, demonstrating…") pad sentences
without adding content.

### 5. Replace vague attribution with real attribution — or silence
"Experts believe" / "Industry reports suggest" → name the source, cite it, or cut the
claim. If you cannot attribute it, you probably should not write it (this is also the
ethical core of the fix: unverified consensus inflation).

### 6. Re-rhythm the prose
- Vary sentence length deliberately: after two 30-word sentences, write a 7-word one.
- Vary paragraph mass: merge two thin paragraphs; split one dense one.
- Replace formulaic connectors (Moreover / Furthermore / Additionally / In conclusion)
  with content links or nothing. Good writers skip transitions constantly.
- One em-dash per few hundred words, maximum.
- Target: sentence-length variation (burstiness_cv in the detect.py report) above ~0.45.

### 7. Commit to a position
Templated prose hedges everything and concludes nothing. Strong writing says "we
think the subgroup effect is real, and here is what would change our mind." Add the
position the evidence supports — that is both better writing and the least
machine-like move available.

## 2. Worked example

**Before (dense boilerplate):**
> In today's rapidly evolving healthcare landscape, AI serves as a testament to human
> innovation. It is worth noting that AI is not just a tool, but a transformative
> force, highlighting the importance of early diagnosis and paving the way for
> personalized treatment. Despite these challenges, the future looks incredibly promising.

**After (format demo — see warning below):**
> AI's clearest win so far is triage: flagging a share of scans radiologists miss
> under load, early enough to change staging. Personalized treatment is further off —
> dosing models work, but only for a few drug classes. Reimbursement, not accuracy,
> is now the bottleneck.

Changes: landscape/testament/not-just-but/-ing-tail/challenges-formula all gone; every
sentence carries a claim the source text must already support; rhythm varies; the
paragraph takes a position.

## 3. Academic-register note

For journal manuscripts, naturalization ≠ casualization. Keep the passive where it is
conventional (methods), keep terminology, keep the citation hygiene. What you are
removing is the *flourish* — significance inflation, rhetorical parallelism, filler
transitions — not the formality. Standard methods phrasing ("GAPDH served as an
internal control") is field convention, not boilerplate; leave it alone.

## 4. Integrity red lines (enforced by verify.py)

Numbers, p-values, confidence intervals, DOIs, PMIDs, years, capital-letter
abbreviations (DNA/PCR/MRI), and any user-supplied term list must survive untouched.
If a revision requires changing a number, the revision is wrong.

## 5. Do not

- **Do not invent specificity.** (Alternative: draw specificity only from facts
  already in the source — quote the original data, hedges and limitations.) The claims in this manual's worked example
  demonstrate format only. In a real revision, specificity must come from facts
  **already in the source text** — adding a number, proportion, or conclusion to
  make prose look concrete is fabrication. verify.py warns on numbers absent from
  the original; the final responsibility is yours.
- Do not chase the report score by deleting content — evidence, hedges, and
  counterexamples are what make prose good.
- Do not synonym-rotate ("crucial"→"pivotal"→"vital"): swapping one set of
  boilerplate for another improves nothing.
- This toolkit is for writing-quality self-review; it does not assist concealing
  AI use or misrepresenting authorship (see references/compliance.md).
