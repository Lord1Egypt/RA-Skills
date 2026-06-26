## Description: <br>
Compares innovation points across multiple research papers in a folder, summarizes each paper, identifies cross-paper similarities or complementarities, and proposes combined research directions for up to 20 papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical reviewers use this skill to compare batches of related papers and find plausible cross-paper research opportunities. It helps agents maintain per-paper progress, summarize innovation points, compare methods and findings, and draft a consolidated comparison report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill instructs agents to run commands and write files without confirmation. <br>
Mitigation: Require explicit user confirmation before package installation, shell commands, or file writes, and run the skill only on a copy of the paper folder or a dedicated output directory. <br>
Risk: The artifact includes a self-evolution workflow that writes diary entries or proposes changes to SKILL.md after execution failures. <br>
Mitigation: Remove or ignore the self-evolution section unless the user explicitly asks for persistent diary files or skill-change proposals. <br>
Risk: Generated paper comparisons and combined research ideas may include unsupported inferences when paper text extraction is incomplete or when the agent extrapolates beyond the cited papers. <br>
Mitigation: Keep direct paper-supported claims separate from hypotheses, mark uncertain ideas clearly, and review the final report before using it for research planning or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/paper-innov-compare-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese research-paper comparison notes, Markdown summaries, JSON progress state, extracted text files, and possible DOCX comparison reports depending on the workflow used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is intended for folders with no more than 20 papers and may write progress files, extracted text, summaries, and final reports into the paper folder or a selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
