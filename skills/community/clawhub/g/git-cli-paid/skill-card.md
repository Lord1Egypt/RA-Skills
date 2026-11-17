## Description: <br>
Git Cli Paid helps agents automate Git workflows, run repository diagnostics, generate workflow guidance, troubleshoot failures, and coordinate batch operations across multiple repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to automate routine Git operations, diagnose repository health, apply workflow templates, troubleshoot Git failures, and manage batches of repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad read, write, and shell execution authority for Git automation. <br>
Mitigation: Install it only where Git automation is intended, review proposed commands before execution, and run it with the narrowest repository and filesystem scope available. <br>
Risk: Automated sync, cleanup, push, branch deletion, tagging, credential changes, and multi-repository operations can change repositories or credentials in ways that are difficult to undo. <br>
Mitigation: Require explicit confirmation for those actions, prefer dry runs, keep backups or recoverable remotes, and avoid global credential storage unless the impact is understood. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include repository status summaries, diagnostic recommendations, workflow templates, automation scripts, troubleshooting steps, and structured result objects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
