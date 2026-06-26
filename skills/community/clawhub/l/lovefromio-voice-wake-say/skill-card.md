## Description: <br>
Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to have an agent acknowledge and optionally speak responses aloud when the latest message begins with the Voice Wake trigger phrase. It is intended for macOS environments that provide the local `say` command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Responses may be spoken aloud in the local environment when the exact Voice Wake trigger phrase is present. <br>
Mitigation: Check each latest message independently, require the trigger phrase at the very start, and speak a concise summary for long or code-heavy responses. <br>
Risk: The macOS `say` command may be unavailable or fail in non-macOS or restricted environments. <br>
Mitigation: Return the normal text response and notify the user that local text-to-speech failed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovefromio/lovefromio-voice-wake-say) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and spoken text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local macOS text-to-speech via `say`; falls back to text-only responses if `say` is unavailable or errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
