## Description:

Use this skill to analyze PDFs with a remote MoDora HTTP service. Credentials are managed through declared environment variables and are not stored in the settings file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to upload PDFs to a deployed MoDora HTTP service, wait for preprocessing, and ask questions about one uploaded document. It is intended for environments where the user trusts the MoDora server operator and supplies explicit model credentials through environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote MoDora server receives PDF contents, questions, and the user model API key supplied in MODORA_USER_API_KEY.

Mitigation: Install only when the server operator is trusted; prefer a local or tightly controlled endpoint and use a limited-scope, low-quota key.

Risk: Sensitive PDFs may be processed outside the user's local environment.

Mitigation: Avoid sensitive PDFs unless third-party processing is approved for the relevant data and workflow.

Risk: Incorrect settings could route work through unintended model instances.

Mitigation: Verify the settings file so every pipeline uses explicit user-owned model instances and does not fall back to server defaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/modora-http)
- [Publisher profile](https://clawhub.ai/user/wu-uk)
- [Default MoDora service endpoint](https://api.modora.pro)
- [Example OpenAI-compatible model endpoint](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads require an absolute PDF path, a non-secret user-owned settings JSON file, environment-managed credentials, and explicit remote credential acknowledgement.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
