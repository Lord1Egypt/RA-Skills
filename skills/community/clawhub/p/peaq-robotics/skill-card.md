## Description:

Core peaq-robotics-ros2 runtime for OpenClaw. Start/stop ROS 2 nodes and call DID, storage, and access-control services. Use when requests are about running an existing peaq ROS2 workspace (not installing/building or sending funds).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lavish0000](https://clawhub.ai/user/lavish0000)

### License/Terms of Use:


## Use Case:

Developers and robotics engineers use this skill to operate an existing peaq ROS 2 workspace from an agent, including local node lifecycle actions and DID, storage, and access-control service calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start long-running local ROS 2 node processes.

Mitigation: Use a private log and PID directory, monitor started processes, and stop background nodes when the task is complete.

Risk: The skill can grant access-control roles and permissions.

Mitigation: Review proposed access-control commands before execution and grant only the minimum role or permission needed.

Risk: The skill depends on an existing ROS 2 workspace and initialized environment.

Mitigation: Confirm ROS 2, the peaq workspace, configuration YAML, and environment setup before running service calls.

## Reference(s):

- [peaq-robotics-ros2 service map](references/peaq_ros2_services.md)
- [ClawHub skill page](https://clawhub.ai/lavish0000/skills/peaq-robotics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local ROS 2 command output and generated JSON payloads.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
