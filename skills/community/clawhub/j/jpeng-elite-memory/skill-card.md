## Description: <br>
Ultimate AI agent memory system for Cursor, Claude, ChatGPT, and Copilot using write-ahead logging, vector search, git-notes, and optional cloud backup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up durable memory files, daily logs, semantic recall, git-notes storage, and optional external memory sync so agents can retain project context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages durable memory about work and conversations, which can retain credentials, personal data, sensitive project details, or stale context. <br>
Mitigation: Set explicit rules prohibiting storage of secrets and sensitive data, and regularly review and prune SESSION-STATE.md, MEMORY.md, daily logs, Git notes, and vector memory. <br>
Risk: Optional Mem0 or SuperMemory use can send selected conversation-derived data to third-party providers. <br>
Mitigation: Enable external sync only after confirming user consent, provider terms, and the data categories allowed for export. <br>
Risk: Silent persistence of decisions or preferences can make incorrect or outdated context influence later agent behavior. <br>
Mitigation: Require periodic memory hygiene, mark uncertain entries clearly, and prefer curated summaries over unreviewed raw conversation capture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-elite-memory) <br>
- [NPM package](https://www.npmjs.com/package/elite-longterm-memory) <br>
- [GitHub repository](https://github.com/NextFrontierBuilds/elite-longterm-memory) <br>
- [bulletproof-memory](https://clawdhub.com/skills/bulletproof-memory) <br>
- [lancedb-memory](https://clawdhub.com/skills/lancedb-memory) <br>
- [git-notes-memory](https://clawdhub.com/skills/git-notes-memory) <br>
- [supermemory](https://clawdhub.com/skills/supermemory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and JSON code blocks; the CLI can create Markdown memory files in the workspace.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY for configured vector search; SUPERMEMORY_API_KEY and MEM0_API_KEY are optional for external memory services.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence, SKILL.md frontmatter, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
