## Description: <br>
Generate MV (Music Video) with AI-driven storyboarding, image generation, and video synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bajie-git](https://clawhub.ai/user/bajie-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn an uploaded audio file into a generated music video with a selected visual style and landscape or portrait aspect ratio. The agent guides parameter collection, uploads the audio to ohyesai.com, submits the generation task, polls for completion, and returns the video link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the selected audio file to ohyesai.com for processing. <br>
Mitigation: Use audio that you own or are licensed to process, and avoid sensitive voice recordings unless you accept the provider handling them. <br>
Risk: The documented API examples place OHEYSAI_API_KEY in URL query parameters, which can appear in logs. <br>
Mitigation: Protect the API key, avoid sharing logs that include request URLs, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bajie-git/ohyesai-mv) <br>
- [Publisher profile](https://clawhub.ai/user/bajie-git) <br>
- [OhYesAI homepage](https://ohyesai.com) <br>
- [OhYesAI API key page](https://ohyesai.com?from=https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request details, parameter prompts, progress updates, and a final video link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OHEYSAI_API_KEY, curl, and sleep; accepts audio files up to 50MB and supports LANDSCAPE or PORTRAIT output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
