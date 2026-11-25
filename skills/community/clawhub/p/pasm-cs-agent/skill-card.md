## Description:

Builds customer-service agents that answer from a supplied knowledge base, escalate complaints to a human, and optionally use an LLM with knowledge-base fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-service developers use the agent to answer questions from their own FAQ or knowledge base, record unanswered questions, and route complaints to human staff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured LLM provider may receive knowledge-base content.

Mitigation: Exclude or redact sensitive information, or use a trusted local endpoint.

Risk: The security assessment is incomplete because some local references were unresolved.

Mitigation: Review unresolved local references and dependency behavior before deployment.

Risk: The HTTP gateway has no built-in session authentication when exposed externally.

Mitigation: Place the gateway behind an authenticated access layer managed by the deploying application.

Risk: The optional non-resistance safety gate can be unavailable with a missing or outdated dependency.

Mitigation: Check startup_report() and address its degrade_reason when relying on this safeguard.

## Reference(s):

- [Project repository](https://github.com/arronJack/pasm-agents)
- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-cs-agent)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Customer-facing text responses and JSON-serializable escalation context and agent snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are grounded in configured knowledge-base entries; an optional LLM may phrase responses when enabled.]

## Skill Version(s):

0.6.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
