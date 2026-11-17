## Description:

Google Workspace Bridge for Gmail, Drive, Sheets, and Calendar via a local API at http://127.0.0.1:8787.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spinzerus](https://clawhub.ai/user/spinzerus)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Gmail, search Drive, read or update Sheets, and list or create Calendar events through a local Google Workspace bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Google Workspace mail, files, sheets, and calendar data through a local bridge.

Mitigation: Review before installing and use only with a trusted local bridge.

Risk: A non-local bridge endpoint or exposed bridge secret could expand access beyond the intended local setup.

Mitigation: Avoid setting GMAIL_BRIDGE_URL to non-local destinations and rotate BRIDGE_SECRET if it may have been exposed.

Risk: Write and create operations can modify Google Sheets or Calendar data.

Mitigation: Require explicit user approval before running write or create operations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/spinzerus/skills/gmail-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text summaries with inline shell commands and JSON responses from the local bridge]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; may use BRIDGE_SECRET and GMAIL_BRIDGE_URL environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
