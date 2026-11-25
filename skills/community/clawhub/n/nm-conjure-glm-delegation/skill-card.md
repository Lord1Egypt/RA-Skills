## Description:

Delegates tasks to Z.ai GLM-5.x via the stock claude binary and an endpoint swap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with the shared delegation workflow to send coding and other tasks to Z.ai GLM through Claude Code, including tasks that benefit from a large context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The delegation workflow may send local documents to an external model without a privacy warning.

Mitigation: Review which files will be transmitted and avoid sending confidential documents or secrets unless sharing is authorized; check the executor's filtering and consent controls before use.

## Reference(s):

- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code]

**Output Format:** [Task-dependent text or Markdown, including code when requested; results may be saved as a dated Markdown file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The content depends on the delegated task.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
