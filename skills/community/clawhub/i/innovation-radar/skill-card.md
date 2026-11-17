## Description:

Innovation Radar analyzes R&D reports, meeting notes, technical proposals, and experiment records to identify potential technical innovations, rate novelty and technical completeness, suggest protection paths, ask follow-up questions, and produce an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

R&D teams, IP engineers, and technical leaders use this skill to screen everyday technical materials for protectable innovation candidates before formal patent drafting or deeper prior-art review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential inventions or trade secrets may be sent to the configured PatSnap patent-search MCP service.

Mitigation: Use the skill only after the organization has approved that data flow, and avoid export-controlled, unpublished, or highly confidential R&D unless explicitly approved.

Risk: Generated HTML reports may store extracted technical details from sensitive R&D materials.

Mitigation: Handle session reports under the same access controls used for confidential invention disclosures and review them before sharing.

Risk: Patentability and protection recommendations are preliminary screening outputs.

Mitigation: Have an IP engineer or qualified professional confirm novelty, disclosure risk, and protection strategy before filing or business action.

## Reference(s):

- [Innovation Extraction Prompt](artifact/references/innovation_extraction_prompt.md)
- [Innovation Taxonomy](artifact/references/innovation_taxonomy.md)
- [Patentability Criteria](artifact/references/patentability_criteria.md)
- [Protection Decision](artifact/references/protection_decision.md)
- [Follow-up Questions](artifact/references/followup_questions.md)
- [MCP Usage Guide](artifact/references/mcp_usage_guide.md)
- [HTML Report Template](artifact/references/html_template.md)
- [PatSnap Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Files, Guidance]

**Output Format:** [HTML report with structured innovation assessments, action queues, evidence tables, and follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a configured PatSnap patent-search MCP service when technical elements are complete; writes a session HTML report.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
