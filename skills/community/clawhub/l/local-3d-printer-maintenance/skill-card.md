## Description: <br>
Offline assistant for FDM 3D printer troubleshooting, maintenance guidance, image analysis, calibration G-code, profile management, and log export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redtechsupplylabs](https://clawhub.ai/user/redtechsupplylabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
3D printer owners, makers, and operators use this skill to troubleshoot FDM print failures, follow maintenance procedures, analyze failed-print images, generate calibration G-code, manage tuning profiles, and export maintenance logs while keeping work local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated calibration G-code may contain machine instructions that are unsuitable for a user's exact printer. <br>
Mitigation: Inspect generated G-code in a slicer or text viewer, verify temperatures and movement limits, and test cautiously before running it. <br>
Risk: Exported profiles and CSV maintenance logs may include printer-specific settings or maintenance history. <br>
Mitigation: Review where profiles and logs are saved and check exported CSVs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redtechsupplylabs/local-3d-printer-maintenance) <br>
- [Publisher profile](https://clawhub.ai/user/redtechsupplylabs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated printer-related files such as calibration G-code, profiles, and CSV logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Ollama models through OpenClaw; generated files should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
