## Description: <br>
Automates GitHub contribution workflows by helping agents find good first issues, analyze projects, prepare branches, implement fixes, and submit pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thatgfsj](https://clawhub.ai/user/Thatgfsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to streamline routine open-source contribution workflows, from issue discovery through pull request drafting and submission, while keeping licensing and project guidelines visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may require broad GitHub write authority through GitHub CLI or API credentials. <br>
Mitigation: Use a least-privilege GitHub credential, avoid broad repo scope where possible, and require human approval before publishing comments, pushes, API calls, or pull requests. <br>
Risk: The daily cron workflow could repeatedly act on GitHub without clear consent or disable guidance. <br>
Mitigation: Do not enable recurring automation unless it is limited to read-only discovery or drafting and has an explicit manual review step before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Thatgfsj/github-pr-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, GitHub CLI and API examples, issue comments, commit messages, and pull request descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub actions under the user's account; comments, pushes, API calls, and pull requests should remain subject to manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
