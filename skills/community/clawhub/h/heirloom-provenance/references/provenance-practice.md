# Family Provenance — Practice Guide

## Why provenance dies

Family object knowledge is oral, contextual, and terminal. The keeper of the
story is usually the eldest person who physically lived near the object; when
they die, the chain breaks silently. Families consistently report the same
regret after a death: "we never asked." Meanwhile the objects flow through
estate settlement where their *story* has no field in the paperwork — only
their value — so the system itself strips provenance.

The fix is boring and effective: a registry, captured early, linked to the
physical object.

## The registry schema

Each record (ID `HL001...`) carries:

- **description** — what a stranger would need to identify it
- **origin** — when/where made or acquired, by whom (uncertainty allowed)
- **owner_chain** — ordered owners with dates; the spine of provenance
- **story** — free text, append-only via `story append` so interviews
  accumulate rather than overwrite (each append is dated)
- **value** — appraisal value + date; `unknown` is honest and allowed
- **condition** — matters for both insurance and story
- **photos** — file references (the tool stays local; no cloud)
- **wishes** — sealed per-person rankings (see below)

Uncertainty is first-class: provenance work is reconstruction, and "Otto's
father maybe carried it in a war — which war unknown" is a *better* record
than a confident guess.

## Interviewing: the method

1. **Object-in-hand sessions.** Memory unlocks through objects. Bring the
   object; ask the 7 core questions (in SKILL.md). One room per session —
   objects cue each other.
2. **Audio first, structure later.** Record freely; transcribe at leisure;
   append transcript excerpts with `story append`. Dated appends build an
   provenance *timeline* of the research itself.
3. **Ask for the negative space.** "Who was supposed to get it?" and "was
   there ever a fight about it?" capture the family's own distribution
   history — often the actual source of present-day tension.
4. **Second keeper rule.** Until two people know a story, it is not saved.
   The storybook export is how the second keeper is made.

## Estate and insurance use

Appraisers and insurers accept provenance when it is:

- **Documented** (written, dated, attributed to a source)
- **Consistent** (owner chain matches dates and events)
- **Contemporaneous or sworn** (interview transcripts with dates qualify)

The `report` output per object is formatted for exactly this: identification,
chain of ownership, appraisal history, condition, story sources. For
insurance schedules, values must be replaced by professional appraisal — the
registry's value field is the *placeholder* that tells the appraiser where
to look.

## Distribution fairness mechanics

The failure mode of object division: anchored positions, first-mover
advantage, and dollar-equality applied to non-fungible things.

1. **Sealed wish-lists.** Everyone ranks wanted objects before seeing
   others' lists. Sealed collection prevents anchoring and strategic
   sandbagging.
2. **Conflict detection.** Two people ranking the same object #1 is THE
   thing to know before a family meeting, not during it. `conflicts`
   surfaces overlaps with rank information.
3. **Wish-maximizing draft.** `draft` assigns objects to maximize top-wish
   satisfaction under rotation fairness (seeded): everyone picks in turn,
   order by seeded coin flip, wishes shown at each pick. Provably no one
   envies the other's bundle more than their best remaining pick.
4. **Equalization payments.** When high-value objects skew a bundle
   (one gets the $4,500 watch, the other the $200 china), the draft prints
   a cash equalization for the *value gap only* — the story-objects are not
   priced.

## Tags and physical linkage

A registry unlinked from the physical object dies at the first house move.
Print the tag (name, ID, QR payload = file path or hosted URL), attach it
underneath or inside the object. The QR payload is configurable — families
who want cloud hosting can point it anywhere; the default is a local
relative path so the system works fully offline.

## Sensitivity

Heirloom data includes family conflict history — treat the JSON like a
diary. It is also the single most useful file a future genealogist in the
family will ever find; archive it in more than one place.
