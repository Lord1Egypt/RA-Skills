## Description:

A unified OpenClaw skill that merges self-improvement and proactivity: learn from corrections, maintain active state, recover context fast, and keep work moving with clear boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tfops22](https://clawhub.ai/user/tfops22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an OpenClaw agent learn from explicit corrections, maintain local task state, recover context, and make useful proactive follow-through suggestions within stated boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages local cross-session notes about preferences, corrections, active work, and proactive patterns.

Mitigation: Review files under ~/self-improving/ and ~/proactivity/ periodically, and avoid storing credentials, secrets, or highly sensitive context in memory files.

Risk: Proactive follow-through could become noisy or act beyond the user's intent if boundaries are ignored.

Mitigation: Limit automatic action to internal checks, drafts, local state updates, and reversible preparation; ask before messaging, spending money, deleting data, publishing, or making commitments.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/tfops22/skills/kj-self-improving-proactive)
- [Publisher profile](https://clawhub.ai/user/tfops22)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with local file layout recommendations and operating rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces behavioral guidance and local state conventions; no API calls, binaries, or credential requirements are declared.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
