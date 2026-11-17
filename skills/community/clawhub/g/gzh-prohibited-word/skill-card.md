## Description:

Checks WeChat Official Account copy from text, documents, images, or webpages for potentially prohibited or sensitive wording and suggests alternatives; when service credits are insufficient, its workflow can initiate a payment-assisted recharge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and marketing teams use the skill to review WeChat Official Account drafts before publication, identify potentially risky wording, and assess suggested alternatives. Its suggestions are editorial aids and do not replace legal or platform review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content is sent to RedFox for checking, and rewritten copies may be saved locally.

Mitigation: Get authorization before sending sensitive copy, avoid submitting confidential content, and review or remove locally saved output after use.

Risk: Insufficient-credit handling can install or use a separate payment tool and act on returned payment details.

Mitigation: Require explicit approval of the recipient and amount for each recharge, validate the checkout destination, safely pass response values to commands, and separately approve and pin payment-tool installation.

Risk: Credential lookup may involve shell configuration files.

Mitigation: Set REDFOX_API_KEY through an environment variable rather than relying on shell-file credential lookup, and do not expose the key in submitted content or logs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/if530770/skills/gzh-prohibited-word)
- [RedFoxHub service](https://redfox.hk/?source=clawhub)
- [Core workflow](references/core_workflow.md)
- [Recharge workflow and safeguards](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown with marked matches, replacement suggestions, and revised copy; optional plain-text file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts pasted text, supported documents, images for text extraction, and webpages. Detection results are not a guarantee of legal or platform compliance.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
