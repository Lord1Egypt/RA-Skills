## Description:

Amplitude (amplitude.com). Use this skill for any Amplitude request involving searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics teams can use this skill to search Amplitude events, review event segmentation, and inspect user activity through their connected Amplitude account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include executing a remote CLI installer, and the installer’s exact changes are not established by the bundled instructions.

Mitigation: Review and install the CLI separately from a verified release, and check which agent skills it installs or updates.

Risk: Connecting Amplitude entrusts OOMOL with credential handling and access to analytics data.

Mitigation: Review the connection and granted access before enabling the skill.

## Reference(s):

- [Amplitude API authentication documentation](https://amplitude.com/docs/apis/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Amplitude](https://amplitude.com)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-amplitude)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON data]

**Output Format:** [Structured Amplitude query results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Amplitude account and the selected query.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
