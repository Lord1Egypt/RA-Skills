# Quality checklist

The script owns deterministic gates. Agents add evidence-based literary review;
they do not convert taste into a hidden global rule.

## Script gates

`novelforgectl` must reject:

1. missing or malformed project, blueprint, Context Ticket, review, or
   settlement files;
2. a state transition that skips a phase or uses the wrong previous state;
3. a dependency ID that is missing, unsafe, or not declared by the blueprint;
4. a source hash, blueprint hash, engine manifest, or review hash that no longer
   matches the file on disk;
5. an engine card with an invalid contract, duplicate ID, or path escape;
6. a settlement submitted before both text and engine reviews pass.

## Text diagnostics

`novelforge_lint.py` reports cliches, possible perspective/mental-state signals,
modern units/terms, AI stock tropes (`ai-trope`, such as rhetorical question
endings or multi-genre cliches), pompous generic naming (`pompous-naming`),
repetitive mechanical symmetry (`repetitive-action`), and flat
sentence cadence (`flat-cadence`). These are warnings by default. Only the
current project policy can promote a rule ID to an error.

## Story review evidence

Every review check states `rule`, `status`, and an evidence location. Reviewers
must verify:

- scene goal, character choice, consequence, and next question;
- viewpoint and knowledge boundary;
- temporal, spatial, relationship, and resource continuity;
- hook introduction, progress, payoff, or retirement;
- character personality authenticity: key actions match current personality
  archive; personality shifts are supported by accumulated `pressure_log`
  evidence;
- anti-cliche plot sanity: conflicts are driven by institutional, economic,
  and social friction rather than cartoonish tropes (no unprovoked coffin gifting,
  no casual street market god-tier items, no unmotivated NPC loyalty);
- entity naming compliance: characters, locations, factions, and items
  adhere to `naming-methodology.md`;
- whether the selected Engine Snapshot was applicable rather than merely
  available.

## Delivery rule

`TEXT_PASS` and `ENGINE_PASS` are independent. Both are required before
Settlement, and Settlement is required before `DELIVERABLE`. A warning may be
accepted with a recorded rationale; an error cannot be waived by Markdown.
