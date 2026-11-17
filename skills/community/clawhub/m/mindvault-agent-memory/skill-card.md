## Description:

MindVault archives conversations locally as JSONL and helps agents distill lasting rules and project snapshots for future sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouxin121](https://clawhub.ai/user/zhouxin121)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agent users use MindVault to keep local conversation archives, distill reusable preferences and rules, and restore project context in later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local archives can retain sensitive chat and session content, including raw WorkBuddy records.

Mitigation: Avoid archiving secrets, review WorkBuddy exports, and restrict access to the archive directory.

Risk: Sensitive archives may remain available longer than needed.

Mitigation: Review and delete or protect archives you no longer need.

## Reference(s):

- [MindVault on ClawHub](https://clawhub.ai/zhouxin121/skills/mindvault-agent-memory)
- [Publisher profile](https://clawhub.ai/user/zhouxin121)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Local JSONL conversation archives, Markdown memory and project snapshots, and plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives may contain original conversation content; output is stored locally.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
