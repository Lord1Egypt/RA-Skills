## Description: <br>
Core peaq-robotics-ros2 runtime for OpenClaw. Start/stop ROS 2 nodes and call DID, storage, and access-control services. Use when requests are about running an existing peaq ROS2 workspace (not installing/building or sending funds). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lavish0000](https://clawhub.ai/user/lavish0000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and robotics engineers use this skill to operate an existing peaq ROS 2 workspace through OpenClaw, including node lifecycle commands and DID, storage, and access-control service calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start background ROS 2 nodes and call DID, storage, and access-control services in an existing peaq robotics workspace. <br>
Mitigation: Verify PEAQ_ROS2_ROOT and configuration paths before use, approve identity or access-control mutations deliberately, and stop background ROS nodes when finished. <br>
Risk: Incorrect JSON inputs or paths could lead to failed service calls or unintended workspace data use. <br>
Mitigation: Use the skill's JSON validation and built-in file path restrictions, and review JSON payloads before passing them to ROS 2 services. <br>
Risk: The skill depends on an externally initialized ROS 2 and peaq-robotics-ros2 environment. <br>
Mitigation: Confirm ROS 2, the built workspace, the config YAML, and the current shell environment are ready before running core commands. <br>


## Reference(s): <br>
- [peaq-robotics-ros2 service map](references/peaq_ros2_services.md) <br>
- [ClawHub release page](https://clawhub.ai/lavish0000/peaq-robotics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local ROS 2 helper scripts when the required workspace and environment are already configured.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
