## Description:

Plans and generates hanzi recognition-card stills from user-supplied character lists and confirmed text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and content creators use this skill to plan consistent Chinese-character recognition cards from confirmed characters and optional user-supplied pinyin, glosses, or visual references. After approval, it can submit the planned stills to Beatra's image service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authorization permits unrelated media and voice operations and is shared across Beatra skills.

Mitigation: Review the full authorization before connecting and prefer narrower permissions where available.

Risk: Malformed installation records may cause the removal helper to disconnect other Beatra skills.

Mitigation: Verify the installation record and uninstall behavior before removal; avoid proceeding with malformed records, and use the Beatra Console to review or revoke device access.

Risk: Installation analytics may be collected, and optional reference files are uploaded to Beatra.

Mitigation: Consider the analytics disclosure and upload only references you intend to share.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/hanzi-card-set)
- [Hanzi card pack workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)

## Skill Output:

**Output Type(s):** [Images, Text]

**Output Format:** [Still-image character cards and a labeled text pack plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A consistent shared card look; usually one still per named character or group, with no more than eight stills by default.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
