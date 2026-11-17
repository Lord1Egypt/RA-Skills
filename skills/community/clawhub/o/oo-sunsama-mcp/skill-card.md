## Description:

Connects an agent to Sunsama through OOMOL's MCP connector to read and manage planning data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who plan work in Sunsama can use an agent to read and manage tasks, calendar events, channels, objectives, and other planning data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses downloaded oo CLI installers that are unverified in the supplied evidence.

Mitigation: Verify the CLI release before installing it or enabling the skill.

Risk: The oo CLI can add persistent skills to other agents during startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if you do not want startup skill synchronization.

Risk: Connecting Sunsama grants OOMOL-mediated access to the connected account.

Mitigation: Connect only an account whose access you intend to authorize through OOMOL.

Risk: Write and destructive actions can change or remove Sunsama data.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval before destructive actions.

## Reference(s):

- [Sunsama MCP documentation](https://help.sunsama.com/docs/integrations/mcp/)
- [oo CLI controls for startup skill synchronization](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-sunsama-mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Guidance]

**Output Format:** [JSON connector requests and responses; Markdown notes and help content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Sunsama data; write and destructive actions can change or remove data.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
