## Description:

Turns supplied insurance policy clauses and authorized still images into short spoken explanation clips, one clip per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance advisors and wealth educators use this skill to make short, separate talking clips from policy clauses and still images they are authorized to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Beatra grants generation and spending authority beyond this insurance workflow.

Mitigation: Review account access before connecting, approve each paid stage, and monitor credits.

Risk: A shared device token is stored locally for the connected account.

Mitigation: Protect the local credential and revoke the device in the Beatra Console when access is no longer trusted.

Risk: The bundled client may install verified updates silently.

Mitigation: Disable automatic updates if unattended package changes are unacceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/insurance-clause-talking)
- [Beatra skill overview](https://beatra.ai/skills/insurance-clause-talking)
- [Clause talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Video clips, Audio narration, Markdown guidance]

**Output Format:** [Separate 2–15-second clips and a written delivery summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip per still; reports available media details and actual credits charged.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata and package manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
