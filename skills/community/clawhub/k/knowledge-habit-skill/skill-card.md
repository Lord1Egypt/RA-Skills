## Description:

A privacy-first, offline-first knowledge work habit tracker that helps users focus on one active habit, record work events and timed sessions, generate node candidates, and run Web, Electron desktop, and Android overlay modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to install and run a local habit tracking app for recording focus time, knowledge work events, and JSON backups while keeping habit data on the user's device by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can fetch mutable external Node/Electron code that was not bundled for review.

Mitigation: Install only after reviewing the target repository, pinning a trusted release or commit, and verifying a checksum or signature when available.

Risk: npm install scripts and fallback install paths may execute code under the user's account.

Mitigation: Review npm dependencies and lifecycle scripts before installation, and run setup in a constrained local environment when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/puppetcat-fire/skills/knowledge-habit-skill)
- [Dragon Palace Knowledge Hub](https://github.com/puppetcat-fire/dragon-palace-knowledge-hub)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON backup data produced by the installed local application]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and bash; the installer may fetch external Node/Electron application code during setup.]

## Skill Version(s):

1.0.9 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
