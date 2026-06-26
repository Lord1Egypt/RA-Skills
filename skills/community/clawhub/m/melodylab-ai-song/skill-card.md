## Description: <br>
ZeeLin Music helps an agent generate complete AI songs from a short prompt, including vocal or instrumental tracks across styles such as pop, rock, folk, and electronic music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjiangliu9-tech](https://clawhub.ai/user/dongjiangliu9-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create AI-generated songs from creative prompts, selected styles, moods, lyrics, or instrumental requests. The workflow requires the user's ZeeLin App-Key for balance checks and paid music generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to paste a reusable ZeeLin billing App-Key into the agent flow and sends that key to MelodyLab for charge handling. <br>
Mitigation: Use a low-balance or easily revocable key, confirm the 200-credit charge before generation, and rotate the key when the skill is no longer needed. <br>
Risk: Creative prompts, lyrics, style preferences, and generated-song requests are sent to MelodyLab and downstream music-generation services. <br>
Mitigation: Avoid sensitive personal content in prompts or lyrics, and review the service privacy terms before using the skill with confidential material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dongjiangliu9-tech/melodylab-ai-song) <br>
- [MelodyLab Homepage](https://melodylab.top) <br>
- [ZeeLin Skill Platform](https://skills.zeelin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown with generated lyrics, status updates, billing summaries, and external audio links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audio and image URLs returned by MelodyLab or Suno.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
