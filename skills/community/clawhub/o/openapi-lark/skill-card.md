## Description:

Syncs OpenAPI or Swagger specifications from local files or runtime URLs into Feishu/Lark wiki and docx documentation trees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API teams use this skill to configure and run OpenAPI-to-Feishu/Lark documentation synchronization for single-service, multi-service, and CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote CLI code while using Lark or CI credentials.

Mitigation: Pin a reviewed source commit or package version, run with narrowly scoped Lark credentials, and keep unrelated CI secrets out of the environment.

Risk: Initialization can write persistent agent instructions into CLAUDE.md by default.

Mitigation: Review generated CLAUDE.md changes before committing, or use --no-claude-md when persistent agent instructions are not needed.

Risk: Synchronization and pruning can overwrite docs or move/delete wiki nodes.

Mitigation: Use a dedicated project wiki node, run dry-run before syncing, review zombie reports, and prefer prune: move over irreversible delete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/openapi-lark)
- [Server-resolved GitHub source](https://github.com/leeguooooo/openapi-lark)
- [Lark CLI](https://github.com/larksuite/cli)
- [Openapi Lark CI synchronization guidance](https://github.com/leeguooooo/openapi-lark#-%E5%9B%A2%E9%98%9F--ci-%E5%90%8C%E6%AD%A5%E6%8E%A8%E8%8D%90%E5%A7%BF%E5%8A%BF)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update project configuration, CLAUDE.md guidance blocks, local OpenAPI snapshots, cache/lock files, and Feishu/Lark wiki/docx content when commands are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
