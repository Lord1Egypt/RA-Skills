## Description:

Use Skyvern to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Skyvern account use this skill to start, inspect, and cancel browser automation runs through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or synchronizing the oo CLI can execute unreviewed remote code or make persistent changes to other agent skills.

Mitigation: Review the install and sync behavior, use a reviewed pinned CLI version, and inspect any skill changes before accepting them.

Risk: Browser task payloads and run cancellations can change or interrupt activity in the connected Skyvern account.

Mitigation: Confirm the exact task payload and cancellation target before running those actions.

Risk: OOMOL intermediates Skyvern account access, while the remote installer and live connector behavior are not included in the release artifact.

Mitigation: Use the connection only for intended Skyvern tasks and review the pinned CLI and account permissions before connecting.

## Reference(s):

- [Skyvern](https://www.skyvern.com)
- [Skyvern API Quickstart](https://www.skyvern.com/docs/developers/getting-started/quickstart)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub Skyvern release](https://clawhub.ai/oomol/skills/oo-skyvern)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Shell commands, JSON results, and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
