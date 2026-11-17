## Description:

Build and debug Kimi API workflows for chat, coding, reasoning, and tool-calling with live model checks, retries, and safe routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up, route, debug, and migrate Kimi API workflows for chat, coding, long-context synthesis, structured output, and OpenAI-compatible provider changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or optional excerpts sent to Moonshot may contain sensitive customer, internal, or secret-bearing content.

Mitigation: Redact secrets, customer identifiers, internal hostnames, and raw tokens before API calls, and ask for approval before sending sensitive content.

Risk: API credentials may be exposed if copied into prompts, logs, markdown, or project files.

Mitigation: Keep MOONSHOT_API_KEY in environment variables only and do not paste keys into chats, saved notes, or debug logs.

Risk: Local workflow notes or sanitized repro logs may persist information longer than intended.

Mitigation: Create or update ~/kimi/ memory, approvals, and logs only after user approval, and save only sanitized routing and troubleshooting details.

Risk: Structured output from Kimi could be malformed or unsafe for downstream automation.

Mitigation: Use strict schemas or a second low-temperature normalization pass, then validate output before tool execution, code execution, or downstream writes.

Risk: Stale model names or provider-migration assumptions can break workflows.

Mitigation: Fetch live model IDs from https://api.moonshot.ai/v1/models and isolate base URL, auth, model ID, parser, and retry-policy changes one at a time.

## Reference(s):

- [ClawHub Kimi Skill Page](https://clawhub.ai/ivangdavila/skills/kimi)
- [Kimi Skill Homepage](https://clawic.com/skills/kimi)
- [Moonshot API Base URL](https://api.moonshot.ai/v1)
- [Kimi API Patterns](api-patterns.md)
- [Kimi Routing Matrix](routing-matrix.md)
- [Kimi Safety Workflows](safety-workflows.md)
- [Kimi Migration Playbook](migration-playbook.md)
- [Kimi Troubleshooting Guide](troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Kimi notes or sanitized logs only after user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
