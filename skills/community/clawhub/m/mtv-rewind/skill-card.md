## Description: <br>
Play classic MTV music videos from the 80s, 90s, and 2000s. Use when the user wants to watch MTV, music videos, retro TV, or says anything like 'play MTV', 'I want my MTV', or 'put on some videos'. No API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Flexasaurusrex](https://clawhub.ai/user/Flexasaurusrex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to open a retro MTV-style web player for 80s, 90s, and 2000s music video requests. Agents should use it for broad MTV, retro music video, or background-video requests, and avoid it for exact-song playback or audio-only requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague requests for background music or unspecified videos could open the MTV Rewind player when the user expected a different media experience. <br>
Mitigation: Ask for confirmation before using the skill for ambiguous music or video requests. <br>
Risk: The skill directs users to a third-party web player outside the agent runtime. <br>
Mitigation: Use the disclosed player URL and rely on the server security summary; do not provide credentials or local data to the site. <br>


## Reference(s): <br>
- [MTV Rewind homepage](https://wantmymtv.xyz) <br>
- [MTV Rewind player](https://wantmymtv.xyz/player.html) <br>
- [ClawHub release page](https://clawhub.ai/Flexasaurusrex/mtv-rewind) <br>
- [Publisher profile](https://clawhub.ai/user/Flexasaurusrex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Short natural-language response with a direct web player URL or platform button payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials, binaries, local data access, or API keys are required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
