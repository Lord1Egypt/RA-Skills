## Description:

MaskClaw is an on-device privacy guard skill suite that detects and masks sensitive UI content, monitors agent behavior, and evolves privacy rules from user feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theodora-y](https://clawhub.ai/user/theodora-y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use MaskClaw to add a privacy-protection layer between cloud agents and phone or desktop UI workflows. It supports sensitive-content masking, behavior monitoring, and user-specific privacy rule evolution for agent-operated interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive behavior records and correction values may be stored while the skill monitors agent actions.

Mitigation: Use controlled deployment, remove raw previews and correction values from logs, and add retention, deletion, and encryption controls before processing real user data.

Risk: The skill can automatically generate and publish persistent user skills from model output.

Mitigation: Disable or gate automatic publishing and review generated rules in a sandbox before deployment.

Risk: The privacy guard depends on local model access and file-path handling.

Mitigation: Restrict MiniCPM access to a trusted local endpoint and fix path validation before using the skill with real user data.

## Reference(s):

- [MaskClaw ClawHub Skill Page](https://clawhub.ai/theodora-y/skills/maskclaw)
- [Project Homepage](https://github.com/your-org/maskclaw)
- [Architecture](references/ARCHITECTURE.md)
- [Skills API](references/SKILLS_API.md)
- [RAG Schema](references/RAG_SCHEMA.md)
- [Prompt Templates](references/PROMPT_TEMPLATES.md)
- [Self Evolution](references/SELF_EVOLUTION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, JSON API responses, and generated SOP or rule files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce masked image file paths, behavior log records, and generated privacy-rule skill drafts when used in an agent workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
