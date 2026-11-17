## Description:

Builds, ships, and debugs native iOS apps: lifecycle, permissions, entitlements, push, widgets, StoreKit, and App Store review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose and implement native iOS platform behavior across lifecycle, permissions, entitlements, background execution, notifications, widgets, StoreKit, privacy, performance, crashes, accessibility, localization, and App Store review issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory may record app, device, project, client, release, and subscription details without a separate opt-in step.

Mitigation: Review or restrict access to ~/Clawic/data before installation and keep only non-secret identifiers and operational notes in those files.

Risk: Legacy-directory migration or shared-record updates could alter local notes that other workflows rely on.

Mitigation: Require explicit confirmation before migrations or shared-record updates, and review the exact paths and records named by the skill before changes are applied.

Risk: Generated iOS guidance may include commands or changes that affect device, simulator, keychain, entitlement, or release state.

Mitigation: Review proposed commands and require confirmation for destructive actions such as simulator resets, keychain deletion, lossy migrations, or release-impacting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/ios)
- [Clawic iOS skill homepage](https://clawic.com/skills/ios)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file updates under configured Clawic data paths and should require explicit confirmation before destructive device, simulator, keychain, or migration actions.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
