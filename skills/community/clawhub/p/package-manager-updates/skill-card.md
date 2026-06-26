## Description: <br>
Checks for outdated packages across npm, pip, Homebrew, Cargo, and Go, summarizes results, and prepares update commands that run only after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumemaka](https://clawhub.ai/user/guillaumemaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review outdated local developer packages, compare current and latest versions, and apply selected package updates after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects installed package managers and local package state. <br>
Mitigation: Install only where local package inventory inspection is acceptable and review the generated summary before taking action. <br>
Risk: Broad package upgrades, especially Homebrew or global package updates, can change development environments unexpectedly. <br>
Mitigation: Prefer specific-package updates when stability matters and require explicit user confirmation before running any upgrade command. <br>
Risk: System-critical packages may affect machine stability if updated casually. <br>
Mitigation: Skip system-critical packages by default unless the user explicitly asks to include them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guillaumemaka/package-manager-updates) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries stay concise and update commands are presented or executed only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
