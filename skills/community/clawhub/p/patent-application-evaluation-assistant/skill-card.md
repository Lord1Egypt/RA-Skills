## Description:

Assists corporate IPR teams, patent engineers, and patent attorneys with pre-evaluating patent applications by checking disclosure completeness, searching patent and non-patent prior art, analyzing China, United States, and Europe patentability, and producing an A/B/C rating with risks and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Corporate IPR teams, patent engineers, and patent attorneys use this skill for initial patent application triage, prior-art-informed patentability review, and application strategy. It is intended to identify disclosure gaps, assess grant feasibility and patent value, and recommend whether to apply, supplement, defer, or treat the invention as a trade secret.

### Deployment Geography for Use:

Global; evaluation coverage focuses on China, United States, and Europe patentability standards.

## Known Risks and Mitigations:

Risk: The skill can send invention-disclosure-derived search queries to external patent and web search services.

Mitigation: Install only for users authorized to disclose those search terms to PatSnap and web search providers; sanitize queries and avoid trade secrets, privileged legal content, export-controlled material, customer-confidential information, or unreleased product identifiers unless those services are approved for that data.

Risk: Generated patentability assessments may be mistaken for formal legal advice.

Mitigation: Present conclusions as preliminary application triage and require review by qualified patent professionals before filing, abandoning, disclosing, or relying on the analysis.

Risk: Optional exported HTML reports may contain sensitive invention and business information.

Mitigation: Treat exported reports as confidential IP/legal work product and store, transmit, and delete them according to the user's approved confidentiality controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-application-evaluation-assistant)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [Opening Message](references/opening-message.md)
- [User Input Template](references/user-input-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with tables, structured ratings, cited prior-art references, and optional self-contained HTML report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include material completeness status, A/B/C or supplement-needed rating, scoring breakdown, China/US/Europe patentability analysis, risks, recommendations, and confidence grading.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
