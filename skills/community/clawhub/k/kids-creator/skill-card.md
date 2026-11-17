## Description:

Kids Creator guides facilitators through a Korean-language, Telegram-based AI workshop where children create personalized, playable HTML games with text, button, and voice inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ico1036](https://clawhub.ai/user/ico1036)

### License/Terms of Use:

MIT-0

## Use Case:

External facilitators and workshop operators use this skill to run a child-focused AI game creation session, manage safe prompt flows, and produce each participant's playable game and sharing materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles and publishes children's identifiable content with insufficient privacy controls.

Mitigation: Require guardian or operator consent, minimize and pseudonymize stored data, define deletion and revocation rules, and protect gallery and game links before use with real children.

Risk: Deployment behavior may expose generated child-specific games or prompts through public gallery links or broad repository updates.

Mitigation: Avoid raw prompts in public displays, review allowlisted files before publishing, and replace broad Git staging with reviewed file selection.

Risk: Operational dependencies and deployment commands can change the public site during a live workshop.

Mitigation: Pin deployment dependencies, pre-test Cloudflare deployment, and keep the documented direct HTML file fallback available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ico1036/skills/kids-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JSON, shell commands, and single-file HTML game requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram interaction copy, workshop state structure, deployment steps, gallery and QR link guidance, and playable HTML game specifications.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
