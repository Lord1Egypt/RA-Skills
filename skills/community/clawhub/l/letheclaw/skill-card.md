## Description: <br>
Use letheClaw to store, search, and manage memories with criticality and provenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoahTheron](https://clawhub.ai/user/JoahTheron) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let agents store, search, update, and explain memories through a configured letheClaw API endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send remembered or observed information to a network service without enough privacy disclosure. <br>
Mitigation: Use only a trusted HTTPS letheClaw endpoint, avoid storing secrets or sensitive personal data, and disclose what is sent and retained before use. <br>
Risk: The skill may save memories when the user has not clearly approved retention. <br>
Mitigation: Require explicit confirmation before saving any memory and prefer user-provided source labels such as operator_input, direct_observation, or inferred. <br>
Risk: Raw shell command examples could be unsafe if user-controlled values are interpolated directly. <br>
Mitigation: Review generated commands before execution and avoid direct interpolation of untrusted query, tag, or memory identifier values. <br>


## Reference(s): <br>
- [letheClaw Skill Page](https://clawhub.ai/JoahTheron/letheclaw) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [ClawHub Publishing Documentation](https://openclawdoc.com/docs/skills/clawhub/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request or response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted HTTPS letheClaw API endpoint and explicit user confirmation before saving memories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
