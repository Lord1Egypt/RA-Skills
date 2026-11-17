## Description:

Jasper Recall gives agents semantic memory search over indexed notes and session digests using ChromaDB and SkillBoss API Hub embeddings, with optional shared-memory and multi-agent recall workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Jasper Recall to let agents retrieve prior decisions, daily notes, and session summaries, and to share selected public memories across sandboxed or multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private agent memory can be exposed through recall results, autoRecall injection, or server access.

Mitigation: Use public-only mode for sandboxed agents, review autoRecall configuration before enabling it, keep the server bound to localhost, and do not enable private recall on shared hosts.

Risk: Memory content used for embeddings may be sent to the SkillBoss embedding API.

Mitigation: Index only memory that is acceptable to send to SkillBoss and run privacy checks before syncing or sharing memory.

Risk: The security evidence reports unsafe server and command execution paths.

Mitigation: Avoid private server access until those issues are fixed, review commands before execution, and prefer pinned package and dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/jasper-recall-2)
- [GitHub repository](https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall)
- [npm package](https://www.npmjs.com/package/jasper-recall)
- [SkillBoss listing](https://skillboss.co/skills/jasper-recall)
- [Multi-Agent Mesh](docs/MULTI-AGENT-MESH.md)
- [Shared Memory Spec](docs/SHARED-MEMORY-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text, Markdown, JSON, and shell command output depending on the command or integration path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some outputs depend on local memory files, ChromaDB collections, configured environment variables, and SkillBoss embedding API access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
