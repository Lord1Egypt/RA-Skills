## Description:

Compare innovations across multiple academic papers in a folder and produce a rolling summary document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical writers use this skill to process up to 20 papers in a folder, summarize each paper's core problem, methods, innovations, experiments, and workload, and compare related papers for possible combined research directions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paper folder containing symlinks could cause the extraction script to read files outside the intended folder.

Mitigation: Use the skill only on trusted paper folders and avoid folders containing symlinks.

Risk: The skill includes persistence and self-evolution behavior that can write diary entries or propose changes to the skill.

Mitigation: Do not allow diary or SKILL.md PR self-evolution steps unless persistent skill changes are explicitly desired and reviewed manually.

Risk: Running the workflow creates or updates files in the selected paper folder.

Mitigation: Review the target folder before use and expect summ.md, paper_summ_state.json, and extracted_text/ to be created or updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orbisz/skills/multi-paper-innovation-comparator)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Chinese-first Markdown research notebook with JSON state and extracted text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates summ.md, paper_summ_state.json, and extracted_text/ in the paper folder unless a separate output directory is explicitly requested.]

## Skill Version(s):

1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
