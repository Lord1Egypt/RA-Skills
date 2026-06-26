## Description: <br>
Jointly analyze a research paper and its open-source implementation. Use when a user wants to understand a paper through code, map theory/formulas/algorithms/experiments to real classes and methods, identify implementation details not disclosed in the paper, produce reproducibility commands and gaps, build explanatory diagrams or a static reader, or validate that an analysis covers both the paper and repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and engineers use this skill in Codex to jointly read a paper and its implementation, map formulas and experiments to real code paths, identify paper-code gaps, and produce reproducibility guidance, diagrams, validation notes, and a reusable static reader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads target papers and source repositories and writes local analysis artifacts, which may expose private project contents in generated reports. <br>
Mitigation: Run it in a dedicated project directory and review generated Markdown, JSON, and reader files before sharing them. <br>
Risk: Reproduction commands or dependency installation can mutate the environment or run untrusted target repository code. <br>
Mitigation: Use static analysis unless execution is explicitly required, and allow dependency installation or experiment runs only after reviewing the target repository instructions. <br>
Risk: The optional static reader can download KaTeX font files when full local typography is requested. <br>
Mitigation: Use the font-install option only when network access and local asset creation are acceptable; otherwise build the reader without downloading fonts. <br>
Risk: Paper-code mappings and reproducibility commands can be incomplete or misleading if paper claims, source files, or line references are not rechecked. <br>
Mitigation: Use the bundled validation scripts and require unresolved questions, unsupported experiments, and approximate commands to be recorded in the validation report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/c-narcissus/paper-code-joint-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/c-narcissus) <br>
- [Output contract](references/output-contract.md) <br>
- [Reader data contract](references/reader-data-contract.md) <br>
- [Analysis bundle schema](references/analysis-bundle.schema.json) <br>
- [Deep reading overlay](references/deep-reading-overlay.md) <br>
- [Large artifact policy](references/large-artifact-policy.md) <br>
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, a structured analysis_bundle.json file, Mermaid diagrams, validation output, shell commands, and a generated static HTML reader.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default user-facing reports and reader labels are Chinese while paper titles, code identifiers, paths, commands, class names, method names, and standard acronyms remain in their original form.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
