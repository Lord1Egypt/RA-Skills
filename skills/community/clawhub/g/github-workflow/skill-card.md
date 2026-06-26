## Description: <br>
Manage GitHub repositories, issues, pull requests, and GitHub Actions workflows through the MorphixAI GitHub integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect GitHub repositories, manage issues and pull requests, and check or trigger GitHub Actions workflows after linking a GitHub account through MorphixAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a linked GitHub account and may create or close issues, create pull requests, or otherwise change repository state. <br>
Mitigation: Use least-privilege repository access, verify the active GitHub account before acting, and require explicit approval before repository-changing operations. <br>
Risk: Triggering GitHub Actions workflows may run CI/CD jobs or deployments. <br>
Mitigation: Require explicit approval before triggering workflows and confirm the target repository, workflow, branch, and inputs. <br>
Risk: The integration depends on MorphixAI credentials and account linking. <br>
Mitigation: Install only after trusting MorphixAI, store MORPHIXAI_API_KEY securely, and link only the GitHub account needed for the intended work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paul-leo/github-workflow) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and YAML-like GitHub tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked GitHub account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
