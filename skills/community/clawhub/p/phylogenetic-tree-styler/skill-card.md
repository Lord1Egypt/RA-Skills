## Description: <br>
Analyzes and styles phylogenetic tree data using a reproducible workflow with validation and structured, review-ready outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics analysts use this skill to render Newick phylogenetic trees with taxonomy color blocks, bootstrap labels, and optional timelines. It helps produce reproducible image outputs for review and interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input or output paths could accidentally read from or write outside the intended project workspace. <br>
Mitigation: Run the skill in a virtual environment or container and provide input and output paths inside the project workspace. <br>
Risk: Unpinned dependencies can make rendered outputs harder to reproduce across environments. <br>
Mitigation: Pin dependency versions for reproducible use before running analysis for review or release. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/aipoch-ai/phylogenetic-tree-styler) <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the packaged script writes PNG, PDF, or SVG tree images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Newick tree input file and may use an optional taxonomy CSV, bootstrap threshold, timeline setting, and image sizing parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
