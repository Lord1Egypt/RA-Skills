## Description:

Generate research-backed Ideal Customer Profiles (ICPs) for mortgage and real estate products. Returns full buyer personas, Meta/Google ad targeting parameters, trigger phrases, content tone, and platform routing - no generic demographics, only actionable targeting intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

External mortgage and real estate marketers use this skill to generate actionable buyer profiles, ad targeting guidance, trigger phrases, and platform routing for specific customer segments. The free paths provide offline ICP profiles and JSON exports; the premium path can generate ICP-tuned marketing content when an Anthropic API key is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The premium content path can load undeclared Python code from local or external paths.

Mitigation: Use premium content generation only in an environment where the imported generate.py module is trusted.

Risk: Premium content generation uses an API key for LLM-backed output.

Mitigation: Limit API key exposure and avoid sharing credentials with untrusted environments.

Risk: Generated mortgage, VA-loan, credit-repair, or real-estate ad copy can create legal or compliance issues if published without review.

Mitigation: Review all generated copy for accuracy and applicable advertising, lending, and compliance requirements before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/icp-modeler)
- [Project homepage from ClawHub metadata](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [CLI text or JSON, with optional generated marketing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline profiles cover five ICPs; premium content generation requires ANTHROPIC_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
