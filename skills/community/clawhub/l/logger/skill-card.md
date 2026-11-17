## Description:

Google Sheets Log Automation. Use when the user wants to append log entries, record audit trails, or automate event logging to a pre-configured Google Sheet (PortEden Secure access).

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to append event, audit, error, and task log rows to a configured Google Sheet through the PortEden CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Log rows may contain secrets, credentials, personal data, internal prompts, or sensitive stack traces.

Mitigation: Redact sensitive content before appending logs to the Google Sheet.

Risk: The skill sends log data to an external Google Sheet through PortEden CLI credentials.

Mitigation: Use a limited-scope token, confirm the connected Google account, and verify the target PE_SHEET_ID before logging.

Risk: Installing an unreviewed latest CLI version can change behavior outside the skill artifact.

Mitigation: Prefer a pinned or otherwise verified PortEden CLI release from a trusted installation path.

## Reference(s):

- [PortEden homepage](https://porteden.com)
- [ClawHub skill page](https://clawhub.ai/porteden/skills/logger)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with shell command examples and compact JSON CLI output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PortEden CLI commands and PE_API_KEY or keyring credentials with PE_SHEET_ID for the target spreadsheet.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
