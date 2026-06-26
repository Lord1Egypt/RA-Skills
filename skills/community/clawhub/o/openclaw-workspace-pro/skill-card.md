## Description: <br>
Production-ready workspace setup for OpenClaw agents that implements artifact workflows, secrets management, memory compaction, and long-running agent patterns based on OpenAI's Shell + Skills best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eugene9D](https://clawhub.ai/user/Eugene9D) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw workspaces with standard artifact directories, safer credential handling, memory compaction guidance, and long-running agent operating patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent AGENTS.md and TOOLS.md additions may change agent behavior or pre-approve domains that are unsuitable for a workspace. <br>
Mitigation: Review the installed AGENTS.md and TOOLS.md additions before use and remove any domains or instructions that should require confirmation. <br>
Risk: Documented uninstall commands can delete artifacts, memory archives, and configuration if run in the wrong workspace. <br>
Mitigation: Confirm the target workspace and back up artifacts, archives, and configuration before running uninstall commands. <br>
Risk: The security evidence notes missing .env and .gitignore template files that users should verify or supply. <br>
Mitigation: Verify that credential templates and gitignore protections exist before storing secrets or committing workspace files. <br>


## Reference(s): <br>
- [OpenAI Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips) <br>
- [OpenClaw Workspace Pro on ClawHub](https://clawhub.ai/Eugene9D/openclaw-workspace-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Files] <br>
**Output Format:** [Markdown instructions with shell commands and workspace file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs workspace directories and documentation templates through a shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, changelog, released 2026-02-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
