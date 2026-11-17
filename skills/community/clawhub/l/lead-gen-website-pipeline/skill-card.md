## Description:

Automated lead generation pipeline that finds local businesses with weak/no websites, AI-generates custom demo sites, deploys to Vercel, and runs a 5-email cold outreach drip sequence via AgentMail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[razzledazzlei](https://clawhub.ai/user/razzledazzlei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, growth operators, and agencies use this skill to configure an automated local-business lead pipeline that discovers prospects, prepares demo websites, tracks approval status, deploys previews, and drafts outreach follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says this skill installs unpinned remote code.

Mitigation: Use an isolated workspace or account, pin and audit the remote repository and dependencies before running npm install, and avoid sharing privileged credentials with the runtime.

Risk: The security summary says this skill enables unattended cold outreach.

Mitigation: Run outreach in dry-run mode first, require human approval of recipients and message content, and add unsubscribe, suppression, rate-limit, and legal-compliance controls before sending.

Risk: The security summary says this skill uses persistent credentials for external services.

Mitigation: Restrict Google, Vercel, AgentMail, and model-provider API keys to the minimum permissions needed, store them outside source control, and rotate them after testing.

## Reference(s):

- [Lead Gen Website Pipeline on ClawHub](https://clawhub.ai/razzledazzlei/skills/lead-gen-website-pipeline)
- [5-Email Drip Sequence](artifact/references/drip-sequence.md)
- [Environment Variables Reference](artifact/references/env-example.md)
- [Google Sheet Setup](artifact/references/google-sheet-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, configuration examples, JSON artifact descriptions, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe per-lead artifacts such as intake, research, specification, HTML, evaluation, outreach email, screenshots, visual QA, and status files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
