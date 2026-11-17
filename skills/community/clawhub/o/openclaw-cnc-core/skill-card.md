## Description:

Supports CNC machining quotes with drawing analysis, cost estimates, historical case retrieval, and risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

CNC shops and developers use the skill to estimate machining costs, generate quotes, retrieve similar cases, and identify quotes needing manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proprietary or customer-owned CAD files may be exposed through the public demo.

Mitigation: Avoid uploading sensitive drawings unless the demo operator's data handling is approved; use local processing for sensitive work.

Risk: Cloud providers and Feishu webhooks may receive sensitive quote or customer details.

Mitigation: Use approved providers and destinations only; prefer local models where data must remain private.

Risk: The provider guide suggests piping a downloaded installer into a shell.

Mitigation: Review installation steps and use an approved installation method instead of running an unreviewed remote script.

Risk: The included publishing script can force-push repositories using configured tokens.

Mitigation: Do not run the publishing script unless you intend to overwrite the publisher's remote branches with authorized credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/timo2026/skills/openclaw-cnc-core)
- [Provider configuration guide](artifact/docs/PROVIDERS.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions]

**Output Format:** [Structured quote data (Python object or JSON), with risk and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes price breakdown, confidence, and manual-review flags.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
