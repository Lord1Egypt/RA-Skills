## Description:

Configure and operate oh-my-openagent (OmO), the OpenCode plugin that adds multi-agent orchestration, skills, hooks, MCPs, and multi-provider model routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kolyanberoks-23loud](https://clawhub.ai/user/kolyanberoks-23loud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate the oh-my-openagent OpenCode plugin, including agent setup, task categories, model routing, hooks, slash commands, MCPs, and provider authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a mutable third-party plugin package can change the code an agent runs locally.

Mitigation: Install only from a trusted source and pin a reviewed version instead of using `latest`.

Risk: Broad local agent authority, background agents, autonomous loops, hooks, and MCPs may perform actions beyond the user's immediate prompt.

Mitigation: Disable unnecessary background agents, hooks, loops, and MCPs; run the plugin in a sandboxed or least-privilege environment.

Risk: Provider authentication uses local credential files, including `auth.json`.

Mitigation: Avoid opening, sharing, or pasting credential files and review provider access before enabling model routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kolyanberoks-23loud/skills/oh-my-openagent)
- [oh-my-openagent repository](https://github.com/code-yeongyu/oh-my-openagent)
- [Configuration schema](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json)
- [Agents reference](references/agents.md)
- [Categories reference](references/categories.md)
- [Configuration reference](references/configuration.md)
- [Hooks reference](references/hooks.md)
- [MCPs reference](references/mcps.md)
- [Providers reference](references/providers.md)
- [Tools reference](references/tools.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration snippets, command examples, and operational recommendations for local OpenCode setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
