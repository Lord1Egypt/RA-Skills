## Description: <br>
Motie CLI helps agents discover Motie marketplace APIs, inspect API documentation, and call documented routes with the motie CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saucedocs](https://clawhub.ai/user/saucedocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find suitable Motie marketplace APIs, inspect their route documentation, and form CLI calls for external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to discover and call third-party APIs with a Motie API key, including calls that may cost money, change account or real-world state, post content, scrape sensitive sites, or send personal information. <br>
Mitigation: Verify the npm package and publisher, use a scoped or easily revocable Motie API key, avoid passing secrets or unnecessary personal data, and require explicit approval before sensitive or costly API calls. <br>


## Reference(s): <br>
- [Motie beta portal](https://beta.motie.dev) <br>
- [ClawHub skill listing](https://clawhub.ai/saucedocs/motie-cle-beta) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API discovery, documentation lookup, and motie call command construction.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
