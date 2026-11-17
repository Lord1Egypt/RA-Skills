## Description:

Use Open Connect's shared cloud-browser controls and verification service for authorized remote browser tasks across AI clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use the skill to operate shared browser sessions and coordinate supported verification workflows for authorized browser tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification tasks can incur metered charges, and retrying an uncertain submission can create a duplicate paid task.

Mitigation: Use only an owned solver key with authorized spending; when a submission is uncertain, inspect the existing attempt and reuse its request ID for a retry.

Risk: A verification proof may be rejected or applied to a page or widget that has changed.

Mitigation: Apply a ready proof only to its matching browser reference, origin, and original widget, then inspect the original page; use human handoff for unresolved challenges and authentication steps.

## Reference(s):

- [Open Connect Global Browser release page](https://clawhub.ai/hillstreet-ph/skills/open-connect-global-browser)
- [2Captcha](https://2captcha.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Natural-language browser workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for browser and verification tool use; no files are produced.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
