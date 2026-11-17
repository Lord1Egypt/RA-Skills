## Description:

Use when running Outlit CLI commands, setting up Outlit for AI agents, authenticating with Outlit, querying customer data from the terminal, or troubleshooting Outlit CLI issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafa-thayto](https://clawhub.ai/user/rafa-thayto)

### License/Terms of Use:


## Use Case:

Developers, operators, and customer-facing teams use this skill to install, authenticate, configure, and run Outlit CLI commands for customer intelligence, customer search, SQL analytics, and agent setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of a CLI that accesses customer records and analytics.

Mitigation: Review authorization before running customer, search, or SQL commands, and limit or redact sensitive output.

Risk: Broad agent setup can configure all detected agents when run with automatic confirmation.

Mitigation: Avoid broad setup with automatic confirmation unless all detected agents should be configured.

Risk: Installing an unpinned global CLI can expose users to unexpected version changes.

Mitigation: Prefer a pinned, trusted @outlit/cli version before installing or updating.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafa-thayto/skills/outlit-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-output guidance for piped Outlit CLI commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
