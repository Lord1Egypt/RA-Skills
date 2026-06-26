## Description: <br>
Manages a local GitHub knowledge base and helps agents search repositories, issues, and pull requests with the GitHub CLI while cataloging cloned repositories in GITHUB_KB.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesChan21](https://clawhub.ai/user/JamesChan21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search GitHub, inspect PRs and issues, clone repositories into a local knowledge base, and maintain a markdown catalog of projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use GitHub CLI authentication and a GITHUB_TOKEN when searching or accessing repositories. <br>
Mitigation: Use a limited GitHub token or account, provide credentials through environment variables or secrets, and never hardcode tokens. <br>
Risk: Repository names, descriptions, and cloned code may be stored in the local knowledge base. <br>
Mitigation: Confirm GITHUB_KB_PATH before cloning and avoid cataloging private repositories unless local retention is intended. <br>


## Reference(s): <br>
- [GitHub CLI Linux installation guide](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) <br>
- [ClawHub release page](https://clawhub.ai/JamesChan21/github-kb) <br>
- [Publisher profile](https://clawhub.ai/user/JamesChan21) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and catalog entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GitHub CLI authentication and update local repository files when the user asks to search, clone, or catalog projects.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
