## Description:

Dual-layer AI content guardrail with red-team test methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add an outbound message guardrail to chatbots or AI agents and to red-team the guardrail against common output-safety bypass patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Eligible outbound chat messages may be sent to Google Gemini for external judging.

Mitigation: Use only where third-party judging is acceptable, and add local redaction or deterministic secret checks before remote evaluation for sensitive deployments.

Risk: The default pattern allows messages through when the judge errors or times out.

Mitigation: Configure fail-closed behavior for confidential, child-facing, financial, health, HR, or regulated use cases.

Risk: The Google API key is required for operation and could create exposure if handled broadly.

Mitigation: Restrict and rotate the Google API key, keep it server-side, and pin dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-content-safety-guard)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)
- [Google Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta/models)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, YAML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_GENAI_API_KEY and sends eligible outbound messages to Google Gemini for judging.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
