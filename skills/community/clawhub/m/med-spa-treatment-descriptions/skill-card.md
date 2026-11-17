## Description:

Writes US med spa treatment pages with device status, session details and claim limits spelled out, so a provider can approve the copy and publish it. Use when the user asks for med spa treatment descriptions, medical spa website copy, botox and filler treatment page. For US med spa owners, marketing managers and the licensed provider who signs off on clinical language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US med spa owners, marketing managers, and licensed providers use this skill to draft treatment-page copy with treatment details, claim checks, and consent notes for provider review before publication.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The helper does not verify medical claims, so drafted copy may contain inaccurate or unsupported claims.

Mitigation: Use the output as drafting assistance and have the licensed provider verify claims before publication.

Risk: The optional Windows app needs independent review; a matching supplied hash does not establish its safety.

Mitigation: Use the Python workflow instead when possible; independently review the optional app before use and do not run it as administrator without a reason.

## Reference(s):

- [US med spa advertising and claim rules](references/medspa-claim-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/med-spa-treatment-descriptions)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Structured Markdown treatment brief with treatment-page copy, status details, claim checks, consent notes, and open items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider review is required before publication; the helper enforces per-field length limits.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
