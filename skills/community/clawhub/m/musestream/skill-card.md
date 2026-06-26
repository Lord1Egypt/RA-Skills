## Description: <br>
AI-Music-Stream helps agents generate AI music from text prompts or user context, return browser-playable stream links, and save generated tracks to a local library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asriverwang](https://clawhub.ai/user/asriverwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up a local MuseStream server, turn natural-language music requests or contextual signals into generation prompts, and share a player URL for continuous browser playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local music server is unauthenticated by default and could expose prompts, saved songs, or paid music API usage if reachable by others. <br>
Mitigation: Keep the server on localhost unless it is protected with authentication, firewall rules, TLS, and rate limiting. <br>
Risk: Generated streams can continue auto-queuing and consume provider credits while the browser session remains active. <br>
Mitigation: Stop the stream or close the browser window when listening is finished, and monitor provider usage. <br>
Risk: Configuration files and the output library can contain API keys, prompts, metadata, or saved songs. <br>
Mitigation: Protect config.json and the output directory, avoid sensitive personal details in prompts or context fields, and stop the background server when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asriverwang/musestream) <br>
- [Sonauto](https://sonauto.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and HTTP endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a local browser player URL and guidance for managing generated audio files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
