## Description:

Use the Privacy CLI to create and manage Privacy Virtual Cards directly from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, list, pause, update, close, and inspect Privacy.com virtual cards and transactions through the Privacy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact financial actions against Privacy.com virtual cards.

Mitigation: Require manual user confirmation before creating, updating, pausing, unpausing, closing, or otherwise changing a card.

Risk: The skill can retrieve full PAN, CVV, and expiry data.

Mitigation: Avoid retrieving full card credentials through chat; when retrieval is necessary, require explicit user confirmation and do not log, save, or store the output.

Risk: Using a global latest npm install can introduce unreviewed CLI changes.

Mitigation: Install a pinned, reviewed Privacy CLI version in a contained environment.

Risk: The Privacy API key grants access to the user's Privacy.com account.

Mitigation: Use only a Privacy.com account and API key that the user intentionally allows the agent to access.

## Reference(s):

- [Privacy CLI documentation](https://developers.privacy.com/docs/privacy-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRIVACY_API_KEY and the privacy CLI; CLI commands should use --json for machine-readable output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
