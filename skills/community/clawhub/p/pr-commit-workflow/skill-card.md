## Description: <br>
This skill should be used when creating commits or pull requests, enforcing a human-written PR structure, intent capture, and evidence in agentic workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshp123](https://clawhub.ai/user/joshp123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide agents through auditable commit and pull request workflows with human-written PR intent, factual change summaries, test evidence, and prompt history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PR prompt history and local environment details may expose secrets, internal paths, private instructions, tokens, or personal data. <br>
Mitigation: Manually review and redact prompts and environment details before publishing a PR, especially on public or sensitive repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joshp123/pr-commit-workflow) <br>
- [Commit Message Format](references/commit-format.md) <br>
- [Human PR Template](references/pr-human-template.md) <br>
- [Commit Workflow](references/workflow-commit.md) <br>
- [PR Workflow](references/workflow-pr.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and PR body structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow instructions and templates for agent-authored commits and pull requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
