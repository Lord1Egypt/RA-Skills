## Description: <br>
Bootstraps the Google agents-cli experience for scaffolding, building, evaluating, deploying, publishing, and observing ADK agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliasecchig](https://clawhub.ai/user/eliasecchig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this onboarding skill to install and activate the Google agents-cli toolchain for common Google Agent Development Kit workflows, including project scaffolding, evaluation, deployment, publishing, and observability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup command is unpinned and persistently installs multiple additional agent skills that were not included in this review. <br>
Mitigation: Verify the package source, pin a known version where possible, and inspect the installed skills before using them. <br>
Risk: The installed workflow skill may remain always active after setup. <br>
Mitigation: Confirm how to disable or remove the workflow skill before installing it in a shared or production agent environment. <br>


## Reference(s): <br>
- [Google agents-cli](https://github.com/google/agents-cli) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to install and activate additional specialized skills after setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
