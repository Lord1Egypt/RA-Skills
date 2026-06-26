## Description: <br>
Submit bug reports to GitHub for OpenClaw issues, including issue templates, GitHub API workflows, and post-submission follow-up reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to prepare, search, create, update, and follow up on OpenClaw GitHub bug reports with a consistent issue format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact contains a hardcoded GitHub token. <br>
Mitigation: Revoke the embedded token, remove it from all skill files, and require a user-supplied least-privilege token through the runtime environment. <br>
Risk: The workflow can create or modify public GitHub issues and comments. <br>
Mitigation: Require human review before posting logs, configurations, screenshots, new issues, updates, or follow-up comments to GitHub. <br>


## Reference(s): <br>
- [Quick Ref](references/quick-ref.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and Python workflow references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in GitHub API calls that create, update, search, or follow up on public issues.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
