## Description:

AI Text Humanizer rewrites submitted text through the Claw0x API to reduce common signs of AI-generated writing, using an LLM path with a regex fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and agent pipelines use this skill to rewrite AI-drafted text so it sounds more natural while preserving the original meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text is sent to external AI services for rewriting.

Mitigation: Use only with text approved for external processing; avoid secrets, regulated data, confidential drafts, and private customer information unless that processing is approved.

Risk: The skill requires API credentials for Claw0x authentication.

Mitigation: Store CLAW0X_API_KEY in a secure environment variable or secret manager, and do not place keys in prompts, source files, or version-controlled configuration.

Risk: Automated rewriting can change tone, emphasis, or nuance.

Mitigation: Review the rewritten output before publication or customer-facing use.

## Reference(s):

- [AI Text Humanizer on ClawHub](https://clawhub.ai/kennyzir/skills/humanizer-plus)
- [Publisher profile](https://clawhub.ai/user/kennyzir)
- [Claw0x](https://claw0x.com)
- [Claw0x API endpoint](https://claw0x.com/v1/call)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON response containing rewritten text, length metadata, and the processing method.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW0X_API_KEY. Submitted text is sent to Claw0x and may be processed by Gemini on the LLM path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
