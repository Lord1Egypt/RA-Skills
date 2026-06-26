## Description: <br>
Turbocharge YOLO26 on Intel AI PCs with Ultralytics + OpenVINO by exporting compressed FP32/INT8 OpenVINO models, deploying live camera or video inference, switching execution across CPU/GPU/NPU, benchmarking acceleration, and building local vision workflows such as people counting, inventory counting, and safety-zone alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuo-yoyowz](https://clawhub.ai/user/zhuo-yoyowz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to export YOLO26 models to OpenVINO, run local object detection on Intel AI PCs, compare CPU/GPU/NPU and FP32/INT8 behavior, and build local vision tasks such as people counting, inventory counting, and safety-zone alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera or video object detection may capture people or sensitive spaces if Source 0 or monitoring-style demos are run unintentionally. <br>
Mitigation: Run camera and video demos only with intentional, visible use that follows applicable laws, workplace rules, and consent expectations. <br>
Risk: The skill can create local CSV logs and optional output videos that may contain sensitive scene information. <br>
Mitigation: Review CSV logs and output videos before sharing, retaining, or using them outside the local workflow. <br>
Risk: Setup and first export may download Python packages, YOLO model weights, and INT8 calibration data when they are not already cached. <br>
Mitigation: Use the skill only in environments where those expected downloads are allowed, or provide already-exported OpenVINO model folders for local inference. <br>


## Reference(s): <br>
- [Downstream Playbooks](artifact/references/downstream_playbooks.md) <br>
- [Performance Notes](artifact/references/performance_notes.md) <br>
- [ClawHub listing](https://clawhub.ai/zhuo-yoyowz/openvino-yolo-aipc) <br>
- [Publisher profile](https://clawhub.ai/user/zhuo-yoyowz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to generate OpenVINO model folders, benchmark console output, CSV event logs, and optional rendered MP4 output videos.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
