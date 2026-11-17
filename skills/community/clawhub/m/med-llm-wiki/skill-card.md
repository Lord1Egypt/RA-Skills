## Description:

Med-LLM-Wiki helps agents organize patient-centered clinical consultation material into a structured medical wiki for precise retrieval and evidence-aware reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingf](https://clawhub.ai/user/zhangyingf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical knowledge-base maintainers use this skill to convert patient backgrounds, consultations, interventions, and medical concepts into a linked wiki structure. It is intended to preserve clinical details and cross-references so agents can answer targeted questions from the organized wiki.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and indexes sensitive patient health details without built-in privacy or retention safeguards.

Mitigation: Use it only with authority to process the data, de-identify records before ingestion, keep generated wiki files in protected locations, and define retention and deletion practices before using real cases.

Risk: Generated patient wiki files could expose clinical details if committed to public or shared repositories.

Mitigation: Exclude generated patient files from source control and avoid public or shared repositories for real clinical data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyingf/skills/med-llm-wiki)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown files with YAML frontmatter and wiki-style cross-links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured wiki page layouts, indexing guidance, and maintenance checklists.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
