## Description:

Diagnose and recover from model rate limit errors (ChatGPT usage limits, 429 errors). Use when cron jobs or agent sessions fail with "Try again in ~9500 min" or similar rate limit messages. Covers API key rotation, model fallback, and manual recovery procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose model-provider rate-limit failures in agent sessions or scheduled jobs and choose recovery steps such as model fallback, API key rotation, or cron job updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-checking examples may expose API keys if copied directly.

Mitigation: Check only whether expected keys are present or use a secret manager; do not run broad environment greps that print secret values.

Risk: Cron update and recovery-script steps can change scheduled task behavior or rerun the wrong job.

Mitigation: Verify the job ID, preview the patch, keep a rollback path, and treat cron changes as privileged operations.

Risk: The recovery-script example writes under /root, which may be inappropriate for normal deployments.

Mitigation: Use a least-privileged workspace path unless root-owned placement is explicitly required.

## Reference(s):

- [OpenClaw Model Providers Docs](/concepts/model-providers)
- [API Key Rotation Documentation](/concepts/model-providers#api-key-rotation)
- [Cron Job Management](/tools/cron)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic steps, recovery procedures, cron configuration examples, and model fallback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
