## Description: <br>
Interpret Alpha and Beta diversity metrics from 16S rRNA sequencing results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and researchers use this skill to analyze OTU/ASV tables and sample metadata, interpret Alpha and Beta diversity metrics, and produce reproducible microbiome diversity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency and local execution risk from running the microbiome analysis script in the user's environment. <br>
Mitigation: Install in an isolated Python environment and review or pin dependency versions before serious use. <br>
Risk: Input or output path mistakes could read the wrong data or replace an important existing output file. <br>
Mitigation: Confirm the OTU/ASV input, metadata file, output format, and output path before running; avoid pointing output at an important existing file unless replacement is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/microbiome-diversity-reporter) <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [HTML, JSON, or Markdown reports with optional plots and statistical summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files to the requested output path and may include visualizations such as PCoA plots, rarefaction curves, heatmaps, and diversity summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
