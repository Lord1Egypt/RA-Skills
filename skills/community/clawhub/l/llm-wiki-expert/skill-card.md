## Description:

Helps individuals and small teams design, build, and operate an agent-maintained Markdown knowledge base through source-grounded ingestion, compilation, querying, maintenance, audits, and evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and small teams use this skill to create and maintain Markdown knowledge bases with traceable sources, evidence-based answers, and repeatable quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cloud embeddings can transmit selected document and query text to an external provider, and saved queries may retain sensitive material.

Mitigation: Keep credentials out of Wiki sources and logs, decide what questions and answers may be retained, and use approved cloud processing or local search for confidential material.

Risk: Global installation examples use automatic confirmation and may run code from an installer or source revision that has not been reviewed.

Mitigation: Review and pin the installer and source revision before using those examples.

## Reference(s):

- [Information Architecture Playbook](references/information-architecture-playbook.md)
- [Source Grounding Playbook](references/source-grounding-playbook.md)
- [Retrieval and Synthesis Playbook](references/retrieval-and-synthesis-playbook.md)
- [Maintenance and Governance Playbook](references/maintenance-governance-playbook.md)
- [Quality and Evaluation Playbook](references/quality-evaluation-playbook.md)
- [RAG Retrieval Playbook](references/rag-retrieval-playbook.md)
- [Wiki Lifecycle Playbook](references/wiki-lifecycle-playbook.md)
- [Karpathy LLM Wiki reference](https://skills.sh/astro-han/karpathy-llm-wiki/karpathy-llm-wiki)
- [OrchestKit RAG retrieval reference](https://skills.sh/yonatangross/orchestkit/rag-retrieval)
- [Diataxis documentation reference](https://github.com/mcollina/skills/tree/main/documentation)
- [LLM Wiki skill reference](https://github.com/lewislulu/llm-wiki-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown guidance with optional code, shell commands, and wiki templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or revise Wiki pages, indexes, manifests, audit reports, and retrieval plans based on supplied sources.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
