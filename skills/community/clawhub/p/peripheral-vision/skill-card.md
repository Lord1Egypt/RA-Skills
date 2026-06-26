## Description: <br>
Monitors adjacent systems, upstream dependencies, and downstream consumers for changes that could affect current work before they break it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to scan surrounding project context for upstream, downstream, sibling, schema, environment, and temporal changes that may affect the files they are working on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect broad repository context, including schemas, dependency links, configuration, CI/CD, infrastructure references, and Git history. <br>
Mitigation: Install it only in repositories where that level of project inspection is acceptable, and ask the agent to limit scans to relevant paths in sensitive repositories. <br>
Risk: Alerts may include sensitive environment or infrastructure details if the agent reports everything it observes. <br>
Mitigation: Avoid printing secrets, environment values, or detailed infrastructure information in alerts. <br>


## Reference(s): <br>
- [Peripheral Vision on ClawHub](https://clawhub.ai/jcools1977/peripheral-vision) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured alerts and command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; zero external dependencies and zero API calls are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
