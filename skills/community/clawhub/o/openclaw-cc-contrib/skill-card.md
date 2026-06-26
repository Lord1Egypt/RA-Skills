## Description: <br>
Openclaw Cc Contrib is an OpenClaw skill collection for extracting, organizing, and consolidating local conversation memories, with an additional code simplification review workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jofiction918](https://clawhub.ai/user/jofiction918) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill collection to preserve useful conversation context in local memory files, review and consolidate those memories, and generate structured code simplification proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically store conversation details in durable local memory files. <br>
Mitigation: Avoid discussing secrets, credentials, private journal details, or sensitive project data in conversations that may be summarized, and review memory/topics and MEMORY.md regularly. <br>
Risk: The memory consolidation workflows can rewrite or delete memory files with limited review controls. <br>
Mitigation: Enable automatic extraction or dream-rem cron only after reviewing the behavior, keep backups before consolidation, and inspect proposed changes before accepting memory-sorting actions. <br>
Risk: Code simplification reports are proposals and may contain incorrect or misleading guidance. <br>
Mitigation: Review each proposal against the current codebase before making code changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jofiction918/openclaw-cc-contrib) <br>
- [README](artifact/README.md) <br>
- [Simplify prompt template](artifact/simplify/references/prompt-template.md) <br>
- [OpenClaw](https://openclaw.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses plus local Markdown, YAML, and JSON memory files and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or edits memory/topics/, MEMORY.md, and heartbeat-state.json when memory workflows are enabled; simplify outputs review proposals without directly changing code.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
