## Description: <br>
Hook Guard adds a three-level safety layer for agents by requiring confirmation for dangerous operations, backing up important changes, and logging routine activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Hook Guard to add operation-level guardrails around file edits, shell commands, external messages, and production-sensitive actions. The skill helps classify actions as confirmation-required, backup-required, or routine audit-log events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic or always-on activation could unexpectedly change how unrelated agent tasks are handled. <br>
Mitigation: Review trigger phrases and automatic mode settings before installation; prefer explicit opt-in or visible guard status when enabling broad coverage. <br>
Risk: Backups and audit logs may retain file paths or copies of modified files longer than intended. <br>
Mitigation: Review backup and audit-log retention settings, restrict access to the guard storage directory, and avoid recording file contents in logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wavmson/hook-guard) <br>
- [Hook Guard README](artifact/README.md) <br>
- [Hook Guard skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, confirmation prompts, backup notices, and audit summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trigger phrases, Red/Yellow/Green action classifications, backup retention guidance, and audit-log reporting behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
