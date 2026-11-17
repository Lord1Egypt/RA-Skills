## Description:

Nasdaq Data Link (data.nasdaq.com). Use this skill for ANY Nasdaq Data Link request — searching and reading data. Whenever a task involves Nasdaq Data Link, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search Nasdaq Data Link and retrieve dataset metadata, table rows, quotes, dividend history, and analyst ratings through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installers and may make persistent agent changes without clear user approval or disclosure.

Mitigation: Review setup before enabling the skill; install a verified, pinned oo release under your control and review or disable bundled-skill synchronization.

Risk: Authenticated requests through OOMOL may incur credit charges.

Mitigation: Review OOMOL credit usage and billing before running requests.

## Reference(s):

- [Nasdaq Data Link](https://data.nasdaq.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON data returned through oo CLI commands, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The real-time quote action is an alias that returns end-of-day quotes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
