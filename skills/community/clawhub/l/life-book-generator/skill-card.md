## Description:

Creates paid Life Book full-report Agent tasks, checks payment and generation status, and retrieves the generated 18-chapter report through the official Agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to collect Life Book intake data, create a paid full-report task, handle payment state, poll task progress, and retrieve the completed report inside an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit sensitive personal intake data, including birth information, life history, relationship details, financial context, and current personal questions.

Mitigation: Run it only after explicit user consent and tell the user what data will be sent and to which operator-approved endpoint.

Risk: The skill uses bearer credentials and task tokens for paid task creation and report retrieval.

Mitigation: Store API keys and task tokens in a protected secret mechanism and avoid passing them directly on command lines or exposing them to end users.

Risk: The Life Book base URL is configurable and could point to an untrusted or plaintext HTTP endpoint.

Mitigation: Configure only an operator-approved HTTPS endpoint before running health checks, task creation, payment confirmation, or result retrieval.

Risk: The workflow can initiate paid task creation or payment-confirmation steps.

Mitigation: Confirm the user understands the paid workflow before creating a report task or submitting payment confirmation, and rely only on official API status for payment and readiness.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xcii/skills/life-book-generator)
- [Life Book Service Endpoint](https://www.elife369.site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, bearer-token handling instructions, payment status, polling status, endpoint URLs, and final report content when the official API returns it.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
