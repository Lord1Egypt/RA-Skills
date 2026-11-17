## Description:

Autonomous GitHub and multi-platform bounty hunter that scans for high-value issues, filters by skills and ROI, submits proposals, and tracks payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronmda](https://clawhub.ai/user/aaronmda)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to identify bounty opportunities, draft proposals or pull requests, and track bounty-related submissions and payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may operate repeatedly in the background and interact with GitHub or bounty platforms on the user's behalf.

Mitigation: Run it only with monitoring and a documented disable path; avoid cron or heartbeat operation unless those controls are in place.

Risk: Generated proposals or pull requests may be submitted without clear user approval or limits.

Mitigation: Require explicit approval before any submission or pull request is sent.

Risk: Bounty and payment workflows may expose account, token, or wallet access.

Mitigation: Use narrowly scoped tokens and keep financial or wallet access read-only where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronmda/skills/julia-bounty-scout)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with generated proposal, pull request, tracking, and operational guidance content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve repeated platform interactions and user-approved submissions.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
