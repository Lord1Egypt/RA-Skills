## Description:

Guides agents through creating, reading, editing, formatting, and quality-checking Microsoft Word .docx files with OfficeCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document automation agents, and external users use this skill to produce, inspect, and revise .docx documents with structured Word features such as headings, tables, fields, comments, headers, footers, and tables of contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can execute a remote installer directly in a shell.

Mitigation: Use a pinned OfficeCLI release with checksums or signatures, or another integrity-verified install path, before enabling the skill.

Risk: Invoking the skill outside actual .docx or Microsoft Word tasks can expose users to unnecessary tool installation and document mutation risk.

Mitigation: Use the skill only for .docx or Microsoft Word workflows, and validate generated or modified documents before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iceyliu/skills/officecli-docx)
- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and DOCX quality checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural guidance for OfficeCLI-driven .docx work; generated documents require validation and visual review before delivery.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
