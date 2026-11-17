## Description:

Use this skill for any QuickChart request, including reading, creating, and updating data through QuickChart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the OOMOL-connected oo CLI to build QuickChart chart and QR code URLs, or create a short chart URL. The skill guides agents to inspect each action's schema before submitting its payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run an unchecked online installer without a separate prompt.

Mitigation: Install a verified CLI release yourself, review any skills it adds, and prevent automatic installer execution.

Risk: Chart and QR payloads are sent through OOMOL.

Mitigation: Exclude secrets and approve the exact content before submission.

## Reference(s):

- [QuickChart](https://quickchart.io)
- [QuickChart API documentation](https://quickchart.io/documentation/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [URLs, JSON, Guidance]

**Output Format:** [Text and JSON responses containing QuickChart URLs and action metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
