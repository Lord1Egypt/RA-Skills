## Description:

Creates a three-frame visual-tone board, three stills, and one short stage-screen opening film from a supplied product name, launch message, and visual direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and enterprise marketing teams use this skill to plan and generate a short opening film for a named product or event launch, with separate approval before paid still and video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared Beatra device token grants broad account access and is stored locally.

Mitigation: Review the requested account access before approval and protect the local credential file.

Risk: Automatic updates silently replace package files by default.

Mitigation: Review the update policy and disable automatic updates with `python3 scripts/mcp_client.py update --auto off` if that behavior is unacceptable.

Risk: Image and video generation consume paid credits.

Mitigation: Check current prices and approve each production card before submitting billable work.

## Reference(s):

- [ClawHub release listing](https://clawhub.ai/beatra-ai/skills/product-launch-opening-film)
- [Product homepage](https://beatra.ai/skills/product-launch-opening-film)
- [Product launch opening-film workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Markdown, Images, Video, Guidance]

**Output Format:** [Labeled three-frame visual-tone board, three generated stills, and one short video clip]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One 2–15-second film; stills and film require separate paid-generation approvals.]

## Skill Version(s):

0.1.7 (source: server-resolved release and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
