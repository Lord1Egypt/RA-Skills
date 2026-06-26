## Description: <br>
Converts novel chapters into MP3 audiobooks by analyzing narration and dialogue, assigning character voices, optionally generating background music, and assembling the final audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lws-lzh](https://clawhub.ai/user/lws-lzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, audiobook producers, and developers can use this skill to turn chapter text or chapter files into narrated MP3 audiobook output with per-character voice assignment and optional mood-matched background music. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chapter text is sent to DeepSeek and MiniMax during analysis, text-to-speech, and music generation. <br>
Mitigation: Use the skill only with manuscript content that is permitted under the providers' terms and retention practices; avoid confidential, unpublished, or contract-restricted text unless those terms are acceptable. <br>
Risk: The skill requires DeepSeek and MiniMax API keys stored in configuration. <br>
Mitigation: Store API keys securely, avoid committing populated configuration files, and rotate keys if they are exposed. <br>
Risk: Generated audio and temporary files are written to configured output paths. <br>
Mitigation: Review output paths before running the scripts so generated MP3 and temporary files are written only to intended locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lws-lzh/novel-to-audiobook-hznuyx17) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lws-lzh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Audio files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON intermediate results, and MP3 audiobook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DeepSeek and MiniMax API keys; generated outputs can include temporary analysis JSON, temporary MP3 segments, optional background music, and a final MP3 audiobook.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
