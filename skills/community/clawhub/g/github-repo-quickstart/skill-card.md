## Description: <br>
Use when the user wants a fast, low-friction onboarding guide for an unfamiliar GitHub repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starquakee](https://clawhub.ai/user/starquakee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly understand an unfamiliar GitHub repository's purpose, architecture, setup path, dependencies, entrypoints, releases, and maintenance status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically invoke external GitHub repository analysis for broad repository-help prompts. <br>
Mitigation: Review before installing, limit any GitHub token or session to the minimum repositories and scopes needed, and require confirmation before external GitHub lookups when appropriate. <br>


## Reference(s): <br>
- [GitHub MCP service endpoint](https://api.githubcopilot.com/mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with annotated text blocks and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's language for headings and explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
