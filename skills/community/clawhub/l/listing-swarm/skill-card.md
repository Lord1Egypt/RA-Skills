## Description:

Listing Swarm helps agents submit an AI product to 70+ AI directories by automating form filling, BYOK captcha solving, optional BYOK IMAP email verification, and submission tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyw00d](https://clawhub.ai/user/heyw00d)

### License/Terms of Use:


## Use Case:

External developers, founders, and product teams use this skill to submit AI product listings across directory websites while keeping humans involved for account creation, payments, failed captchas, and other blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional IMAP access can expose email content and credentials if a personal inbox is used.

Mitigation: Use a dedicated submission email account with an app password and revoke it after the campaign if no longer needed.

Risk: Captcha solving requires a user-provided paid API key.

Mitigation: Use a dedicated, low-balance CAPTCHA account and keep the key in runtime environment variables only.

Risk: Product and contact details are submitted to many third-party directory websites.

Mitigation: Review the directory list and product configuration before running, and submit only information intended for public listing.

Risk: Some directory targets may require payment, account creation, or terms-of-service review.

Mitigation: Keep human approval in the loop for paid listings, account creation, failed captchas, and any non-HTTPS or otherwise unexpected target.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heyw00d/skills/listing-swarm)
- [LinkSwarm skill page](https://linkswarm.ai/skill/)
- [Security documentation](SECURITY.md)
- [Complete documentation](DOCS.md)
- [2Captcha](https://2captcha.com)
- [Anti-Captcha](https://anti-captcha.com)
- [CapSolver](https://capsolver.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets; submission tracking is stored as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided product information and optional environment variables for captcha solving and IMAP verification.]

## Skill Version(s):

1.0.3 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
