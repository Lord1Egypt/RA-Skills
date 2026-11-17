## Description:

Reads a user's Lose It! nutrition data and returns per-day summaries in JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve their own Lose It! food log summaries for nutrition tracking and agent workflows. Developers can use the per-day JSON output in downstream tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The config file can contain a plaintext Lose It! email and password.

Mitigation: Keep config.json private and out of shared or backed-up locations; use environment variables on shared machines.

Risk: The cached liauth token is a reusable session credential that can provide access to account data until it expires.

Mitigation: Protect the token and its containing directory with owner-only access, and keep it off shared disks and backups.

Risk: Some referenced files were unavailable to the security scan, which had medium overall confidence.

Mitigation: Review the release and its referenced files before installing, as advised by the scan guidance.

## Reference(s):

- [Lose It Nutrition on ClawHub](https://clawhub.ai/stozo04/skills/loseit-scan-pr16-2)
- [loseit-cli project](https://github.com/stozo04/loseit-cli)
- [Nutrition JSON contract](https://github.com/stozo04/loseit-cli/blob/main/docs/MACHINE_CONTRACT.md)
- [loseit-cli releases](https://github.com/stozo04/loseit-cli/releases)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands, Configuration guidance]

**Output Format:** [Per-day nutrition JSON; Markdown setup and usage instructions with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Nutrition fields and meal details depend on the selected days and the data available in the export.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
