## Description: <br>
Sensor calibration toolkit for calibrating IMU magnetometer data with a close-form method that computes soft-iron and hard-iron corrections and uses VQF sensor fusion for orientation estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to calibrate IMU magnetometer data by computing a soft-iron matrix and hard-iron offset from timestamped accelerometer, gyroscope, and magnetometer arrays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python package dependencies could introduce supply-chain risk if installed from untrusted sources or without version control. <br>
Mitigation: Install referenced packages only from trusted sources and prefer pinned dependency versions before using the skill. <br>
Risk: Calibration quality depends on suitable IMU data coverage, matching array shapes, and varied sensor orientations. <br>
Mitigation: Use timestamp, accelerometer, gyroscope, and magnetometer arrays with matching sample counts, and collect data across varied orientations before applying calibration parameters. <br>
Risk: Sensor data is processed in the local Python environment. <br>
Mitigation: Use only sensor datasets that are acceptable to process in that environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may describe calibration usage and Python snippets; the runtime calibration call returns a 3x3 soft-iron matrix and a 3-element hard-iron offset.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
