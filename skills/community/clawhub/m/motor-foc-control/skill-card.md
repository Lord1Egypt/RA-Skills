## Description: <br>
FOC magnetic field oriented control guide covering FOC principles, SVPWM, MTPA, flux weakening, observer concepts, engineering examples, C code, and a PI tuning script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and motor-control engineers use this skill as an engineering reference for PMSM FOC implementation, tuning, and troubleshooting. It helps agents explain control concepts, produce example control code, run PI tuning calculations, and summarize typical motor-drive parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested gains, thresholds, dead-time values, and flux-weakening settings may be unsuitable for a specific motor-drive system. <br>
Mitigation: Treat all values as examples or initial estimates and validate them against motor, inverter, sensor, datasheet, current-limit, and thermal constraints before applying them. <br>
Risk: Applying generated or example motor-control settings directly to physical hardware can create safety or equipment-damage risk. <br>
Mitigation: Use staged bench validation with current limits, thermal monitoring, and an emergency-stop setup before live operation. <br>


## Reference(s): <br>
- [FOC engineering parameter quick reference](references/foc-quick-ref.md) <br>
- [ClawHub release page](https://clawhub.ai/yongjie666888/motor-foc-control) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with inline C, Python, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calculated PI gains, SVPWM examples, FOC parameter tables, and troubleshooting steps for review before hardware use.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
