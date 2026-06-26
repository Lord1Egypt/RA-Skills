## Description: <br>
Diagnose 3D print failures from symptoms or images, recommend slicer setting fixes, and log or analyze recurring print problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Makers, 3D printing operators, and support engineers use this skill to diagnose failed prints, choose slicer setting changes, record failures, and review recurring printer or material patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local failure logs and saved reports can contain printer names, materials, slicer settings, descriptions, fixes, and notes. <br>
Mitigation: Avoid entering sensitive personal or business details unless local retention is acceptable, and delete or redact logs and reports when they are no longer needed. <br>
Risk: Suggested slicer changes may not match every printer, filament, or operating environment. <br>
Mitigation: Apply recommendations as starting points, verify them against the printer and material in use, and test changes incrementally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/print-failure-analyst) <br>
- [3D Print Failure Types](references/failure-types.md) <br>
- [Slicer Setting Fixes](references/slicer-fixes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional structured JSON diagnostics and local markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local failure logs and saved report files when the user requests logging or reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
