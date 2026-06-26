## Description: <br>
Manage GitHub Projects v2 with the GitHub CLI to list and filter project items, update project fields, comment on issues, create issues, and manage sub-issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freddydk](https://clawhub.ai/user/freddydk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to operate GitHub Projects v2 from an agent workflow, including backlog triage, project field updates, issue creation, issue comments, and sub-issue management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to perform GitHub write actions across repositories and projects. <br>
Mitigation: Review each command before execution and use a GitHub token limited to the specific owner, repository, and project needed for the task. <br>
Risk: The skill suggests installing an unpinned third-party GitHub CLI extension for sub-issue workflows. <br>
Mitigation: Install the extension only after reviewing and trusting it, pin it where possible, or use the documented GraphQL fallback instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freddydk/git-hub-projects-v2) <br>
- [Publisher profile](https://clawhub.ai/user/freddydk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated GitHub CLI session with project scope for full functionality.] <br>

## Skill Version(s): <br>
1.0.0 (source: changelog and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
