## Description: <br>
Have I Been Pwned connector for searching and reading breach, paste, data-class, subscription, and latest-breach data through the OOMOL oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Have I Been Pwned through an OOMOL-connected account for breach records, latest breach data, subscription status, data classes, paste exposures, and breached-account searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a Have I Been Pwned API key through OOMOL as an intermediary. <br>
Mitigation: Install only when that intermediary model is acceptable, and connect credentials only through the intended OOMOL account. <br>
Risk: First-time setup includes curl-to-bash and PowerShell install commands. <br>
Mitigation: Prefer the official install guide, inspect installer scripts before execution, and verify the source. <br>
Risk: Breach and paste searches may reveal sensitive information about email addresses. <br>
Mitigation: Query email addresses only when the user explicitly asks for those accounts to be checked. <br>


## Reference(s): <br>
- [Have I Been Pwned homepage](https://haveibeenpwned.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-haveibeenpwned) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL account, and a connected Have I Been Pwned API key for live connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
