## Description:

Transform AI-generated content into natural, human-sounding writing, measure the improvement, and optionally verify the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itxbilal176](https://clawhub.ai/user/itxbilal176)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to rewrite AI-assisted drafts into clearer, less formulaic text, then review local before/after metrics and an optional metrics-only verification summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional verification could expose sensitive source or rewritten text if used incorrectly.

Mitigation: Send only aggregate evaluation metrics to any verifier; do not send original text, rewritten text, secrets, credentials, or private documents.

Risk: The rewrite could be mistaken for proof of human authorship or an AI-detector result.

Mitigation: Treat the output as a style transformation with documented metrics, not as proof that a human authored the text or that detection can be bypassed.

## Reference(s):

- [Verified Humanizer Examples](artifact/references/examples.md)
- [OpenClaw Integration Notes](artifact/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON response with rewritten text, change notes, local evaluation metrics, and optional verification status; markdown reports may be used from bundled templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rewriting workflow; optional verification should use metrics only, not source or rewritten text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
