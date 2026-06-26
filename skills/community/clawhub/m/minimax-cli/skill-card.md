## Description: <br>
MiniMax AI platform CLI - text, image, video, speech, music, vision, and web search from terminal or AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylerdotai](https://clawhub.ai/user/tylerdotai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the MiniMax CLI for text, image, video, speech, music, vision, and web search workflows from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an external CLI package can introduce supply-chain trust risk. <br>
Mitigation: Verify that mmx-cli is the MiniMax CLI package you intend to trust before installing it. <br>
Risk: MiniMax API keys can be exposed through shared terminals, shell history, or scripts. <br>
Mitigation: Use a dedicated or revocable MiniMax API key, prefer environment-variable or interactive secret entry when available, and avoid pasting real keys into shared terminals or scripts. <br>
Risk: Prompts, images, audio, or video sent through the CLI may be processed by MiniMax. <br>
Mitigation: Do not send sensitive prompts or media unless MiniMax processing is acceptable for that data. <br>


## Reference(s): <br>
- [MiniMax CLI Reference Notes](references/api-notes.md) <br>
- [MiniMax Platform](https://platform.minimax.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MiniMax CLI commands and notes for API key setup, quota checks, async video workflow, and region selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
