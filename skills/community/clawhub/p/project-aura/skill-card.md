## Description:

Project Aura adds seven emotional personality modules and adaptive feedback-based phrase selection to AI companion interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryanchen3777](https://clawhub.ai/user/bryanchen3777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Project Aura to add emotional phrase selection, feedback-tuned ratings, combo responses, and local JSON persistence to AI companion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce intimate or romantic AI companion preset phrases that may be inappropriate for some deployments.

Mitigation: Install it only for agents where that companion style is intended, and review phrase libraries before use.

Risk: Local phrase and feedback data can contain private user-created content.

Mitigation: Keep green_tea_modules.json private, avoid storing secrets in phrases or feedback, and delete or edit the file to reset learned ratings and counts.

## Reference(s):

- [Project Aura on ClawHub](https://clawhub.ai/bryanchen3777/skills/project-aura)
- [Publisher Profile](https://clawhub.ai/user/bryanchen3777)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON persistence for phrase counts, ratings, and cooldown timestamps.]

## Skill Version(s):

1.8.0 (source: server release evidence and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
