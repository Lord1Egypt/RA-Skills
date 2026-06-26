## Description: <br>
Organizes scattered metric definitions into a catalog of definitions, formulas, ownership, exceptions, common misuses, and maintenance notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analytics, data, and operations teams use this skill to turn metric lists, definition fragments, and calculation notes into reviewable Markdown catalogs for governance, dashboard alignment, and cross-team consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script contains unused audit and scanning paths beyond the advertised metrics-catalog workflow. <br>
Mitigation: Use the default structured metric-catalog workflow unless broader local-file inspection is intentionally needed, and review generated Markdown before acting on it. <br>
Risk: Metric catalogs can become misleading when inputs omit ownership, formula details, exceptions, or conflicting definitions. <br>
Mitigation: Treat outputs as review drafts, keep unresolved items in the generated confirmation list, and avoid inventing missing metric sources or BI configuration details. <br>
Risk: Inputs may include sensitive business metrics or personal information. <br>
Mitigation: Use scoped, non-sensitive or redacted inputs before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/metric-definition-catalog) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Structured metric catalog specification](resources/spec.json) <br>
- [Output template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON output from the bundled Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review drafts, explicit missing-information notes, and next-step suggestions; it does not modify external systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
