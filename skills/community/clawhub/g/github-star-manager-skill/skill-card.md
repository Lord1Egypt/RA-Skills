## Description: <br>
Manage GitHub stars with AI-powered categorization and cleanup for organizing starred repositories into GitHub Lists, cleaning up stale or deprecated stars, exporting star data for analysis, and getting stats about GitHub stars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosformula](https://clawhub.ai/user/cosformula) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and GitHub users use this skill to inspect, categorize, export, and maintain their starred repositories. It supports read-only analysis as well as confirmed GitHub Lists and unstar operations through the authenticated GitHub CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the existing GitHub CLI login to read starred repositories and can modify stars or GitHub Lists. <br>
Mitigation: Confirm the active GitHub account and token scopes before use, and use the narrowest scopes that support the requested operation. <br>
Risk: Unstar and list-changing commands can change a user's GitHub account state. <br>
Mitigation: Review proposed repositories and commands with the user before execution, and require explicit confirmation for unstar, create-list, and add-to-list actions. <br>
Risk: Bulk GitHub API operations can hit rate limits or apply repeated changes too quickly. <br>
Mitigation: Run a small batch first and use delays between API calls for larger updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cosformula/github-star-manager-skill) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the existing GitHub CLI authentication session and asks for confirmation before destructive or list-changing operations.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
