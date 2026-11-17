## Description:

Legal Doc Reviewer helps agents review NDAs, compare contract versions, verify legal citations, generate meeting briefings, and assemble legal status reports with risk flags and suggested revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, compliance, and business teams use this skill to produce draft review artifacts for NDAs, contract redlines, legal citation checks, privileged meeting summaries, and weekly status reports. Its outputs are intended to support review by qualified legal professionals, not replace formal legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive legal documents and may create local outputs or logs containing privileged or confidential material.

Mitigation: Run it in a constrained workspace, limit access to generated files and logs, and avoid retaining privileged or confidential material unless retention and access controls are clear.

Risk: The skill asks for broad command execution and callback or API use.

Mitigation: Review command execution, network callbacks, and API use before allowing them, and keep API keys in environment variables rather than documents or logs.

Risk: Generated legal analysis, citation checks, and privilege labels may be incorrect or stale.

Mitigation: Require qualified legal review, verify current law and cited sources, and keep the skill's disclaimer that outputs do not constitute legal advice.

## Reference(s):

- [Legal Doc Reviewer on ClawHub](https://clawhub.ai/thcjp/skills/legal-doc-reviewer)
- [National Laws and Regulations Database](https://flk.npc.gov.cn)
- [PKULaw](https://www.pkulaw.com)
- [China Judgments Online](https://wenshu.court.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with risk labels, source notes, action lists, disclaimers, and suggested revisions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local review artifacts under output/{id}/ paths and may process sensitive legal documents; outputs require human legal review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
