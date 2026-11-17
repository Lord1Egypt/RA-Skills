## Description:

Bootstrap a new OpenClaw automation project from a plain-language description through workflow reasoning, flowchart confirmation, node configuration, and scaffold generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcking](https://clawhub.ai/user/lcking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to turn a new workflow idea into an OpenClaw project scaffold, including a Mermaid flowchart, node configuration, runtime files, scripts, Telegram routing, and cron registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill grants persistent OpenClaw authority and handles credentials too broadly for automatic installation.

Mitigation: Review scripts before installation, run the bootstrap script with --plan first, do not pass real bot tokens on the command line, and patch or remove broad auth-profile copying before live use.

Risk: The security guidance flags project key validation and cron administration as areas requiring care.

Mitigation: Add strict project_key validation before writing workspace files, use --cron-list before any removal, and avoid --cron-remove unless intentional admin-level cron control is required.

## Reference(s):

- [Project Factory README](artifact/README.md)
- [Flow Design Language](artifact/references/flow_design_language.md)
- [Content Pipeline Shared Architecture](artifact/references/architecture.md)
- [Project Onboarding Checklist](artifact/references/onboarding_checklist.md)
- [Shared Routing Group Schema](artifact/references/shared_routing_group_schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration drafts, Mermaid flowcharts, shell commands, and generated project scaffold files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write project files and register routing or cron configuration when its scripts are run outside preview mode.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
