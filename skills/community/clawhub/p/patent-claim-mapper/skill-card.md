## Description: <br>
Use when mapping patent claims to products, analyzing patent infringement, or preparing freedom-to-operate analyses. Compares patent claims against product features for biotech and pharmaceutical IP assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent, product, and IP analysis teams use this skill to compare patent claims with biotech or pharmaceutical product features for infringement review, freedom-to-operate assessment, and design-around gap analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads patent and product files from local paths and writes a report to a chosen output path, so unintended files or locations could be used. <br>
Mitigation: Use only patent and product files intentionally provided for the analysis, review input and output paths before execution, and run in a controlled workspace. <br>
Risk: Patent infringement and freedom-to-operate results can be incomplete or legally unreliable if treated as final advice. <br>
Mitigation: Treat generated mappings and risk scores as preliminary analytical support and have qualified patent counsel review any legal or business decision based on them. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a JSON report from the packaged CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided patent claims and product description files; writes a JSON infringement analysis report to the selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
