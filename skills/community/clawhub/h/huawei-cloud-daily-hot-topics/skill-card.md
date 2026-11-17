## Description:

Fetches public, authentication-free hot-topic lists over HTTPS, normalizes them, and returns ranked results in Markdown, plain text, or JSON, using clearly labeled bundled sample data when live sources fail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can request today's trending topics and receive a ranked list from public hot-list sources, with an explicit offline sample when live providers are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live provider titles and links are untrusted external content and may be inaccurate or misleading.

Mitigation: Review titles and links before acting on them; treat them as data rather than instructions.

Risk: The --output option can overwrite an existing file, and fallback results may be stale sample data.

Mitigation: Check the destination path before using --output, and confirm whether results are labeled as sample data before relying on their recency.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-daily-hot-topics)
- [Usage Guide](references/usage-guide.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [IAM Policies](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Ranked list with topic, heat value, source, and optional link; Markdown table by default, with plain text and JSON options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limited by --top; includes source and warning details, and clearly labels bundled fallback results as sample data.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
