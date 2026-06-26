## Description: <br>
Query positions of spacecraft, planets, moons, and asteroids in the solar system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangzesen](https://clawhub.ai/user/huangzesen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and science users use this skill to query solar-system ephemeris data, compute distances, transform coordinate frames, list supported missions and frames, and manage local SPICE kernel data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path adds the heliospice Python package to the user's environment. <br>
Mitigation: Install in a virtual environment and pin or verify the package version before use. <br>
Risk: Kernel management can download or purge local cached ephemeris files. <br>
Mitigation: Review manage_kernels actions before execution and keep important local kernel files backed up or reproducible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huangzesen/heliospice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and structured query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on the heliospice Python package and local SPICE kernel cache state.] <br>

## Skill Version(s): <br>
0.4.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
