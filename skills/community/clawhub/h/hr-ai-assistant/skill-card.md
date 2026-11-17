## Description:

HR AI Assistant helps agents answer HR questions and generate HR policies, forms, job descriptions, reports, and related documents through HRrule AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aijuntao](https://clawhub.ai/user/aijuntao)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, HR practitioners, and operators use this skill to draft HR documents and get HR-focused Q&A support. Developers and platform integrators can use the bundled scripts and references to connect an agent to HRrule AI with configured API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send HR questions and document context to HRrule, which may include sensitive employee, compensation, medical, disciplinary, or legal information.

Mitigation: Use only with authorization and a valid data-processing basis, and avoid sending sensitive employee details unless required and approved.

Risk: The skill uses API credentials for HRrule access.

Mitigation: Do not paste real API keys into chat; prefer environment variables or a protected local secret store and rotate keys if exposed.

Risk: Browser examples include an unsecured ws:// endpoint while the Python client uses wss://ai.hrrule.com.

Mitigation: Prefer TLS-protected wss:// connections and avoid the ws:// browser example for real HR data.

Risk: Generated HR and labor-law guidance may be incomplete, jurisdiction-specific, or unsuitable for final use.

Mitigation: Have qualified HR, legal, or compliance reviewers check generated policies, forms, and advice before relying on them.

Risk: The skill includes optional local scripts and attachment download behavior.

Mitigation: Review scripts before execution, run them in a controlled environment, and inspect downloaded documents before distribution.

## Reference(s):

- [HR AI Assistant on ClawHub](https://clawhub.ai/aijuntao/skills/hr-ai-assistant)
- [HRrule AI](https://ai.hrrule.com/)
- [HRrule AI WebSocket API Reference](artifact/references/api_reference.md)
- [HRrule AI Example Prompts](artifact/references/example_prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown text with optional code blocks, shell commands, configuration snippets, and document download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams HRrule responses; generated attachments may be exposed as Markdown links or downloaded when enabled.]

## Skill Version(s):

2.5.9 (source: server release metadata and changelog, released 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
