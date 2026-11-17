## Description:

Nex Onboarding helps agency operators manage client onboarding workflows from contract through go-live with local checklists, progress tracking, blocked-step handling, statistics, templates, and JSON or CSV exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External agency operators, web agencies, design studios, and service providers use this skill to start, track, update, pause, complete, and report on client onboarding work. It is designed for structured onboarding across administrative, technical, design, content, communication, delivery, and QA steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored onboarding records may contain client contact details or project notes in a local SQLite database.

Mitigation: Protect ~/.nex-onboarding like business records and avoid storing unnecessary sensitive client data in onboarding notes.

Risk: CSV exports may be opened in spreadsheet software when data includes untrusted client-provided text.

Mitigation: Prefer JSON for untrusted data or sanitize CSV exports before opening them in spreadsheet tools.

Risk: Setup creates local files under ~/.nex-onboarding and ~/.local/bin.

Mitigation: Install only on machines where creating those local files and command wrappers is acceptable.

## Reference(s):

- [Nex Onboarding README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/nexaiguy/skills/nex-onboarding)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; CLI output as plain text, JSON, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite persistence under ~/.nex-onboarding and can write JSON or CSV export files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, release evidence, lib/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
