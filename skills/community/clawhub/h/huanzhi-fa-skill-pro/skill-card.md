## Description:

Chinese-language agent skill for OPC founders that supports fundraising readiness diagnosis, business-plan review, term-sheet analysis, policy matching, investor-readiness guidance, emotional support, and optional structured HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-innopower](https://clawhub.ai/user/ai-innopower)

### License/Terms of Use:

MIT

## Use Case:

External founders and startup teams use this skill to assess financing readiness, improve fundraising materials, review investor terms, match Chinese startup policies, and receive structured next-step guidance. It is especially focused on Chinese OPC and early-stage startup financing workflows.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may share confidential business plans, cap tables, term sheets, financials, or legal materials.

Mitigation: Require clear data-handling language, ask users to redact sensitive files before sharing, and avoid retaining uploaded startup materials unless a secure intake process is documented.

Risk: Hardcoded WeChat/email footer and off-platform document transfer can create privacy and support-channel risk.

Mitigation: Make off-platform contact optional, document when it is used, and provide a secure intake path before requesting confidential documents.

Risk: Curl-to-shell installation guidance can expose users to unverifiable installer behavior.

Mitigation: Replace curl-to-shell setup with verifiable package or script steps, checksums, and instructions users can inspect before execution.

Risk: Financing, legal, policy, and tax guidance may be mistaken for professional advice.

Mitigation: Preserve visible disclaimers and route critical financing, legal, accounting, tax, and policy decisions to qualified professionals or official sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-innopower/skills/huanzhi-fa-skill-pro)
- [Publisher profile](https://clawhub.ai/user/ai-innopower)
- [User guide](artifact/docs/user-guide.md)
- [Developer guide](artifact/docs/developer-guide.md)
- [Output schema](artifact/references/outputs-schema.md)
- [Known limitations](artifact/references/known-limitations.md)
- [OPC policy database](artifact/references/opc-policy-db.md)
- [HTML design specification](artifact/references/html-design-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown responses with structured scoring tables, JSON-like report schemas, optional HTML report content, and inline command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include funding scores, risk flags, action plans, policy estimates, disclaimers, and optional report-generation guidance.]

## Skill Version(s):

3.1.0 (source: frontmatter, skill.json, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
