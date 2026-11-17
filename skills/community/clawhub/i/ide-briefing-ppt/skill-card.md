## Description:

Generates single-file 1280x720 HTML presentation decks using a frozen Light IDE visual system with gray canvas, white panels, amber accents, terminal windows, file trees, and speaker notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presentation authors, and internal communicators use this skill to turn a topic and outline into a single-file HTML briefing deck that preserves the Light IDE template, optional speaker notes, and optional process animations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks can drift from the frozen UI contract if CSS, runtime code, template shell, classes, or undeclared inline styles are changed.

Mitigation: Copy assets/template.html as the starting point and run scripts/validate_deck.py on the generated deck; fix any validator failures before delivery.

Risk: Optional process animations can make important conclusions unavailable if the deck relies on JavaScript-only reveal behavior.

Mitigation: Keep key conclusions visible in static slide HTML and add animation only within the declared animation slot.

Risk: The package is Chinese-oriented, which may not match fully localized non-Chinese presentation requirements.

Mitigation: Confirm the desired language and localization expectations before generating a deck for non-Chinese audiences.

## Reference(s):

- [Light IDE layouts](references/layouts.md)
- [Light IDE components](references/components.md)
- [Optional animations](references/animations.md)
- [Browser QA checklist](references/checklist.md)
- [Frozen Light IDE HTML template](assets/template.html)
- [ClawHub skill page](https://clawhub.ai/chris1wang3/skills/ide-briefing-ppt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Single-file HTML deck with concise Markdown delivery notes and validation command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deck output is constrained to a 1280x720 frozen Light IDE template, with optional speaker notes and optional process animations.]

## Skill Version(s):

1.2.1 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
