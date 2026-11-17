## Description:

Integrate Paddle payments with subscriptions, webhooks, checkout, and tax compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to integrate Paddle for SaaS payments, including API calls, checkout setup, subscription lifecycle handling, webhook verification, and tax compliance configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers high-impact billing operations such as creating customers and changing subscriptions against a live Paddle account.

Mitigation: Require explicit user confirmation before creating customers or changing subscriptions, and prefer sandbox endpoints until the user is ready for production.

Risk: API keys and integration details could be mishandled in local Paddle memory.

Mitigation: Keep API keys out of ~/paddle/memory.md and store only environment, product, tech stack, price ID, and decision notes.

Risk: Webhook verification examples are under-scoped for a payments workflow.

Mitigation: Replace examples with hardened code that checks timestamp freshness, validates signature format, handles malformed input safely, and minimizes webhook payload logging.

## Reference(s):

- [Paddle ClawHub skill page](https://clawhub.ai/ivangdavila/skills/paddle)
- [Paddle skill homepage](https://clawic.com/skills/paddle)
- [Paddle production API endpoint](https://api.paddle.com)
- [Paddle sandbox API endpoint](https://sandbox-api.paddle.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Paddle API request examples, webhook handler examples, and local integration memory guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
