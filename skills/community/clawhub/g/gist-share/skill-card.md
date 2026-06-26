## Description: <br>
Post content to GitHub Gist and get back a shareable URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ragesaq](https://clawhub.ai/user/ragesaq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to publish markdown or text context to GitHub Gist and return a shareable URL for handoff or later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public gists, which may expose secrets, private logs, customer data, internal prompts, or proprietary material. <br>
Mitigation: Review gist content before publication and use secret gists only when link-based access is appropriate; do not upload sensitive or proprietary data. <br>
Risk: The artifact gives long-lived GitHub token setup guidance that may persist credentials in shell startup files. <br>
Mitigation: Prefer GitHub CLI authentication or a credential manager, use the minimum gist-only scope, and rotate or revoke the token when it is no longer needed. <br>


## Reference(s): <br>
- [Gist Share ClawHub listing](https://clawhub.ai/ragesaq/gist-share) <br>
- [Gist Share homepage](https://github.com/PsiClawOps/gist-share) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and returned GitHub Gist URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub CLI authentication with a token that has gist scope.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
