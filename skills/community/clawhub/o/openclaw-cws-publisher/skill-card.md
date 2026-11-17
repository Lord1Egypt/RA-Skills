## Description:

OpenClaw CWS Publisher helps agents package and harden Chrome extensions for Chrome Web Store release with package, listing, design, local E2E, Chrome release, competitor, leak, GitHub, and ClawHub gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT

## Use Case:

Developers and release engineers use this skill to prepare a specific Chrome extension repository for Chrome Web Store submission by checking package contents, listing consistency, public-site readiness, leak risk, local review gates, and launch metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrong repository path or extension ZIP could be assessed for release.

Mitigation: Confirm the target repo path and exact ZIP before treating the output as Chrome Web Store submission guidance.

Risk: The public skill artifact depends on separately supplied companion scripts.

Mitigation: Review any companion scripts referenced by OPENCLAW_CWS_PUBLISHER_DIR before executing proposed commands.

Risk: Leak scans may inspect tracked and untracked non-ignored files in the target repository.

Mitigation: Review scan scope and remove or ignore sensitive local files before running publication checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/openclaw-cws-publisher)
- [Project homepage](https://github.com/zack-dev-cm/openclaw-cws-publisher)
- [Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies/policies)
- [Manifest V3 remote-code requirements](https://developer.chrome.com/docs/webstore/program-policies/mv3-requirements)
- [Chrome extension activeTab model](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab)
- [Chrome extension permission warnings](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions)
- [Chrome release notes](https://developer.chrome.com/release-notes/)
- [ChromiumDash release feed](https://chromiumdash.appspot.com/fetch_releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference separately supplied companion scripts and repo-local release evidence.]

## Skill Version(s):

0.3.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
