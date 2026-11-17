## Description:

Use this skill to build academic-style .docx papers with formal citation styles, numbered equations, figure and table cross-references, footnotes or endnotes, bibliography formatting, and optional multi-column journal layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-generation agents use this skill to create academic .docx manuscripts, journal or conference papers, and thesis chapters with venue-aware citation, equation, bibliography, figure, table, and layout conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include direct execution of downloaded installer scripts.

Mitigation: Review the installer before running it, or prefer a verifiable, version-pinned OfficeCLI release.

Risk: Document validation can miss academic-style defects such as unresolved citations, stale figure or table numbers, and equations rendered as plain text.

Mitigation: Run the skill's citation, SEQ-field, and visual-preview checks before delivering the final .docx.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iceyliu/skills/officecli-academic-paper)
- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with OfficeCLI shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation and validation of a single academic .docx output.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
