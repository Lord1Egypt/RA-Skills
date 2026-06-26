## Description: <br>
Auto-fix security vulnerabilities in OpenClaw skills by generating remediations for hardcoded secrets, shell injection risks, prompt injection, path traversal issues, secure code replacements, and environment variable templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to remediate security findings in OpenClaw skills, inspect generated fixes, create environment variable templates, and produce fix reports before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security fixer can rewrite local skill files and may not provide the per-change confirmation described in its documentation. <br>
Mitigation: Start with --dry-run, keep the target skill in version control, review generated diffs before deployment, and avoid --auto until the changes have been inspected. <br>
Risk: The skill depends on a scanner or audit module that is not declared in the artifact evidence. <br>
Mitigation: Verify the scanner dependency and command entrypoint before installing or running the fixer. <br>


## Reference(s): <br>
- [Fix Templates](references/fix-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Neckr0ik/neckr0ik-security-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON reports, shell command output, code replacements, and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify target skill files, create .env.example, update .gitignore, create backups, or run in dry-run/report-only modes depending on command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
