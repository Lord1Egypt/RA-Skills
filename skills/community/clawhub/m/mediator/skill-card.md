## Description:

Mediator helps agents filter messages from configured difficult contacts by extracting factual requests, summarizing tone-neutral content, and drafting measured responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylntrnr](https://clawhub.ai/user/dylntrnr)

### License/Terms of Use:


## Use Case:

Individuals and agents use this skill to mediate incoming email or iMessage communications from explicitly configured contacts. It supports contact configuration, message checking, factual or neutral summaries, and draft response guidance for review before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive personal communications and writes configuration, state, and logs under the user's home directory.

Mitigation: Use it only with accounts and contacts you explicitly configure, review local file permissions, and keep original messages available for important decisions.

Risk: Default Gmail accounts and notification settings may not match the installing user's intended scope.

Mitigation: Remove or replace hardcoded account and notification defaults before enabling scheduled checks through cron or heartbeat.

Risk: Runtime dependency installation can fetch packages without a pinned, reviewed dependency source.

Mitigation: Install required dependencies yourself from trusted, pinned sources before running the scripts.

Risk: AI summaries and suggested responses can omit context or produce misleading guidance.

Mitigation: Treat summaries and drafts as review aids, and inspect original messages before responding to legal, financial, child-related, or otherwise sensitive communications.

Risk: Auto-response behavior could send messages without adequate human review.

Mitigation: Keep response mode set to draft unless a human has reviewed the configuration, contact scope, and failure modes.

## Reference(s):

- [Prompt reference](artifact/references/prompts.md)
- [ClawHub skill page](https://clawhub.ai/dylntrnr/skills/mediator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON-like summary fields, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include factual summaries, action-required flags, deadlines, and suggested neutral responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
