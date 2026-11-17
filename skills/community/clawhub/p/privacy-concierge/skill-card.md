## Description:

Personal AI assistant that monitors online privacy exposure, supports data broker opt-outs and DSAR tracking, scans for new exposures or breaches, and offers privacy advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlielila](https://clawhub.ai/user/charlielila)

### License/Terms of Use:


## Use Case:

External users use this agent to monitor personal privacy exposure, request data broker removals, track deletion requests, and receive privacy guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to handle very sensitive personal information and the evidence says sensitive personal-data flows are under-disclosed.

Mitigation: Require explicit consent, review, retention, and deletion controls before enabling workflows that collect, store, or act on personal information.

Risk: The evidence identifies an undeclared unrestricted local file read tool.

Mitigation: Remove the local file read tool or strictly sandbox it before installation.

Risk: The skill may send opt-out or deletion requests externally on a user's behalf.

Mitigation: Require user review and approval before any outbound opt-out, deletion, or DSAR request is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlielila/skills/privacy-concierge)
- [Publisher profile](https://clawhub.ai/user/charlielila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privacy scores, opt-out status, exposure alerts, DSAR request guidance, and source-backed privacy answers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
