## Description:

Searches the web and selected workspace content with bounded, source-labeled results for research and fact-finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyeque](https://clawhub.ai/user/iyeque)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can find current web information or locate content in workspace memory and skills, then inspect source-labeled results before using them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web queries sent to Tavily may disclose confidential or proprietary information.

Mitigation: Enable network search only for approved, non-sensitive queries.

Risk: Local search can read workspace memory and skills content.

Mitigation: Enable local search only when access to those folders is appropriate.

Risk: Web results may be inaccurate or misleading.

Mitigation: Verify important claims against their sources before relying on them.

## Reference(s):

- [Unified Web Search on ClawHub](https://clawhub.ai/iyeque/skills/iyeque-unified-web-search)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 50 source-labeled results with titles, scores, and content or snippets; URLs when available, with warnings reported separately.]

## Skill Version(s):

1.3.2 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
