## Description: <br>
Helps an agent manage local skill installation, update checks, updates, and uninstall actions for skills sourced from GitHub repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qvshuo](https://clawhub.ai/user/qvshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, register, check, update, and uninstall local skills from GitHub repositories while tracking source metadata in REGISTRY.yaml. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to install, update, or remove local skills. <br>
Mitigation: Require explicit confirmation before uninstalling or bulk-updating skills, and avoid overwriting existing directories except during an intentional update. <br>
Risk: Installing or updating unfamiliar GitHub skills can introduce unreviewed behavior into the local agent environment. <br>
Mitigation: Verify the owner, repo, branch, and path before use, and inspect unfamiliar skills before deployment. <br>
Risk: GitHub operations depend on an authenticated gh CLI session. <br>
Mitigation: Use a least-privileged GitHub login where possible and check authentication status before running GitHub API operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qvshuo/github-skill-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with status tables, inline shell commands, and YAML registry entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local skill file changes and REGISTRY.yaml updates when the agent executes the workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
