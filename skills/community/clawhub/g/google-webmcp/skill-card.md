## Description: <br>
Connects to Google Search and Gemini through the built-in local-mcp Google adapter and a fixed UXC link for searches, Gemini chat, and generated image downloads from an authenticated browser profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Google web searches, interact with Gemini, check authentication state, and download visible generated images through a managed Google browser profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a persistent authenticated Google browser profile. <br>
Mitigation: Use an isolated Google profile or account and verify authentication state before running Gemini actions. <br>
Risk: Gemini image generation can save generated images locally. <br>
Mitigation: Check where downloads are saved before using the skill with sensitive prompts or content. <br>
Risk: Browser navigation outside the intended Google surfaces could expose the managed profile to unrelated sites. <br>
Mitigation: Keep navigation on Google-owned hosts and use the fixed Google link created by the helper script. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Link Creation Helper](scripts/ensure-links.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use JSON arguments and expect JSON responses with ok/data or ok/error envelopes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
