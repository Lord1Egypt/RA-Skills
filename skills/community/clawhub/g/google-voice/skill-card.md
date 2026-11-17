## Description:

Google Voice web-client automation and MCP integration from HAR captures for SMS thread access, approved SMS sends, approved outbound calls, optional audio injection and recording, and HAR endpoint analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate Google Voice web-client workflows from authenticated browser sessions or HAR-derived endpoint knowledge. It is intended for user-approved SMS reads, SMS sends, outbound calls, local audio injection, call recording, and MCP-based Google Voice operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad authenticated Google Voice account actions, including sending SMS and starting calls.

Mitigation: Review before installing and require explicit approval for the exact recipient, phone number, message, call intent, or audio before taking external actions.

Risk: Cookie exports, HAR samples, SMS records, generated speech, and call recordings can expose private account or communications data.

Mitigation: Prefer browser/CDP mode, keep cookie exports outside shared workspaces, avoid committing secrets or raw payloads, and treat exported records and recordings as sensitive private data.

Risk: Raw endpoint calls and audio mode can bypass normal guardrails or increase impact if misconfigured.

Mitigation: Avoid gv_raw_call unless the endpoint and payload are understood, use dry-run modes before live actions, and do not run audio mode as a privileged user.

## Reference(s):

- [Google Voice Skill Page](https://clawhub.ai/earlvanze/skills/google-voice)
- [Publisher Profile](https://clawhub.ai/user/earlvanze)
- [Google Voice HAR Notes](references/har-endpoints.md)
- [Google Voice Call HAR Notes](references/call-har-endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON records, and code-oriented configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive SMS records, call recordings, generated speech files, and authenticated Google Voice actions when explicitly approved.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
