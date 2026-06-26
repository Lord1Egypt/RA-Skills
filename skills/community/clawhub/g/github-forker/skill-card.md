## Description: <br>
Github Forker extracts GitHub repository references from text or images, forks the repositories through the GitHub API, stars the originals, and reports the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chat2dev](https://clawhub.ai/user/chat2dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to copy one or more GitHub repositories into their own GitHub account from plain text or image-based repo references. It is most useful when the user wants the agent to normalize repo URLs, call the GitHub API, and return a concise fork/star status report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically stars each original repository after a successful fork without a separate opt-in step. <br>
Mitigation: Review the skill before installation and remove the starring step or require explicit confirmation if automatic starring is not desired. <br>
Risk: The skill requires a GitHub token capable of forking repositories, so an over-scoped or persistent token increases account risk. <br>
Mitigation: Use a least-privilege, revocable GitHub token and avoid storing it permanently in shell startup files unless that storage is intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chat2dev/github-forker) <br>
- [Publisher Profile](https://clawhub.ai/user/chat2dev) <br>
- [curl for Windows](https://curl.se/windows/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API Calls] <br>
**Output Format:** [Markdown report with inline shell commands and GitHub API status details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub token in GITHUB_TOKEN and may perform account-changing API calls.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
