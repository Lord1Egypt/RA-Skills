## Description: <br>
AWS STS helps agents inspect OOMOL connector schemas and run AWS STS actions through the oo CLI, including actions that can return temporary AWS credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they want an agent to call AWS STS through an OOMOL-connected account, inspect live action schemas, and request temporary credentials for approved STS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce temporary AWS credentials through assume_role or get_federated_credentials. <br>
Mitigation: Require explicit user approval before running either credential-producing action, including the intended role, federation context, and payload. <br>
Risk: The artifact presents untagged actions as safe to run directly while the available actions can return credentials. <br>
Mitigation: Treat all AWS STS action runs as sensitive, inspect the live schema first, and review the exact JSON payload before execution. <br>


## Reference(s): <br>
- [AWS STS homepage](https://aws.amazon.com/iam/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-aws-sts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector schema and run commands; responses can include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
