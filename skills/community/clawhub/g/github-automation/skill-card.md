## Description: <br>
Automate common GitHub tasks including creating issues, checking PR status, listing repositories, and managing projects from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcompile](https://clawhub.ai/user/cloudcompile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to perform common GitHub workflows programmatically, including issue creation, PR checks, repository listing, and notification review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a GitHub token while security evidence reports weakened HTTPS protections. <br>
Mitigation: Review before installing, restore TLS verification before using a real token, and use a fine-grained token limited to the specific repositories and actions needed. <br>
Risk: The skill can perform write actions such as creating issues or commenting on GitHub resources. <br>
Mitigation: Manually confirm any action that writes to GitHub and scope the token to only the required permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudcompile/github-automation) <br>
- [GitHub REST API endpoint](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GITHUB_TOKEN environment variable for authenticated GitHub API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
