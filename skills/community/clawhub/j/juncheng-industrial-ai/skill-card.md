## Description: <br>
郡城工业AI helps agents analyze PLC code, draft industrial automation PLC frameworks, diagnose equipment faults, and generate SCADA sensor reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liwiw](https://clawhub.ai/user/liwiw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industrial automation engineers use this skill to review PLC ladder, SCL, and STL logic; draft PLC program frameworks from process flows; investigate equipment alarms with historical data; and produce SCADA daily, weekly, or monthly reports from sensor data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PLC logic, diagnostics, or SCADA reports may be incomplete or incorrect for a live industrial environment. <br>
Mitigation: Require qualified engineering review and safe testing before applying outputs to real equipment or operations. <br>
Risk: Alarm-code and historical-data analysis may not capture all site-specific operating conditions. <br>
Mitigation: Use the skill's findings as draft troubleshooting guidance and verify them against plant procedures, instrumentation, and maintenance records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liwiw/juncheng-industrial-ai) <br>
- [Artifact skill description](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown or text with PLC code/framework snippets and SCADA report tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Treat generated PLC logic, diagnostics, and operational recommendations as engineering drafts requiring qualified review and safe testing before use on real equipment.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
