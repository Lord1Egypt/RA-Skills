## Description:

Manage SaaS Custom Domains accounts, upstreams, and custom domains through the OOMOL-connected oo CLI, including listing, retrieval, creation, deletion, DNS verification, and cache purging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to manage upstreams and custom domains in their connected SaaS Custom Domains account. It can retrieve and list resources, create or delete them, trigger DNS verification, and purge a domain's HTTP cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says the required helper can add and update other agent skills, while this skill does not explain or control those lasting changes.

Mitigation: Review the specific CLI release before use, disable automatic skill synchronization for each invocation with OO_SKILLS_SYNC_DISABLED=1, and inspect the command reference.

Risk: The remote CLI installers and deployed connector implementation have not been verified, and OOMOL holds the connected API key server-side.

Mitigation: Review and install a specific CLI release yourself, consider the connected-key custody, and approve exact change or deletion targets before execution.

## Reference(s):

- [SaaS Custom Domains](https://saascustomdomains.com)
- [SaaS Custom Domains API authentication documentation](https://docs.saascustomdomains.com/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require the oo CLI and a connected account. The skill identifies state-changing and destructive actions for user confirmation.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
