## Description:

Turbocharge YOLO26 on Intel AI PCs with Ultralytics + OpenVINO by exporting compressed FP32/INT8 OpenVINO models, deploying live camera or video inference, switching execution across CPU/GPU/NPU, benchmarking acceleration, and building local vision workflows such as people counting, inventory counting, and safety-zone alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuo-yoyowz](https://clawhub.ai/user/zhuo-yoyowz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to export YOLO26 models to OpenVINO FP32 or INT8, run local camera or video inference on Intel CPU/GPU/NPU devices, compare performance, and build local vision workflows such as people counting, inventory counting, and safety-zone alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live camera, people-counting, safety-zone, event-log, and output-video modes can process or record people or sensitive spaces.

Mitigation: Run these modes only where monitoring or recording is authorized, keep outputs local when possible, and handle generated logs or videos under the user's retention and privacy policy.

Risk: Setup and first export can download Python packages, model weights, and INT8 calibration data, and the dependency list is not fully pinned.

Mitigation: Install in an isolated virtual environment without administrator privileges, review or pin dependencies before use, and prefer trusted cached model and calibration assets where available.

Risk: Object detection can produce false positives or false negatives, especially when used for safety-zone or inventory decisions.

Mitigation: Use stable-frame confirmation, cooldowns, and human review for consequential actions; do not rely on the demo as the sole safety or compliance control.

## Reference(s):

- [Downstream Playbooks](references/downstream_playbooks.md)
- [Performance Notes](references/performance_notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline PowerShell, shell, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local OpenVINO model folders, benchmark metrics, CSV event logs, or optional rendered video files depending on the selected workflow.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
