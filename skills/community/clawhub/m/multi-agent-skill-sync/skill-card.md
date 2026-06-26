## Description: <br>
One source of truth for local AI agent skills: audit Codex, Claude, OpenClaw, OpenCode, workspace skills, and shared roots; score hygiene, diff conflicting installs, deduplicate into one canonical source, and migrate the same layout across machines with restorable backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donttal](https://clawhub.ai/user/donttal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Skill Sync to audit local AI-agent skill installations across multiple host roots, compare conflicting copies, preview deduplication or root-adoption plans, and apply reversible convergence when the plan is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applied dedupe, import, or adopt-root commands can reorganize local AI-agent skill directories. <br>
Mitigation: Run preview commands first, inspect the planned replacements, and use --apply only after confirming the affected paths. <br>
Risk: Forced installation or convergence can replace existing local skill folders. <br>
Mitigation: Avoid --force and applied operations until the target roots are correct, and keep the backup directory available for restore. <br>


## Reference(s): <br>
- [Skill Sync on ClawHub](https://clawhub.ai/donttal/multi-agent-skill-sync) <br>
- [Compatibility Model](references/compatibility.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce preview plans, diffs, export/import manifests, symlink operations, and restore instructions depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
