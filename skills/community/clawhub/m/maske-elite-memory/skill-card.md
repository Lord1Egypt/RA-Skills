## Description:

终极AI智能体记忆系统。WAL协议 + 向量搜索 + git-notes + 云备份。6层记忆架构：热RAM(SESSION-STATE)、温存储(LanceDB向量)、冷存储(Git-Notes知识图)、精选档案(MEMORY.md)、云备份(SuperMemory)、自动提取(Mem0)。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent working memory, curated Markdown archives, semantic recall, git-notes decision history, and optional cloud-backed memory flows to AI agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain broad user and project context, including sensitive information if an agent records it.

Mitigation: Define what may be stored, avoid secrets and regulated data, and review generated SESSION-STATE.md, MEMORY.md, and memory logs before sharing or committing a workspace.

Risk: Optional SuperMemory and Mem0 integrations can send memory content to third-party services when API keys are configured.

Mitigation: Keep cloud and Mem0 features disabled unless third-party processing is intended and approved for the workspace data.

Risk: Maintenance commands include deletion of local vector memory directories.

Mitigation: Back up memory files and confirm target paths before running deletion commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/skills/maske-elite-memory)
- [ClawHub publisher profile](https://clawhub.ai/user/skillforge-jojo)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact-declared npm package](https://www.npmjs.com/package/elite-longterm-memory)
- [Artifact-declared GitHub repository](https://github.com/NextFrontierBuilds/elite-longterm-memory)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated workspace memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initializes SESSION-STATE.md, MEMORY.md, and dated memory logs; optional cloud and Mem0 integrations require explicit API keys.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter; artifact package.json lists 1.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
