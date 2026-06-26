# Material Bundle

When a user has scattered assets, prefer one zip bundle over many pasted fragments.

Default bundle shape:

```text
project-materials/
├── 01-brief/
├── 02-data-proof/
├── 03-brand-assets/
├── 04-reference-decks/
└── 05-visual-assets/
```

## Folder Intent

- `01-brief/`
Project brief, meeting notes, target audience, deck goal, rough outline.

- `02-data-proof/`
Spreadsheets, screenshots, metrics, tables, survey results, research notes, quotes.

- `03-brand-assets/`
Logo, color guide, fonts, template screenshots, brand rules.

- `04-reference-decks/`
Old PPTs, competitor decks, examples of tone or structure.

- `05-visual-assets/`
Photos, product renders, UI screenshots, diagrams, and generated visuals.

## Intake Rule

If the user already has many files, ask for the zip once, not piecemeal.

If the user has no organized materials, accept a rough dump and create the missing structure during intake.

If implementation tooling later ingests a material bundle, it should accept either a folder or a zip file.

If repeatability matters, AI-generated visuals should be saved into `05-visual-assets/generated/` before export.
