## Description: <br>
Omniscient combines cognitive prompting, code execution guidance, and Windows system-control scripts to help an agent plan and carry out multi-step automation across desktop software, hardware, peripherals, network devices, IoT endpoints, and GUI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation users can use this skill to route a task into reasoning, code-generation, or Windows device-control workflows. It is most relevant when an agent needs to propose commands, generate scripts, inspect system state, or coordinate local desktop, hardware, network, Bluetooth, IoT, audio, camera, printing, scanning, and GUI actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local system-control automation can affect windows, processes, hardware settings, network configuration, peripherals, and IoT devices. <br>
Mitigation: Install only when this level of local control is intentional, review proposed commands before execution, and use a controlled environment for testing. <br>
Risk: The skill can interact with sensitive inputs and outputs, including WiFi passwords, OAuth-style tokens, camera capture, microphone recording, screenshots, and screen automation. <br>
Mitigation: Avoid exposing live credentials or private screens in logs, prefer environment variables for tokens, and do not run camera, microphone, or screenshot actions unless explicitly needed. <br>
Risk: Some helper scripts may install Python packages at runtime. <br>
Mitigation: Run the skill in a dedicated virtual environment and review dependency installation behavior before use on sensitive systems. <br>


## Reference(s): <br>
- [Command Reference](artifact/references/command_reference.md) <br>
- [Security Review Checklist](artifact/references/security_checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/omniscient) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, JSON command results, and human-readable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Python scripts, command sequences, system-control instructions, and summarized execution results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
