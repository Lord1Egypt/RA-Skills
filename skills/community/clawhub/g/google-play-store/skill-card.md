## Description:

Publish, optimize, and scale Android apps on Google Play with release automation, ASO, policy compliance, and rejection recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and release managers use this skill to prepare, publish, optimize, and troubleshoot Android app releases on Google Play. It helps agents provide checklists, rollout guidance, ASO advice, policy compliance review, rejection recovery steps, and Fastlane-oriented automation examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep local notes about app names, package identifiers, release status, and workflow preferences under ~/google-play-store/.

Mitigation: Use the memory folder only for non-secret app and workflow notes, keep it appropriately protected, and never store API keys, tokens, service-account JSON, keystores, or passwords there.

Risk: Fastlane and CI/CD snippets are examples that may handle release credentials or generated secret files if adapted directly.

Mitigation: Harden examples before use by pinning dependencies, protecting CI secrets, limiting service-account permissions, and cleaning up decoded secret files.

Risk: Track promotion or production rollout commands can affect live app availability and users.

Mitigation: Review rollout percentage, target track, versionCode, and policy readiness before running commands; prefer staged rollouts with monitoring gates.

Risk: Trying to bypass Google enforcement with additional developer accounts can lead to broader account termination.

Mitigation: Resolve policy issues through documented fixes and appeals instead of creating accounts to evade enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/google-play-store)
- [Skill homepage](https://clawic.com/skills/google-play-store)
- [Setup](artifact/setup.md)
- [Release tracks and rollouts](artifact/tracks.md)
- [App Store Optimization](artifact/aso.md)
- [Policy compliance](artifact/policies.md)
- [Rejection recovery](artifact/rejections.md)
- [Fastlane automation](artifact/fastlane.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with checklists, tables, shell commands, configuration snippets, and release workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local note structures under ~/google-play-store/ and Fastlane or CI examples for the user to review and run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
