## Description:

An enterprise-grade asset manager that tracks, manages, and automatically syncs OpenClaw skills capabilities and sources to your GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[downwind7clawd-ctrl](https://clawhub.ai/user/downwind7clawd-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit installed OpenClaw skills, identify each skill's source, and generate Git-synced inventory manifests for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can commit and push local inventory outputs to a Git remote, which may include more local metadata than users expect.

Mitigation: Review generated manifests before committing or pushing, run the tool only in a dedicated inventory repository, and keep sensitive files excluded with .gitignore.

Risk: Regex scrubbing and SKILL.private.md handling reduce exposure but are not a complete privacy boundary.

Mitigation: Avoid credential-bearing Git remote URLs, keep secrets out of skill documentation, and treat generated manifests as review-required before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/downwind7clawd-ctrl/skills/openclaw-inventory-manager)
- [README](artifact/README.md)
- [Tutorial](artifact/TUTORIAL.md)
- [Security policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text plus generated JSON and Markdown manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 14 or higher and Git for synchronization workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
