## Description: <br>
GInstall OneClick helps an agent use the ginstall CLI to plan, clone, install Node.js dependencies, and run development scripts for GitHub projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunzhouli-hub](https://clawhub.ai/user/yunzhouli-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up GitHub-hosted Node.js projects from natural language requests, including owner/repo inputs, full GitHub URLs, and monorepo tree paths. It guides the agent to invoke ginstall in guided, assisted, or plan-only modes and to handle optional GitHub authentication for private repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps run an installer for arbitrary GitHub projects, which may execute untrusted dependency or development scripts. <br>
Mitigation: Use guided or plan-only mode for unfamiliar repositories, review the generated plan before execution, and avoid non-interactive approval unless the repository and environment are trusted. <br>
Risk: The separate ginstall CLI is required but not bundled in the skill artifact. <br>
Mitigation: Verify the ginstall CLI source and version before installing or running it. <br>
Risk: A GitHub token used for private repositories could be exposed to untrusted project scripts if provided too broadly. <br>
Mitigation: Use a least-privileged token such as contents:read, provide it only when needed, and avoid pasting secrets into chat or shared plan files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunzhouli-hub/one-click-installation-of-github-projects) <br>
- [GInstall OneClick homepage](https://github.com/ginstall-oneclick/ginstall-oneclick) <br>
- [OpenClaw skill format](https://docs.openclaw.ai/clawhub/skill-format) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point users to plan Markdown and report paths produced by the ginstall CLI.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
