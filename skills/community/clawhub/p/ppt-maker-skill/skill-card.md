## Description:

Generates structured PPT decks from a topic, Markdown, or existing draft, supports natural-language slide and component edits, renders HTML previews, and exports editable PPTX files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-q526](https://clawhub.ai/user/mr-q526)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, preview, edit, validate, and export structured presentation decks for business briefings, lessons, personal introductions, project introductions, customer stories, and similar presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malicious or attacker-influenced deck.json content can inject script into generated previews.

Mitigation: Open previews only for trusted decks and reference materials until preview escaping is fixed.

Risk: Deck image references can point to local files outside the project.

Mitigation: Keep image references contained to trusted project or materials directories and avoid externally influenced deck files until path containment is fixed.

Risk: Sensitive presentation materials may be processed by local scripts and dependencies.

Mitigation: Update dependencies and use explicit invocation for sensitive documents.

## Reference(s):

- [Slide Schema](references/slide-schema.md)
- [Layout Rules](references/layout-rules.md)
- [Template Catalog](references/template-catalog.md)
- [Prompt Patterns](references/prompt-patterns.md)
- [PPT Maker Skill Page](https://clawhub.ai/mr-q526/skills/ppt-maker-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON deck files, HTML previews, structured edit plans, and PPTX exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; generated decks use deck.json as the source of truth and can be validated, previewed, edited, and exported through bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
