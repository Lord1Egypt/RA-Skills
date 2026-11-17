## Description:

Recommends arXiv papers for team members by reading research profiles from PostgreSQL, applying rule-based matching, and producing OpenClaw reranking and personal-card payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhcolin0313](https://clawhub.ai/user/zhcolin0313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research operations teams use this skill to generate per-member literature recommendation candidates from stored research preferences and recent arXiv papers. The skill returns structured payloads that OpenClaw can rerank and deliver as personal recommendation cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Member profile data may be included in downstream reports and reranking payloads.

Mitigation: Limit reranking payloads to the profile fields needed for matching and avoid printing full reports to orchestration logs.

Risk: External paper content from arXiv may influence downstream LLM reranking.

Mitigation: Treat paper titles and abstracts as untrusted content and isolate them from system or developer instructions during reranking.

Risk: Runtime dependencies are specified as version ranges rather than a reviewed lock file.

Mitigation: Pin dependencies in a reviewed lock file before installing in production or sensitive environments.

Risk: Database access and saved output reports may expose member preference data.

Mitigation: Use a least-privilege PostgreSQL account scoped to this skill's tables and apply retention controls to the output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhcolin0313/skills/literature-recommendation)
- [arXiv API](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [json, markdown, guidance]

**Output Format:** [JSON reports containing OpenClaw reranking payloads and Feishu personal-card objects with Markdown card text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PostgreSQL profile data and writes run reports to the configured output directory.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
