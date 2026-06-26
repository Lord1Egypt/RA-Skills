## Description: <br>
Extract semantic relationships from long narratives, architectures, or complex discussions using RDF-style triple notation and generate adjacency matrices that reveal narrative structure, dependency graphs, and critical paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and analysts use this skill to mark relationships in markdown narratives and produce graph-friendly adjacency matrices for dependency, causality, workflow, or technical-debt analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local scanner recursively reads matching files beneath the directory where it is run. <br>
Mitigation: Run it only from a dedicated folder containing the documents intended for analysis, not from a home directory or broad repository root. <br>
Risk: Extracted graph output can reveal relationship structure from sensitive source documents. <br>
Mitigation: Review source documents and output before sharing adjacency matrices, node lists, or statistics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turinfohlen/narrative-topology) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, text] <br>
**Output Format:** [Markdown guidance with Python code and shell commands; scanner output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner output includes node lists, compressed x::n adjacency matrix rows, and graph statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
