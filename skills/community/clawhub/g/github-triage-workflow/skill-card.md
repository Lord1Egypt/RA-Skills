## Description: <br>
Review GitHub repositories, group issues and pull requests by urgency, and take safe triage actions after confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review GitHub issues and pull requests, group repository work by urgency, and prepare or apply triage actions after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can work through authenticated GitHub access and may propose repository-changing actions such as labels, comments, assignments, issue creation, and issue status updates. <br>
Mitigation: Use read-only inspection first, preview intended writes when available, and require explicit user confirmation before any GitHub write action. <br>
Risk: Triage recommendations may misclassify urgency or suggest action that does not match repository norms. <br>
Mitigation: Group items with supporting evidence, keep initial reports concise, and prefer draft comments or proposed actions when uncertainty remains. <br>
Risk: The release requires OAuth-connected GitHub access and sensitive credentials through ClawLink. <br>
Mitigation: Install only for expected GitHub triage workflows, verify the GitHub integration is connected, and review commands before approving them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/github-triage-workflow) <br>
- [GitHub REST API](https://docs.github.com/en/rest) <br>
- [GitHub GraphQL API](https://docs.github.com/en/graphql) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated GitHub write actions, but the artifact requires preview and confirmation before comments, labels, closure, reopening, or metadata edits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
