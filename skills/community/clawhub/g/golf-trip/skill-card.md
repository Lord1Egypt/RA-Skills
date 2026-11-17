## Description:

Book flights for golf trips to world-class golf resorts and courses, with support for related travel planning tasks powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect golf-trip route parameters, run live flyai flight searches, and return bookable flight options in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global third-party flyai CLI package.

Mitigation: Require explicit approval before installation and use a pinned or reviewed CLI version where possible.

Risk: Travel-search details may be sent to the flyai or Fliggy service and exposed through provider booking links.

Mitigation: Confirm user intent before searches and share only the route, date, and booking details required for the request.

Risk: Broad activation language could route ordinary travel requests through provider booking flows.

Mitigation: Use narrower activation for intentional flight-search requests and ask clarifying questions when the trip intent is ambiguous.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown flight-search summaries with booking links, plus shell commands for flyai execution when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight options must come from live flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
