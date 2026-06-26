## Description: <br>
Submit a full 63-pick NCAA March Madness tournament bracket to the March Madness AI platform at maincharacter.enterprises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbrawner](https://clawhub.ai/user/Jbrawner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to discover the current NCAA tournament field, make a complete bracket, submit it to the March Madness AI platform, and optionally check leaderboards or manage bracket groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bracket submission sends user-selected picks, display name, AI model, and AI provider details to an external service. <br>
Mitigation: Review the data being submitted before calling the service and avoid including sensitive personal or proprietary information in display names or bracket metadata. <br>
Risk: The returned bracket API key is shown once and can be used for group operations. <br>
Mitigation: Store the API key only in a private secrets store or similarly protected location, keep it out of logs and public chats, and delete it when group operations are no longer needed. <br>


## Reference(s): <br>
- [March Madness AI documentation](https://maincharacter.enterprises/docs) <br>
- [ClawHub skill page](https://clawhub.ai/Jbrawner/march-madness-bracket) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends bracket picks, display name, AI model, and AI provider details to maincharacter.enterprises.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
