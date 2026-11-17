## Description:

Generate professional PDF client intake forms for pet sitting businesses with fillable fields, custom themes, multi-pet support, home-access sections, and service-specific templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[basilanathan](https://clawhub.ai/user/basilanathan)

### License/Terms of Use:

MIT

## Use Case:

External pet sitters, dog walkers, boarding businesses, and pet care professionals use this skill to generate branded client onboarding and pet information PDFs from business details, service choices, and optional configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script through shell access and its manifest places user-provided text into a command template.

Mitigation: Review generated shell commands before execution and avoid passing untrusted text into the form-generation prompt until inputs are handled as structured arguments.

Risk: Generated intake PDFs may contain house-entry details, alarm codes, WiFi credentials, addresses, emergency contacts, and veterinary information.

Mitigation: Store and share completed PDFs securely, and omit home-access fields unless they are needed for the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/basilanathan/skills/pet-sitter-intake)
- [Source Repository Listed in Skill Metadata](https://github.com/basilanathan/pet-sitter-intake)
- [Support Issues](https://github.com/basilanathan/pet-sitter-intake/issues)
- [README](artifact/README.md)
- [Example Configurations](artifact/examples/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent collects business and pet-care form inputs, can use YAML configuration, and produces a fillable or print-ready PDF through a local Python script.]

## Skill Version(s):

5.0.1 (source: server release metadata; artifact manifests list 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
