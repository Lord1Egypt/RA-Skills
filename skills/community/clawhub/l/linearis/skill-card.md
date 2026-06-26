## Description: <br>
Linear.app CLI for issue tracking. Use for listing, creating, updating, and searching Linear issues, comments, documents, cycles, and projects. Optimized for LLM agents with JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisnnamdi](https://clawhub.ai/user/whoisnnamdi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use Linearis to query and manage Linear issues, comments, documents, projects, cycles, users, teams, and file embeds from a CLI that returns JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Linear API token can grant access to workspace data. <br>
Mitigation: Use a trusted npm package source and a Linear API token with the narrowest practical scope. <br>
Risk: Create, update, delete, upload, and download commands can change Linear workspace data or local files. <br>
Mitigation: Allow an agent to run these commands only after the user explicitly requests the action and understands the affected resources. <br>


## Reference(s): <br>
- [Linearis documentation](https://github.com/czottmann/linearis) <br>
- [Linearis blog post](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html) <br>
- [Linear](https://linear.app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; CLI commands return JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the linearis binary and a Linear API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
