# Production contracts

Read only the contract relevant to the current job. Keep it next to the production job card so revisions remain auditable.

## Exact-text manifest

Use this for posters, packaging, UI mockups, infographics, store listings, or localized assets.

```md
| ID | Exact string | Language | Case and punctuation | Line breaks | Placement | Hierarchy | Must be generated? |
|----|--------------|----------|----------------------|-------------|-----------|-----------|--------------------|
| T1 |              |          |                      |             |           |           | yes/no             |
```

Rules:

- Copy strings from user-approved source text; do not paraphrase.
- Quote each string once in the final prompt and refer to it by ID elsewhere.
- Keep the number of generated text blocks small. If dense body copy is required, generate the visual and add the copy later in a deterministic design tool.
- Specify reading order, alignment, relative size, and safe area rather than naming a font the service may not support.
- Verify every string character-for-character at delivery size. A visually similar glyph is a failure.

## Reference-image role contract

Use one row per reference. A reference may have more than one role only when those roles do not conflict.

```md
| Ref | Role | Must inherit | Must not inherit | Priority | Conflict rule |
|-----|------|--------------|------------------|----------|---------------|
| R1  |      |              |                  |          |               |
```

Useful roles include identity, product geometry, wardrobe, pose, composition, environment, lighting, palette, material, and typography layout.

Rules:

- Put identity and product truth above style and environment.
- State which people, objects, text, logos, backgrounds, or artifacts must not transfer from each reference.
- When two references conflict, resolve the conflict in the table before generating.
- Reduce the reference set or split the work into stages when roles cannot be separated cleanly.
- Use only references the user is authorized to use. Never infer consent from an accessible URL or file.

## Edit ledger

Use this after the first render or for an existing-image edit.

```md
| Round | Observed failure | Requested change | Frozen regions | Result |
|-------|------------------|------------------|----------------|--------|
| 1     |                  |                  |                |        |
```

Rules:

- Describe one failure class per round: text, identity, geometry, composition, lighting, or artifacts.
- Name frozen regions explicitly, such as “face, bottle silhouette, front label, and background gradient.”
- Do not restart from the original prompt when a good intermediate result exists.
- Stop when improvement stalls, the site changes accepted settings, or another generation would spend credits without a specific testable correction.

## Delivery QA

Record the target placement, pixel dimensions, crop, text readability, color/profile expectations, and required file format. Review at both full size and intended display size. Keep the unedited download as the source asset and save derived crops or overlays as separate files.
