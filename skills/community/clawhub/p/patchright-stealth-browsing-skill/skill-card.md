## Description:

Perform stealth browser automation to bypass bot detection (Cloudflare, Akamai, Datadome) using Patchright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide OpenClaw agents through authorized stealth browser automation on protected websites, including navigation, interaction, session reuse, screenshots, and blocker-page handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is explicitly framed around bypassing anti-bot protections.

Mitigation: Use only on sites and accounts where the operator has clear authorization, and review the skill carefully before installation.

Risk: Session cookie storage and reuse can expose authenticated access.

Mitigation: Avoid storing or reusing cookies unless necessary, and clear session state after use.

Risk: Video recording may capture sensitive page content or credentials.

Mitigation: Disable video recording by default and treat recorded files as sensitive artifacts.

Risk: Proxy routing can expose authenticated traffic to untrusted infrastructure.

Mitigation: Do not route authenticated traffic through untrusted proxies.

## Reference(s):

- [Patchright Stealth Browsing on ClawHub](https://clawhub.ai/cyber-bye/skills/patchright-stealth-browsing-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions for MCP tool selection and browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and a configured patchright-mcp server exposing patchright_navigation, patchright_interaction, patchright_session, and patchright_execution.]

## Skill Version(s):

2.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
