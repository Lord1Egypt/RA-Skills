## Description: <br>
Generate interactive HTML sunburst charts for taxonomic abundance hierarchies in metagenomic samples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, bioinformatics analysts, and researchers use this skill to validate metagenomic classification inputs and produce reviewable interactive Krona-style charts from Kraken2, Bracken, or custom TSV data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code with pandas and plotly and reads and writes user-selected files. <br>
Mitigation: Install dependencies in a virtual environment, review or pin dependency versions, and run commands only against intended input and output paths. <br>
Risk: Generated HTML can contain sample or taxonomy details and may load Plotly JavaScript from a CDN when opened. <br>
Mitigation: Treat output HTML as a data-bearing artifact, review it before sharing, and open it in a controlled environment when CDN loading is a concern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/metagenomic-krona-chart) <br>
- [README](README.md) <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>
- [Sample Kraken2 report](example/sample_kraken2.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated artifact is standalone HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Kraken2, Bracken, or custom TSV taxonomy data and writes an interactive HTML chart.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
