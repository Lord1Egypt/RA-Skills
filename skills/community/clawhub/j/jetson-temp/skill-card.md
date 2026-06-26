## Description: <br>
Monitors CPU, GPU, and thermal zone temperatures on NVIDIA Jetson devices running Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxd9199](https://clawhub.ai/user/wxd9199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Jetson operators use this skill to check local device temperatures from Linux thermal sensor files while diagnosing thermal behavior or monitoring system health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a shell script that reads local thermal sensor files. <br>
Mitigation: Review the script before use and run it without elevated privileges on systems where local thermal sensor access is expected. <br>
Risk: On non-Jetson systems or Linux systems without thermal subsystem support, output may be incomplete or unavailable. <br>
Mitigation: Use the skill on NVIDIA Jetson hardware with Linux thermal subsystem support and treat missing readings as an environment compatibility issue. <br>


## Reference(s): <br>
- [ClawHub skill page: Jetson Temperature](https://clawhub.ai/wxd9199/jetson-temp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command snippets and terminal output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local /sys/class/thermal thermal sensor files; no credentials, network access, admin privileges, or background execution are expected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
