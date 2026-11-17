## Description:

Guides users through setting up OpenMAIC, generating interactive classrooms, and extending its application and SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyuc](https://clawhub.ai/user/wyuc)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and creators use this skill to generate interactive classrooms from a brief and optional materials. Developers use it to deploy or customize OpenMAIC and its SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Classroom requirements, uploaded materials, and the Live Demo access code are sent to the OpenMAIC service when using its hosted demo.

Mitigation: Use the hosted demo only when its handling of those inputs is appropriate; avoid uploading sensitive documents.

Risk: Local setup can install dependencies, start Docker services, and use provider API keys.

Mitigation: Review commands before approval and keep provider keys in local configuration or the web app rather than chat.

## Reference(s):

- [OpenMAIC on ClawHub](https://clawhub.ai/wyuc/skills/openmaic)
- [OpenMAIC Live Demo](https://open.maic.chat)
- [Classroom generation flow](references/generate-flow.md)
- [Provider keys](references/provider-keys.md)
- [Extending OpenMAIC](references/extend.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide classroom creation and return a classroom link.]

## Skill Version(s):

0.3.13 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
