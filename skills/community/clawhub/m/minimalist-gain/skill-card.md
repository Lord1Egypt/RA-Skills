## Description:

Report what minimalist actually measured in this session or project: LOC avoided, scope rejected, and dependencies declined.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyeshjayswal](https://clawhub.ai/user/divyeshjayswal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to report a project's minimalist savings from a persisted rejection ledger, including rejected scope, avoided LOC, and declined dependencies when supported by logged data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persisted project ledger may include rejected-scope entries from earlier sessions that contain private or unrelated details.

Mitigation: Review the ledger contents before sharing or publishing the report.

Risk: The lines-avoided total may be mistaken for a measured value even though the artifact describes it as the agent's estimate at logging time.

Mitigation: Keep the estimate label attached and avoid restating it as a hard measurement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/divyeshjayswal/skills/minimalist-gain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text report with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports logged measurements only; does not extrapolate cost or percentages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
