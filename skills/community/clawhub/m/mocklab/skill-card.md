## Description:

MockLab is a smart API toolkit that helps agents turn interface documents into mock schemas, start a local Mock API server, forward requests, and reproduce API data for development and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancer07](https://clawhub.ai/user/lancer07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, test engineers, and API integration teams use this skill to parse API documentation, generate mock response schemas, run a local Mock API server, simulate latency and errors, and proxy requests during integration debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local API tool can expose unauthenticated proxy, admin, file-write, and state-access capabilities.

Mitigation: Keep it on localhost or a trusted network boundary, review it before installation, and add authentication, host restrictions, and safer persistence controls before broader use.

Risk: Request forwarding may send request bodies and custom headers to real URLs.

Mitigation: Use synthetic tokens, sanitize API documents, and avoid production credentials until redaction and forwarding restrictions are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lancer07/skills/mocklab)
- [README](artifact/README.md)
- [English README](artifact/README_en.md)
- [Schema template](artifact/references/demo.json)
- [Generated response examples](artifact/references/demo__实际返回示例.json)
- [Field key naming rules](artifact/references/field_keys.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with JSON schema files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local mock-server configuration and may create project schema and state files.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
