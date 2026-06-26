# Audit Checklist

Use this to trim a skill, check for spec drift, or tighten a newly built skeleton before handing it off.

## 1. Trigger quality

- [ ] Is the `description` clear about what the skill does?
- [ ] Does it say when to use the skill?
- [ ] Would normal user phrasing trigger it?
- [ ] Is the description pushy enough to catch casual/informal phrasings?
- [ ] Does it include 3-5 concrete trigger phrases or adjacent concepts?
- [ ] Is the scope honest, or is it promising too much?
- [ ] Are there obvious overlaps with another existing skill?

## 2. Decide / build / audit fit

- [ ] Is this actually a skill problem rather than a plain edit, tool use, or subagent task?
- [ ] If building, was a skill explicitly justified before files were added?
- [ ] If auditing, are we tightening the existing skill instead of reflexively replacing it?
- [ ] Does the skill still say "do nothing special" when that is the right answer?

## 3. SKILL.md discipline

- [ ] Is `SKILL.md` easy to scan?
- [ ] Does it contain the core workflow, not every edge case?
- [ ] Are long examples/checklists moved into `references/`?
- [ ] Are references named explicitly so they are discoverable?
- [ ] Does the file avoid policy sprawl and manifesto language?
- [ ] If this skill builds new skills, does it still stay narrow and concrete?
- [ ] Is `SKILL.md` under ~500 lines? If approaching this limit, is detail pushed to references?

## 4. Writing quality

- [ ] Are instructions in imperative voice? ("Read the file" not "You might want to read the file")
- [ ] Do instructions explain *why* steps matter, not just *what* to do?
- [ ] Are ALWAYS/NEVER/CRITICAL used sparingly and only when reasoning is also given?
- [ ] Are examples concrete and minimal (1-2, not 10)?
- [ ] Is output format defined with a template when consistency matters?
- [ ] Is there unnecessary preamble before the first actionable instruction?

## 5. Build minimalism

- [ ] Is the folder structure the smallest one that works?
- [ ] Is `SKILL.md` present and sufficient on its own?
- [ ] Are `references/` files limited to justified supporting detail?
- [ ] Are there 1-3 reference files at most unless scope truly demands otherwise?
- [ ] Is an `assets/` folder present only if the skill needs bundled templates or static files?
- [ ] Is a `scripts/` stub included only if deterministic execution is clearly needed?
- [ ] Are publish suggestions optional rather than embedded process requirements?

## 6. Folder hygiene

- [ ] Does every file directly support the skill's job?
- [ ] Are there unnecessary docs like README, CHANGELOG, or setup notes?
- [ ] Are there stale placeholders or abandoned experiments?
- [ ] Is there any duplicated content between `SKILL.md` and `references/`?
- [ ] Are scripts present only when deterministic execution is needed?

## 7. Spec drift and staleness

- [ ] Do instructions still match the current tools/workflow?
- [ ] Are referenced files and paths real?
- [ ] Are examples still accurate?
- [ ] Did the skill accrete side-missions beyond its original purpose?
- [ ] Should some content be deleted instead of updated?

## 8. Smoke test

- [ ] Has the skill been tested with at least 2-3 realistic prompts?
- [ ] Does a clear trigger prompt correctly activate the skill?
- [ ] Does an edge-case prompt activate it and behave reasonably?
- [ ] Does a near-miss prompt correctly *not* activate it?

## 9. Do-nothing check

Before expanding the skill, ask:
- [ ] Would a plain edit solve this faster?
- [ ] Would using an existing tool or skill solve it cleanly?
- [ ] Is this really a subagent problem, not a skill problem?
- [ ] Is the proposed addition carrying its own weight?

## 10. Tool Addition Gate (lightweight)

- [ ] Did we check existing tools first?
- [ ] Would a lean skill solve the problem without inventing a new primitive?
- [ ] Is a new script/tool being proposed for a real capability gap rather than convenience theater?

## Recommended outcomes

### Keep as-is
The skill is already sharp, current, and lean.

### Tighten
Trim wording, improve description, move detail into `references/`, delete dead files.

### Restructure lightly
Keep the skill, but separate core workflow from supporting detail.

### Build minimally
Create or refine only the smallest justified skeleton.

### Retire / merge
If the skill duplicates another one or no longer earns its context cost, remove or merge it.
