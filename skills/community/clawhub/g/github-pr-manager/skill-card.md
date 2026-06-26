## Description: <br>
Manages GitHub pull request workflows by tracking PR status, checking CI, handling review feedback, fixing routine issues, and preparing replies through merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godnight](https://clawhub.ai/user/godnight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to have an agent monitor and manage GitHub pull requests, respond to CI and reviewer feedback, and keep the user informed until merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact GitHub changes using the user's GitHub identity, including pushes, force-pushes, comments, branch deletion, and issue updates. <br>
Mitigation: Use a fine-grained token limited to the specific repository and require explicit confirmation before any high-impact GitHub operation. <br>
Risk: Recurring PR tracking can continue after the user's immediate task is complete. <br>
Mitigation: Remove scheduled tracking when the PR is closed or merged, and keep tracking state visible in the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godnight/github-pr-manager) <br>
- [GitHub PR management workflow](artifact/references/workflow.md) <br>
- [PR reply templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, GitHub CLI/API command examples, reply templates, and task tracking notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create PR tracking notes and schedule recurring checks when configured by the agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
