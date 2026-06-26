## Description: <br>
Comprehensive GitHub CLI (gh) reference. Covers repos, issues, PRs, Actions, releases, gists, search, projects v2, API, secrets/variables, labels, codespaces, extensions, auth, and advanced GraphQL patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a GitHub CLI reference for authentication, repository work, issues, pull requests, Actions, releases, API calls, secrets, variables, codespaces, extensions, and automation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub tokens, secrets, or environment values could be exposed when following authentication, token, or .env examples. <br>
Mitigation: Keep `gh` authenticated with the minimum scopes needed, do not print or paste tokens, and review `.env` files before importing them. <br>
Risk: Repository, release, issue, or workflow commands can mutate or delete GitHub resources when run against the wrong target. <br>
Mitigation: Confirm repository names before mutating or deleting anything and prefer explicit `--repo OWNER/REPO` targeting when context is ambiguous. <br>
Risk: GitHub CLI extensions can add unreviewed behavior to an agent workflow. <br>
Mitigation: Install `gh` extensions only from trusted repositories. <br>


## Reference(s): <br>
- [Github Cli on ClawHub](https://clawhub.ai/tag-assistant/github-cli) <br>
- [tag-assistant publisher profile](https://clawhub.ai/user/tag-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the GitHub CLI (`gh`) for command execution; authenticated GitHub access is needed for commands that contact GitHub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
