## Description:

Track laundry loads, view usage stats, and export reports in multiple formats. Use when logging wash cycles, reviewing patterns, exporting schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home operators use this skill to log laundry activity, track household inventory and maintenance notes, review recent history and usage statistics, and export laundry records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Laundry and household entries are stored locally and may be included in exports.

Mitigation: Avoid entering sensitive personal details and review exported files before sharing them.

Risk: CSV exports can carry spreadsheet-opening risks if entries include formula-like content.

Mitigation: Inspect CSV exports before opening them in spreadsheet software, especially on shared or managed machines.

Risk: Local records under ~/.local/share/laundry may be visible to other users on shared systems depending on file permissions.

Mitigation: Review local file permissions and machine access controls before storing household records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/laundry)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command suggestions and guidance for a local shell-based laundry tracker; exports may be JSON, CSV, or plain text.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
