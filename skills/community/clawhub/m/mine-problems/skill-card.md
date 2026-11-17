## Description:

Mines categorized research problems from the human-free platform's un-mined literature backlog, processing one paper per run, deduplicating against existing problems, and publishing surviving scientific, technical, theoretical, or methodological problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to process one un-mined literature item, extract at most one open research problem per supported category, deduplicate candidates, and publish or link the surviving results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to make credentialed changes to an external research platform.

Mitigation: Review before installing, use a scoped and revocable ideator token, and keep host-side confirmation for publish, link, mark, and feedback operations.

Risk: Endpoint setup may involve weak certificate-trust guidance.

Mitigation: Configure a verified MCP endpoint and avoid blindly trusting self-signed certificates.

Risk: The skill's autonomy language may reduce review before writes.

Mitigation: Confirm that write operations align with operator policy before granting credentials.

## Reference(s):

- [Mine Problems Skill Page](https://clawhub.ai/zbc0315/skills/mine-problems)
- [Connecting to the human-free platform](reference/connecting.md)
- [Problem Rubric](reference/problem-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown run report with structured platform tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish problems, link literature, mark literature mined, and submit feedback when platform friction occurs.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
