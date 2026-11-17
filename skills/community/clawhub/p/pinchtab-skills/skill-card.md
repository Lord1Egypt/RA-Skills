## Description:

Controls local headless or headed Chrome through the PinchTab HTTP API for browser automation, crawling, form filling, navigation, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellotombruce](https://clawhub.ai/user/hellotombruce)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to control a local Chrome browser, inspect page state, interact with elements, capture screenshots or PDFs, and extract text through CLI commands or the PinchTab HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent browser control can expose authenticated sites or saved browser state when a persisted Chrome profile is used.

Mitigation: Use a fresh dedicated PinchTab profile and avoid daily or password-filled Chrome profiles.

Risk: Network exposure of the PinchTab API could allow unintended browser control.

Mitigation: Keep the API bound to 127.0.0.1 and set BRIDGE_TOKEN before any network exposure.

Risk: Screenshots, snapshots, raw text, and eval output may contain sensitive page data.

Mitigation: Treat these outputs as sensitive data and limit retention and sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hellotombruce/skills/pinchtab-skills)
- [PinchTab API Reference](artifact/references/api.md)
- [Environment Variables Reference](artifact/references/env.md)
- [Profile Management](artifact/references/profiles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, HTTP examples, configuration notes, and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser navigation steps, HTTP request examples, screenshot and PDF export guidance, and operational precautions for local browser control.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
