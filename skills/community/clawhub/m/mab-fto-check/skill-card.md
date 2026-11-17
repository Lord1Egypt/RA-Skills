## Description:

Mab FTO Check guides agents through monoclonal antibody freedom-to-operate analysis using PatSnap patent data, sequence alignment, structure search, multi-module patent retrieval, claim comparison, risk grading, and a standardized HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent, IP, and biotechnology teams use this skill to structure mAb FTO research, collect required product and market inputs, search relevant antibody patent families, compare independent claims, and produce decision-support reports for attorney review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated FTO conclusions as legal advice or as sufficient for launch clearance.

Mitigation: Present outputs as decision support and require patent attorney review for launch, clearance, licensing, or design-around decisions.

Risk: Live patent retrieval and claim comparison depend on authorized PatSnap/MCP access and current patent data.

Mitigation: Use the skill only with an authorized account, document source retrieval status, and avoid final conclusions when original claims or legal status cannot be fetched.

Risk: Incomplete intake data can narrow searches incorrectly and produce misleading risk assessments.

Mitigation: Collect antibody sequence, target, indication, target market, competitor, and legal-status preferences before running a full FTO workflow.

## Reference(s):

- [User Intake Protocol](artifact/references/user-intake-protocol.md)
- [Search Modules](artifact/references/search-modules.md)
- [Modification Search](artifact/references/modification-search.md)
- [Workflow Steps](artifact/references/workflow-steps.md)
- [Search Loop](artifact/references/search-loop.md)
- [Sequence Search](artifact/references/sequence-search.md)
- [Patent Family Merge](artifact/references/patent-family-merge.md)
- [Output Contract](artifact/references/output-contract.md)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap Eureka Patent Search](https://eureka.zhihuiya.com/search?q={patent_number})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and self-contained HTML report files, with optional shell command output from the recall estimator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized PatSnap/MCP access for live patent retrieval; final FTO conclusions are decision support and should be reviewed by patent counsel.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
