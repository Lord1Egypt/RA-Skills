## Description: <br>
Generate 30-second instrumental music via Google Lyria (Vertex AI). Use when user requests music generation, specific styles/keys/instruments, or music iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MeNoPeter](https://clawhub.ai/user/MeNoPeter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate short instrumental WAV tracks for social video, transitions, loops, and rapid music iteration from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google Cloud bearer token in a local configuration file. <br>
Mitigation: Keep the config file private, avoid committing or sharing it, use restrictive file permissions, and use a least-privilege Google Cloud project. <br>
Risk: Prompts are sent to Google Vertex AI for music generation. <br>
Mitigation: Avoid putting sensitive or confidential information in prompts. <br>
Risk: Bearer tokens expire periodically and can interrupt generation. <br>
Mitigation: Refresh the token with the documented Google Cloud command before long sessions or after authentication failures. <br>


## Reference(s): <br>
- [Google AI music generation documentation](https://ai.google.dev/gemini-api/docs/music-generation) <br>
- [ClawHub release page](https://clawhub.ai/MeNoPeter/google-lyria-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated WAV file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one or more 30-second instrumental WAV files through Google Vertex AI and saves them to the configured workspace output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
