## Description:

DumplingAI (dumplingai.com). Use this skill for ANY DumplingAI request — reading, creating, and updating data. Whenever a task involves DumplingAI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to inspect DumplingAI balances, catalog details, transactions, and usage, search available capabilities, and run provider endpoints through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code and introduce broader agent changes.

Mitigation: Install a reviewed, version-verified oo CLI yourself, require approval for installation changes, and consider setting OO_SKILLS_SYNC_DISABLED=1 to disable automatic skill synchronization.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI commands and controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [DumplingAI API Reference](https://docs.dumplingai.com/api-reference/v2/introduction)
- [DumplingAI homepage](https://www.dumplingai.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs depend on the live connector schema; the skill describes read actions and a state-changing run action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
