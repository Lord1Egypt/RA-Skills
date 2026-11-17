## Description:

Sensor calibration toolkit with magnetometer calibration using close-form method for calibrating IMU sensors and computing soft-iron matrix and hard-iron offset correction parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to apply a Python magnetometer calibration workflow to IMU sensor data and produce correction parameters for raw magnetometer readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Python calibration packages from the runtime environment.

Mitigation: Confirm that pywayne, vqf, and qmt are installed from trusted sources before using the calibration workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/magnetometer-calibration)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with inline Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces usage guidance for computing a soft-iron matrix and hard-iron offset vector; no executable code is included in the skill artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
