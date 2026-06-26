## Description: <br>
PatSight-MolVision performs optical chemical structure recognition on molecular structure images, calls the PatSight Patent Extractor API, and returns SMILES/SDF data with optional RDKit-derived properties and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SnailWhb](https://clawhub.ai/user/SnailWhb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, chemistry researchers, and developers use this skill to process one or more molecular structure images, extract SMILES/SDF structures through PatSight, and generate local JSON and PNG reports with molecular properties. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected molecular structure images are sent to PatSight or another configured endpoint for OCSR processing. <br>
Mitigation: Install and run the skill only when that external processing is acceptable, and keep the default API URL unless a different endpoint is intentionally trusted. <br>
Risk: Authentication can use PatSight account credentials or tokens. <br>
Mitigation: Use a dedicated PatSight token or account where possible, store credentials in environment variables, and avoid passing passwords directly on the command line. <br>
Risk: Recognition and RDKit-derived properties may be incomplete or unavailable for some images or molecules. <br>
Mitigation: Review the JSON results, confidence scores, and report output before using extracted structures or properties in downstream work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SnailWhb/ocsr) <br>
- [PatSight homepage](https://patent.xinsight-ai.com/home) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is JSON result files and PNG dashboard report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include raw API responses, enriched RDKit properties when RDKit can parse the result, source image references, and visualization dashboards.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
