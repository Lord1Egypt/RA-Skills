## Description: <br>
Adapts OpenClaw agents by learning user interaction patterns, switching personas by context, and evolving personality weekly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngmeyer](https://clawhub.ai/user/ngmeyer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to initialize and maintain local persona files, switch between context modes, analyze workspace memory for interaction patterns, and generate weekly evolution suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI command dispatcher can run unsafe shell commands when untrusted text is passed as arguments. <br>
Mitigation: Do not pass untrusted text to the CLI until argument handling is fixed, and review commands before execution. <br>
Risk: The skill can persist sensitive personality profile data and generated context from workspace memory. <br>
Mitigation: Install only if local personality profiling is acceptable, keep PERSONA and evolution files private, and review them regularly. <br>
Risk: Heartbeat automation can analyze workspace memory automatically. <br>
Mitigation: Enable heartbeat automation only after confirming which workspace it will analyze. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ngmeyer/personality-dynamics) <br>
- [Publisher profile](https://clawhub.ai/user/ngmeyer) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local PERSONA files and mode state in the active workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
