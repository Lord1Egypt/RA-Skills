## Description:

Lovefromio Elite Longterm Memory helps AI agents preserve context with write-ahead logging, vector search, git-notes, file archives, and optional cloud memory integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure durable memory for coding and assistant agents, including session state files, curated memory logs, semantic recall, and optional third-party memory services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent memory can retain sensitive user context longer than intended.

Mitigation: Use the skill only with explicit memory expectations, review generated memory files regularly, and delete stale or sensitive entries.

Risk: Silent automatic capture can store preferences, decisions, or facts without clear user consent.

Mitigation: Disable silent auto-capture unless explicitly wanted and prefer opt-in memory writes for sensitive workflows.

Risk: Optional Mem0 or SuperMemory integrations can send conversation content to third-party services.

Mitigation: Redact sensitive content, avoid uploading full conversations without consent, and configure third-party API use according to the deployment privacy policy.

Risk: Unpinned package versions can change memory behavior or dependency exposure over time.

Mitigation: Pin package versions and review dependency updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-elite-longterm-memory)
- [Publisher profile](https://clawhub.ai/user/lovefromio)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [NPM package](https://www.npmjs.com/package/elite-longterm-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files such as SESSION-STATE.md, MEMORY.md, and memory/YYYY-MM-DD.md when its CLI is used.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata; artifact frontmatter reports 1.2.1 and package.json reports 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
