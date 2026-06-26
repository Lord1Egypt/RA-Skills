## Description: <br>
Migration Runbook Generator turns migration plans into reviewable runbooks with cutover windows, prerequisites, rollback plans, and acceptance signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to convert migration scope, timing, dependencies, rollback requirements, and validation needs into a structured runbook draft for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated runbooks may contain incomplete or incorrect operational guidance if source migration details are missing. <br>
Mitigation: Review the generated draft before operational use and require explicit confirmation of missing scope, dependency, timing, rollback, and validation details. <br>
Risk: Migration inputs may contain sensitive infrastructure or personal data. <br>
Mitigation: Use scoped input files and redact sensitive migration details before processing or sharing generated runbooks. <br>
Risk: The bundled helper reads a chosen input and writes to a chosen output path. <br>
Mitigation: Review the local Python script when provenance matters and choose safe, intended output paths. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/52YuanChangXing/migration-runbook-generator) <br>
- [README](artifact/README.md) <br>
- [Runbook Specification](artifact/resources/spec.json) <br>
- [Runbook Template](artifact/resources/template.md) <br>
- [Example Input](artifact/examples/example-input.md) <br>
- [Example Output](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown runbook draft or JSON report from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pre-checks, migration steps, cutover window, validation signals, rollback plan, responsibilities, pending confirmations, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
