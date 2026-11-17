## Description:

Monitor Gmail inbox, read incoming emails, generate personalized follow-up replies with OpenAI, and save replies into Gmail Drafts for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuliuyi717-ux](https://clawhub.ai/user/yuliuyi717-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor selected Gmail inbox messages, generate personalized reply drafts, and keep a human review step before any email is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify Gmail data and create drafts using Gmail OAuth scopes.

Mitigation: Grant Gmail access only to trusted accounts, use narrow Gmail queries, test without --mark-read, and review every generated draft before sending.

Risk: Selected email contents may be sent to the configured model service.

Mitigation: Use a trusted local loopback endpoint or explicitly trusted HTTPS provider, and avoid processing sensitive messages unless that data sharing is approved.

Risk: OAuth tokens, OpenAI keys, or local gateway tokens could expose mailbox or model access if mishandled.

Mitigation: Protect token files and environment variables, use a dedicated OPENAI_API_KEY for external providers, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuliuyi717-ux/skills/gmail-auto-draft)
- [Gmail Auto Draft Setup](references/setup.md)
- [Prompt Tuning](references/prompt-tuning.md)
- [Upwork Demo Preset](references/upwork-demo.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON runtime status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Gmail draft replies and prints per-cycle JSON containing processed counts, draft metadata, skipped messages, and errors.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
