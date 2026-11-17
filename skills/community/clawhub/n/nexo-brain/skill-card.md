## Description:

Runtime core for NEXO Desktop. Provides local memory, Deep Sleep, Evolution support-ticket mode, skills, watchdog, and MCP tools for the desktop product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wazionapps](https://clawhub.ai/user/wazionapps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to install and configure the NEXO Desktop runtime core, including its local memory, watchdog, session, follow-up, and MCP tool support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow asks users to execute an unpinned npm package that can install a persistent local MCP runtime.

Mitigation: Install only a trusted, reviewed version of nexo-brain and verify what creates ~/.nexo/server.py before enabling the runtime in OpenClaw.

Risk: The runtime maintains local memory across sessions.

Mitigation: Review the contents and retention behavior under ~/.nexo and avoid enabling the runtime for workflows where persistent local memory is not acceptable.

## Reference(s):

- [NEXO Desktop homepage](https://nexo-desktop.com)
- [nexo-brain npm package](https://www.npmjs.com/package/nexo-brain)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install guidance for npm, OpenClaw MCP configuration, and local runtime usage notes.]

## Skill Version(s):

7.38.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
