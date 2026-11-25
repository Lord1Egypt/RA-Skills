## Description:

Checks store readiness of Android, iOS and Flutter apps for Google Play and the App Store: target API level, Data safety, sensitive permissions, account deletion, Play App Signing, privacy manifest and required-reason APIs, App Review rejections, ATT, TestFlight, versioning, staged and phased rollout, crash gates and rollback. Use before submitting a build, for a store rejection, or to plan a release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Mobile app developers and release engineers use this skill to assess Android, iOS, and Flutter builds against Google Play and App Store readiness requirements, investigate store rejections, and plan staged rollouts with stop conditions and a rollback path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes reported capabilities for production uploads and iOS submissions, and scanner coverage is incomplete.

Mitigation: Confirm those release actions are intended and require explicit authorization before any production upload or App Store submission.

Risk: Store requirements and thresholds can change after the dates checked in the skill's references.

Mitigation: Re-check current official store guidance before relying on a date or threshold for a release decision.

## Reference(s):

- [Google Play release readiness](artifact/references/google-play.md)
- [App Store release readiness](artifact/references/app-store.md)
- [Versioning and rollout](artifact/references/versioning-and-rollout.md)
- [ClawHub mobile-release page](https://clawhub.ai/ahmadhussain0335/skills/mobile-release)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration guidance, Shell commands, Code examples]

**Output Format:** [Markdown release-readiness report with evidence, blockers, rollout guidance, and optional code or command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Readiness items are marked Pass, Fail, N/A, or Not verified with evidence and an owner for console-only checks.]

## Skill Version(s):

1.0.1 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
