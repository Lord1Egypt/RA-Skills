## Description:

Generates Upwork and freelance bid materials from a job description, including a proposal draft, bid-worthiness score, pricing suggestion, milestone split, and follow-up messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeterwang](https://clawhub.ai/user/jeterwang)

### License/Terms of Use:


## Use Case:

Freelancers and proposal-writing agents use this skill to evaluate whether to bid on a job description and produce copy-paste-ready proposal, pricing, milestone, and follow-up materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an exposed billing API key.

Mitigation: Remove the key from the artifact, rotate it before release, and use a documented secret-management path.

Risk: The release evidence reports an under-scoped external charging flow.

Mitigation: Document the billing endpoint and transmitted fields, and require explicit user confirmation before each paid charge.

Risk: The release evidence reports broken JavaScript and paid/free command logic issues.

Mitigation: Repair the syntax error and verify that preview, scoring, pricing, follow-up, and paid generation commands enforce the documented billing behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeterwang/skills/proposal-copilot)
- [Publisher profile](https://clawhub.ai/user/jeterwang)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON containing proposal text, scoring, pricing, milestones, and follow-up copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bid decision labels, numeric score components, pricing suggestions, and paid/free command behavior.]

## Skill Version(s):

2.0.0 (source: server release metadata and module export)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
