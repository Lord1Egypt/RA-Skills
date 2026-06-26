## Description: <br>
Use when the user asks for a hello, a greeting, says hi, or wants to test that the hello-world plugin is loaded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin-li-okg](https://clawhub.ai/user/kevin-li-okg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route simple greeting or plugin-test requests to the hello-world OpenClaw plugin and return its greeting text directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may trigger on ordinary greetings such as hi. <br>
Mitigation: Install it only when automatic greeting-tool behavior is desired and keep the exposed tool allowlist limited to hello. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kevin-li-okg/hello-world-test) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Plain text greeting returned through the agent response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional name parameter; defaults to world when omitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
