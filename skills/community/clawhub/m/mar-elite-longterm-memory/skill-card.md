## Description:

Elite Longterm Memory helps AI coding agents preserve context with write-ahead session state, vector search, git-notes knowledge graphs, local memory archives, and optional SkillBoss cloud backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external AI agent users use this skill to set up durable working memory, semantic recall, decision logging, daily memory archives, and optional cloud-backed memory sync for coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages durable capture of conversation facts, preferences, decisions, and project context.

Mitigation: Use it only where persistent memory is intended, and regularly review or clear SESSION-STATE.md, MEMORY.md, daily logs, and vector memory.

Risk: Optional SkillBoss chat, embedding, and cloud backup features can send conversation or memory content to a third-party API.

Mitigation: Keep those features disabled for sensitive projects unless approved, scope SKILLBOSS_API_KEY carefully, and avoid storing the key in shell startup files unless necessary.

Risk: Automatic recall can inject stale, irrelevant, or overly broad memories into later agent work.

Mitigation: Apply memory hygiene, tune recall thresholds, disable automatic capture when appropriate, and review recalled context before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-elite-longterm-memory)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)
- [NPM package link from artifact README](https://www.npmjs.com/package/elite-longterm-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, JavaScript examples, and generated memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SkillBoss-backed features require SKILLBOSS_API_KEY; LanceDB recall depends on the memory-lancedb plugin.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
