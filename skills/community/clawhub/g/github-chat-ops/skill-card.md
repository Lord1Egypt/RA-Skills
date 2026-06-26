## Description: <br>
Manage a single GitHub repository through chat for non-technical requesters after they share the repo URL and a temporary personal token; the skill pulls status, summarizes activity, and creates or follows up on issues through the GitHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamkalio](https://clawhub.ai/user/iamkalio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to ask an assistant for lightweight GitHub repository help in a chat flow, including recent activity summaries, issue creation, issue follow-up, and file-level context checks without cloning the repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide GitHub credentials that may grant repository access. <br>
Mitigation: Use a fine-grained, short-lived token limited to one repository and the minimum permissions needed, avoid retained chat where possible, unset the token after use, and revoke it when the session ends. <br>
Risk: Issue, comment, or repository update text could be posted with incorrect or unintended content. <br>
Mitigation: Review all generated issue bodies, comments, labels, assignees, and status updates before sending API requests that modify GitHub state. <br>
Risk: Daily cron automation can turn temporary repository access into unattended long-lived access. <br>
Mitigation: Enable cron automation only after securing the secret, reviewing the script, documenting how to disable the job, and confirming token revocation procedures. <br>


## Reference(s): <br>
- [GitHub API Cheatsheet (Repo chat ops)](references/github-api-cheatsheet.md) <br>
- [GitHub REST API endpoint](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON request examples, and concise chat-ready summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub API request payloads, issue links, status bullets, and temporary environment-variable handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
