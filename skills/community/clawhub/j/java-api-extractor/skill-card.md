## Description: <br>
Extracts Java Spring Boot Controller-layer API definitions into JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowzhouj](https://clawhub.ai/user/snowzhouj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API platform teams use this skill to scan Java Spring Boot projects, extract Controller endpoints, and prepare standardized JSON API definitions for documentation or downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist extracted API metadata outside the chosen output path. <br>
Mitigation: Run local-only extraction first, use --no-backup when backup copies are not needed, and review generated JSON before sharing it. <br>
Risk: The documentation includes external publishing workflows that may send API metadata to a product platform. <br>
Mitigation: Do not use --push, Git hook, or CI publishing examples until the destination, authorization, and data classification rules have been confirmed. <br>
Risk: Scanning a project may expose internal endpoint names, parameters, and response structures. <br>
Mitigation: Limit runs to approved Java projects and treat the generated API definition file according to the source project's data handling requirements. <br>


## Reference(s): <br>
- [API definition standard](references/api-definition-standard.md) <br>
- [Usage examples](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API definition files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated API metadata may be printed to stdout, written to a JSON file, and optionally backed up or passed to a publishing workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
