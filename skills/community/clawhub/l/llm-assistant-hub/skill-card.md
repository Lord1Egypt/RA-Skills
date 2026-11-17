## Description:

LLM助手中枢 helps agents analyze, compress, and compare long commercial or legal documents using tiered review, chunking, assumption checks, and risk-marked summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to review long contracts, memoranda, proposals, and policies; compare document versions; surface assumptions, contradictions, and risk signals; and produce decision-ready summaries. It is not a substitute for licensed legal advice or deterministic high-stakes decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests exec, write, search, and file-globbing powers that are broader than the stated document-analysis purpose.

Mitigation: Review before installation and prefer a narrowed version that removes exec and write unless a concrete workflow requires them.

Risk: Credential and integration guidance is inconsistent, with the artifact saying both that no API key is needed and that API keys or callbacks may be configured.

Mitigation: Confirm whether credentials, network calls, callbacks, or file writes are required before use, and do not provide secrets unless the requirement is explicit and trusted.

Risk: The skill targets commercial and legal documents, where model outputs can be mistaken for authoritative legal or business determinations.

Mitigation: Use outputs as review support only, preserve uncertainty markers, and route legal, contractual, or regulated decisions to qualified reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/llm-assistant-hub)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown analysis reports with optional JSON, text, or CSV result structure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include document assessment, core logic, risk markers, structural improvements, assumptions, next steps, and version-difference summaries.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
