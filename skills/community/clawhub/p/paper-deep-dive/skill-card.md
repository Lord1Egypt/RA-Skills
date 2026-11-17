## Description:

Paper Deep Dive helps agents produce structured, evidence-driven Chinese-language deep dives for a single academic paper, including research context, method explanation, claim-to-evidence analysis, limitations, and follow-up reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom-zju](https://clawhub.ai/user/tom-zju)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, technical writers, and engineers use this skill to convert a focal paper and supporting sources such as PDFs, arXiv pages, appendices, project pages, or official code into a detailed paper analysis. It is especially suited for blog drafts, technical talks, research discussions, method walkthroughs, and checking whether experiments support the paper's claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Chinese-language paper analysis, which may not match every deployment's reader language.

Mitigation: Tell the agent the required output language when installing or invoking the skill for a non-Chinese audience.

Risk: Paper analysis can overstate unsupported claims when source material is incomplete or only an abstract is available.

Mitigation: Require use of the skill's limited deep-dive posture for title-and-abstract inputs and ask the agent to label unsupported points as unverified.

## Reference(s):

- [Paper Deep Dive Source](artifact/SKILL.md)
- [Paper Deep Dive - Evidence Rules and Uncertainty Labels](artifact/references/evidence-rules.md)
- [Paper Deep Dive - Full Output Template](artifact/references/output-template.md)
- [Paper Deep Dive - Paper Type Adaptation Guide](artifact/references/paper-types.md)
- [Paper Deep Dive - Quick Reference](artifact/references/quickref.md)
- [Paper Deep Dive - Visualization Guidelines](artifact/references/visualization.md)
- [Paper Deep Dive - Complete Example](artifact/references/example-attention.md)
- [ClawHub Skill Page](https://clawhub.ai/tom-zju/skills/paper-deep-dive)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown, typically in Chinese, with tables and optional Mermaid diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce standard, deep-dive, or limited deep-dive variants depending on the user's source material.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
