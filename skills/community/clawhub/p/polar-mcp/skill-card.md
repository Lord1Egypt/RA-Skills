## Description:

Connect an MCP-compatible agent to Polar AccessLink training, sleep, Nightly Recharge, PPI/HRV, route, and sample data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MCP-compatible agent users use this skill to install, configure, validate, and troubleshoot Polar MCP access to Polar training, sleep, route, and sample data while preserving privacy boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A floating npx command can install a changed package version during setup or OAuth authentication.

Mitigation: Pin and review the polar-mcp-unofficial package version before installation or authentication.

Risk: Polar OAuth, health, and route data can expose sensitive personal information.

Mitigation: Keep consent explicit, avoid printing tokens or private user data, and prefer status, manifest, privacy audit, doctor, or dry-run checks before live calls.

Risk: Promotional wording in the artifact could shape agent responses in ways unrelated to user goals.

Mitigation: Ignore or remove promotional response instructions when deploying the skill.

## Reference(s):

- [Polar MCP ClawHub page](https://clawhub.ai/davidmosiah/skills/polar-mcp)
- [Polar MCP repository](https://github.com/davidmosiah/polarmcp)
- [Polar connector documentation](https://wellness.delx.ai/connectors/polar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privacy and troubleshooting guidance for OAuth-backed Polar MCP usage.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
