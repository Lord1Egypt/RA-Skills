## Description:

OpenWeb gives agents typed JSON access to more than 90 real websites for search, shopping, travel, finance, social, news, and developer workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imoonkey](https://clawhub.ai/user/imoonkey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use OpenWeb to inspect available site operations, execute read and permitted write actions through the openweb CLI, and add or expand site coverage when an operation is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate through logged-in browser sessions across many sites.

Mitigation: Use a dedicated low-privilege browser profile or test accounts, and avoid finance or primary personal accounts.

Risk: Write, delete, or transaction-like operations can affect user accounts or external services.

Mitigation: Keep write and delete permissions at prompt or deny, and leave transaction actions denied unless explicitly reviewed.

Risk: Capture folders, temporary output files, and token caches can contain sensitive account data.

Mitigation: Treat these files as secrets and remove or protect them after use.

## Reference(s):

- [OpenWeb homepage](https://getopenweb.com)
- [OpenWeb repository](https://github.com/openweb-org/openweb)
- [CLI Reference](references/cli.md)
- [Troubleshooting](references/troubleshooting.md)
- [x-openweb Schema](references/x-openweb.md)
- [ClawHub skill page](https://clawhub.ai/imoonkey/skills/openweb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON operation results, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large CLI responses may spill to a temporary file; browser-backed operations may require a logged-in browser session.]

## Skill Version(s):

0.1.5 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
