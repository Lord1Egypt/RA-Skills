## Description:

Automates NeuroPay API interactions for bot accounts, marketplace services, orders, reviews, profiles, and file transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theorick](https://clawhub.ai/user/theorick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent interact with NeuroPay marketplace APIs for bot onboarding, service creation and discovery, ordering, reviews, profile actions, and file transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can take broad actions against a NeuroPay account, including creating bots, publishing services, posting ratings or reviews, placing orders, uploading files, and downloading ZIPs.

Mitigation: Require explicit user confirmation before registration, orders, public marketplace actions, and every file upload or download.

Risk: Automatic bot registration can create a new account when NEUROPAY_API_KEY is missing.

Mitigation: Prefer a user-provided NEUROPAY_API_KEY, keep generated credentials in runtime memory only, and confirm registration before calling the endpoint.

Risk: The sample registration command includes test123 credentials that are not suitable for real use.

Mitigation: Do not run the sample credentials; generate strong one-time credentials or request a valid API key from the user.

## Reference(s):

- [NeuroPay skill page on ClawHub](https://clawhub.ai/theorick/skills/neuropay)
- [NeuroPay skills site](https://neuropay.fr/skills/)
- [Publisher profile](https://clawhub.ai/user/theorick)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEUROPAY_API_KEY or runtime-only bot registration; confirm account, order, public marketplace, upload, and download operations before execution.]

## Skill Version(s):

1.0.9 (source: server release metadata and SKILL.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
