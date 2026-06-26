## Description: <br>
Deep-read research papers into source-aware reports, traceable claim evidence, and research-direction seeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and engineers use this skill to turn research papers, LaTeX sources, appendices, code notes, peer reviews, and related material into grounded deep-reading reports, traceability artifacts, and testable research-direction seeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may access more paper or source files than needed for a reading task. <br>
Mitigation: Provide a narrow input directory and a local output path for each run. <br>
Risk: Online paper sources, successor papers, or review material retrieved by the agent may be incomplete or mismatched. <br>
Mitigation: Verify retrieved sources against title, authors, venue, year, abstract, and source links before relying on the report. <br>
Risk: Unpinned markdown and pyyaml dependency ranges may change behavior in controlled environments. <br>
Mitigation: Pin or audit markdown and pyyaml versions before deployment in controlled environments. <br>
Risk: Registry capability tags include unrelated crypto and purchase indicators. <br>
Mitigation: Treat those tags as publisher metadata that should be corrected before broad distribution; the security evidence reports no risk findings for the package behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/c-narcissus/paper-deep-reading) <br>
- [Artifact Contract](references/artifact_contract.md) <br>
- [Research-Generative Methodology](references/research-generative-methodology.md) <br>
- [Research-Direction Mining Best Practices](references/research-direction-mining-best-practices.md) <br>
- [SyncTeX Locator Notes](references/synctex_locator_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports plus JSON traceability, research-lens, direction-board, LaTeX paragraph, and artifact-index files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are source-aware and claim-anchored; bundled helper scripts validate traceability and direction-board artifacts.] <br>

## Skill Version(s): <br>
1.2.0 (source: skill metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
