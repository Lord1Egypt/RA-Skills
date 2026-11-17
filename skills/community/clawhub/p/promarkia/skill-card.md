## Description:

Helps OpenClaw users inspect Promarkia capabilities and connections, submit a specifically approved marketing run, and retrieve its results and artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dominiclachance](https://clawhub.ai/user/dominiclachance)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and marketing teams use this skill to inspect approved Promarkia squads and connections, request a single approved marketing task, and review run status, artifacts, and action receipts. It does not provide recurring automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts sent to Promarkia may expose sensitive information and consume credits.

Mitigation: Obtain approval for the exact run and credit use; remove secrets, private files, and unrelated personal data before submission.

Risk: Publishing or outreach through connected accounts can create unintended external effects.

Mitigation: Confirm the exact action, destination, audience, connected account ID, and provider receipt; use draft-only mode when no external action is intended.

Risk: A timed-out local request may leave a remote run active, making a retry costly or duplicative.

Mitigation: Retrieve the original run ID and check its status before starting another run.

## Reference(s):

- [Promarkia external API contract v2](references/api-contract-v2.md)
- [Promarkia](https://www.promarkia.com)
- [Promarkia skill on ClawHub](https://clawhub.ai/dominiclachance/skills/promarkia)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Marketing drafts and guidance, with structured run status, artifact metadata, and action receipts when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One approved run per submission; outputs and artifacts depend on the selected squad and server capabilities.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata, artifact README and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
