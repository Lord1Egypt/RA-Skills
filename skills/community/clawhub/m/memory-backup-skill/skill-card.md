## Description: <br>
Lobster Memory Backup & Sync helps an agent save important conversation summaries to memory files, sync them across channels, and back them up to a configured private Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmww](https://clawhub.ai/user/nmww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve durable memory, migrate workflows across machines, and coordinate channel-specific context while controlling what is saved or pushed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation summaries and workflow notes can be persisted to files and pushed to a Git remote. <br>
Mitigation: Use a private repository, inspect the exact commit before pushing, and avoid storing secrets or raw credentials in memory files. <br>
Risk: Cross-channel sync can expose channel-specific context more broadly than intended. <br>
Mitigation: Require explicit confirmation of the source file and target scope before each save, sync, or push action. <br>
Risk: Workflow cleanup guidance can remove older files during migration. <br>
Mitigation: Prefer archive or dry-run migration steps before deleting old workflow files. <br>
Risk: Automated backup jobs can repeatedly push unreviewed memory changes. <br>
Mitigation: Keep scheduled backups disabled until the configuration has been tested and reviewed with a dedicated limited SSH key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nmww/memory-backup-skill) <br>
- [Memory structure reference](references/memory-structure.md) <br>
- [Backup setup guide](references/setup-guide.md) <br>
- [Workflow backup guide](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and generated memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can invoke shell scripts that commit and push selected memory files to a configured Git remote.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
