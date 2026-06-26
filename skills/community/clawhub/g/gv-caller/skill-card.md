## Description: <br>
Uses Google Voice to automatically place calls and play AI-generated speech or local audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to trigger Google Voice outbound calls from an agent workflow, including spoken TTS messages or local audio playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored Google session cookies can grant account access if exposed or reused outside the intended environment. <br>
Mitigation: Use a dedicated low-risk Google Voice account, isolate the runtime environment, and protect or avoid reusable Google cookies. <br>
Risk: Broad call triggers could place unintended or costly outbound calls without sufficient confirmation. <br>
Mitigation: Disable broad auto-invocation and require explicit human confirmation of the phone number, message or audio, duration, and expected cost before every call. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joe12801/gv-caller) <br>
- [Google Voice calls page](https://voice.google.com/u/0/calls) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces outbound call actions through Google Voice when configured with required account cookies and runtime dependencies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
