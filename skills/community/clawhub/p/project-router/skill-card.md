## Description:

Project Router helps agents detect project context, manage local .project bundles, run standardized targets, manage artifacts, and expose the workflow through CLI or MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[safatinaztepe](https://clawhub.ai/user/safatinaztepe)

### License/Terms of Use:


## Use Case:

Developers and agents use Project Router to bootstrap project-local context bundles, read workspace context, run declared targets, manage artifact indexes, and switch between project or task context through CLI or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-defined targets can execute commands on the user's machine.

Mitigation: Use only in trusted repositories and inspect .project/targets.json before invoking target run or MCP target execution.

Risk: Apply workflows can write files into the local project bundle.

Mitigation: Inspect .project/history/plans/*.json before applying plans and keep generated apply receipts for audit.

Risk: The MCP server exposes tools that can run targets and apply project plans.

Mitigation: Avoid running the MCP server with sensitive environment variables until command confirmation, path containment, and bundled-CLI verification are in place.

## Reference(s):

- [Project Router ClawHub listing](https://clawhub.ai/safatinaztepe/skills/project-router)
- [safatinaztepe publisher profile](https://clawhub.ai/user/safatinaztepe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown and JSON text with CLI commands, MCP tool responses, project briefs, target lists, plans, and apply receipts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read project context and may write .project bundle files when apply workflows are invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
