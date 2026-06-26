## Description: <br>
Generates AI music, background music, and songs from text prompts using IMA Studio models including Suno and DouBao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create generated music, background tracks, jingles, soundtrack drafts, and song prototypes from text prompts. It is best understood as a text-to-music integration rather than a voiceover or narration tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published voiceover and narration description conflicts with the actual music-generation workflow. <br>
Mitigation: Present and review the skill as an AI music, song, and BGM generator before installation or use. <br>
Risk: Prompts and IMA_API_KEY are sent to IMA's API and generation may spend IMA credits. <br>
Mitigation: Use only prompts and credentials appropriate for IMA Studio, monitor credit usage, and confirm users understand the external API dependency. <br>
Risk: The script exposes a --base-url option that can redirect requests away from the default endpoint. <br>
Mitigation: Use the default api.imastudio.com endpoint unless the replacement endpoint is fully trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/ima-voice-ai) <br>
- [IMA homepage](https://www.imaclaw.ai) <br>
- [SKILL-DETAIL.md](artifact/SKILL-DETAIL.md) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON result objects containing generated audio URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY and may consume IMA credits; results are remote audio URLs rather than local downloads.] <br>

## Skill Version(s): <br>
1.0.14 (source: server-resolved release metadata; artifact files report internal version 1.2.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
