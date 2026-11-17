## Description:

Diagnose and fix common Gladia API issues, including authentication and rate-limit errors, unexpected transcription behavior, audio format problems, WebSocket disconnections, polling failures, billing confusion, and limits questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiaio](https://clawhub.ai/user/gladiaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose Gladia API integration failures, transcription quality issues, billing or concurrency confusion, and production-readiness problems. It guides users toward SDK-first fixes and targeted checks for authentication, rate limits, audio formats, live sessions, webhooks, and plan restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting may involve API keys or account details.

Mitigation: Keep Gladia API keys private and avoid sharing secrets in prompts, logs, or copied error output.

Risk: Limits, pricing, SDK versions, and plan restrictions can change over time.

Mitigation: Verify time-sensitive production decisions against Gladia's current official documentation or dashboard.

## Reference(s):

- [Authentication](https://docs.gladia.io/chapters/api/authentication)
- [Rate limits and concurrency](https://docs.gladia.io/chapters/limits-and-specifications/rate-limits)
- [Supported formats and limits](https://docs.gladia.io/chapters/limits-and-specifications/supported-formats)
- [Webhooks](https://docs.gladia.io/chapters/pre-recorded-stt/webhooks)
- [API reference](https://docs.gladia.io/api-reference)
- [Gladia Documentation](https://docs.gladia.io)
- [Support Center](https://support.gladia.io)
- [API Status](https://status.gladia.io)
- [Dashboard](https://app.gladia.io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with inline JSON, TypeScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides troubleshooting checks, remediation steps, and verification checklist items; it does not execute API calls or require tool access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
