## Description: <br>
Microservice Gen is a local Bash toolkit that records development prompts and notes for generation, templating, validation, linting, review, reporting, search, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill as a local searchable journal for microservice-related development prompts, notes, checks, and reports. It should not be treated as a real code generator, linter, formatter, or validator without independent review of its outputs and behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect real microservice generation, validation, linting, or formatting, while the artifact primarily records supplied text in local logs. <br>
Mitigation: Use it only as a local development journal and independently review any generated, validated, or formatted code before relying on it. <br>
Risk: Prompts, proprietary code, credentials, internal paths, or incident details entered into commands are persisted under ~/.local/share/microservice-gen/ and can be exported. <br>
Mitigation: Avoid entering sensitive information, restrict access to the local data directory, and delete logs or exported files when they are no longer needed. <br>


## Reference(s): <br>
- [Microservice Gen on ClawHub](https://clawhub.ai/xueyetianya/microservice-gen) <br>
- [Publisher profile: xueyetianya](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records timestamped local log entries under ~/.local/share/microservice-gen/ and can export logs as JSON, CSV, or text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
