## Description:

Read itch.io creator stats and publish or update itch.io game builds from Windows using the itch.io server-side API and Butler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game creators use this skill to inspect itch.io account and game stats, validate an itch.io API key, install Butler on Windows, and publish local game builds to confirmed itch.io project channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An itch.io API key is needed for account access and publishing.

Mitigation: Use a limited or rotated API key where possible, avoid verbose logging, and do not paste API keys back into chat unless explicitly requested.

Risk: A live Butler push can publish or update a build on the wrong itch.io target.

Mitigation: Confirm the exact source path and target channel, and perform a dry-run before live upload for new projects or channels.

Risk: Butler is downloaded during setup.

Mitigation: Verify Butler from an official source when stronger supply-chain assurance is required.

## Reference(s):

- [itch.io server-side API endpoint](https://itch.io/api/1/$key)
- [Butler Windows archive endpoint](https://broth.itch.zone/butler/windows-amd64/LATEST/archive/default)
- [ClawHub skill page](https://clawhub.ai/stanestane/skills/itch-io-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command blocks and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API responses summarized as JSON when reading itch.io account or game statistics.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
