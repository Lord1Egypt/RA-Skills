## Description: <br>
Compile turns raw markdown notes from a configured inbox into structured knowledge-transfer documents, then archives the original material with reversible links and checkpointed audit state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arroncn993-sys](https://clawhub.ai/user/arroncn993-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators and developers use this skill to turn local markdown inbox items into curated knowledge-transfer documents with duplicate checks, generated frontmatter, archiving, backlinks, checkpoints, and a final audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, archive, and rewrite files inside the configured markdown vault. <br>
Mitigation: Configure inbox, transit, raw, and state directories narrowly; keep backups or a dry-run process before production use. <br>
Risk: A free-form shell audit command may run during the workflow. <br>
Mitigation: Review any --audit-cmd value before execution and install only when the publisher is trusted. <br>
Risk: Misconfigured paths could affect the wrong local notes or vault content. <br>
Mitigation: Set COMPILE_INBOX_DIR explicitly and verify vault-related environment variables before running the workflow. <br>


## Reference(s): <br>
- [Compile Skill on ClawHub](https://clawhub.ai/arroncn993-sys/openclaw-compile-skill) <br>
- [Workflow](references/workflow.md) <br>
- [Compile Template](references/compile-template.md) <br>
- [Frontmatter Specification](references/frontmatter-spec.md) <br>
- [Self-Check Checklist](references/self-check-checklist.md) <br>
- [Title Rules](references/title-rules.md) <br>
- [Error Playbook](references/error-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents with YAML frontmatter, local file updates, checkpoint records, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured local markdown vault and basic shell tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
