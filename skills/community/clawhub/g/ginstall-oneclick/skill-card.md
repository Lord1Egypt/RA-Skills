## Description: <br>
GInstall OneClick helps agents set up GitHub Node.js repositories by planning, cloning, installing dependencies, and running development scripts through the ginstall CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunzhouli-hub](https://clawhub.ai/user/yunzhouli-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they want an agent to install or prepare GitHub Node.js repositories, including monorepo subpaths, with the ginstall CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unfamiliar GitHub repository can clone code, install packages, and run project scripts on the local machine. <br>
Mitigation: Use guided or plan-only mode for unfamiliar repositories, review the generated plan before execution, avoid --yes unless the repository and environment are trusted, and verify the external ginstall CLI source and version. <br>
Risk: Private repository access may require a GitHub token. <br>
Mitigation: Use a least-privilege token only when needed, keep it in the environment or approved secret storage, and never paste tokens into chat or shared plan files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunzhouli-hub/ginstall-oneclick) <br>
- [GInstall OneClick CLI homepage](https://github.com/ginstall-oneclick/ginstall-oneclick) <br>
- [OpenClaw skill format](https://docs.openclaw.ai/clawhub/skill-format) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and environment variable notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point to ginstall plan Markdown and report paths emitted by the CLI.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
