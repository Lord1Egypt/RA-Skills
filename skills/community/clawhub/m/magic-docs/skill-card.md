## Description: <br>
Magic Docs helps agents maintain Markdown files marked with `<!-- MAGIC DOC -->` by detecting relevant conversation updates and appending or correcting durable project information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use Magic Docs to keep selected Markdown documents current with durable decisions, configuration changes, and project facts captured during agent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may scan workspace content and write conversation-derived information to Markdown files beyond the intended scope. <br>
Mitigation: Define exactly which files and scopes it may manage before use, and review diffs before accepting generated updates. <br>
Risk: Conversation context can include sensitive secrets or infrastructure details that should not be persisted into documentation. <br>
Mitigation: Keep memory, tooling, secret, and infrastructure files out of scope; redact credentials and reference approved secret locations instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wavmson/magic-docs) <br>
- [Publisher profile](https://clawhub.ai/user/wavmson) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown edits with optional inline shell commands and changelog entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May scan workspace Markdown files marked with `<!-- MAGIC DOC -->` and update them when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
