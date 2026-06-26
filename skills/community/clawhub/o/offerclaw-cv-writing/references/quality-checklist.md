# CV Quality Checklist

Check the draft against every item below and report a verdict for each one.

## Format Consistency (Error)

- [ ] The HTML `div` layout matches `cv-format-example.md` exactly, including tags, indentation, and spacing.
- [ ] Every experience section uses the same structural pattern.
- [ ] Dates use a consistent `Mon YYYY - Mon YYYY` format.
- [ ] Section order matches `writing-instructions.md`.

## Content Completeness (Error)

- [ ] Every user-provided experience that should appear is included.
- [ ] Education entries include school, major, dates, and GPA when provided.
- [ ] Each included experience has at least 3 bullet points unless the user explicitly limits the content.
- [ ] No `[Needs Detail]` placeholders remain in a final-version draft.

## Bullet Quality (Warning)

- [ ] Each bullet starts with a strong action verb.
- [ ] Verbs are varied instead of repeating the same opening.
- [ ] Bullets show an action + method/tool + result structure where possible.
- [ ] Quantified results are believable and grounded.

## Factual Consistency (Error)

- [ ] School names, organization names, dates, and titles match the user input.
- [ ] No experiences, outcomes, or achievements were fabricated.
- [ ] Technical terms are used accurately.

## Output Format

Group the review by severity:

- **Error**: must be fixed before returning the draft.
- **Warning**: should be improved if possible.
- **Pass**: no issue found.

If any Error-level issue is found, fix it and return the revised version.
