## Description: <br>
Create films with AI video generation by managing scripts, prompts, consistency, and production workflows from concept to final cut. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, filmmakers, and production teams use this skill to plan AI-assisted film projects, turn scripts into shot lists, route shots to generation tools, and assemble final edits with continuity, color, sound, export, and commercial-delivery guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ffmpeg examples can read from or write to unintended paths, especially when using concat list files or user-supplied media paths. <br>
Mitigation: Review input and output paths, avoid untrusted list.txt files, and keep editing work inside the intended project folder before running commands. <br>
Risk: AI video workflows may involve sensitive client assets, character references, scripts, or brand materials being sent to third-party generation tools. <br>
Mitigation: Share sensitive assets with third-party tools only when that transfer is intended and consistent with project, client, and rights requirements. <br>
Risk: Commercial productions can create legal or rights issues through likeness, music, brand, disclosure, or regional compliance mistakes. <br>
Mitigation: Verify consent for real-person likenesses, confirm rights to music and sound, follow brand guidelines, and check AI-disclosure or local regulatory requirements before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/movie) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Pre-Production - Script to Shot List](artifact/preproduction.md) <br>
- [Generation - Prompt Engineering for Video](artifact/generation.md) <br>
- [Post-Production - Assembly, Color, Sound](artifact/postproduction.md) <br>
- [Tools - Video Generation APIs & CLIs](artifact/tools.md) <br>
- [Commercial Production - Ads, Corporate, Branded Content](artifact/commercial.md) <br>
- [Experimental Video - Artistic, Abstract, Music-Driven](artifact/experimental.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with checklists, prompt templates, tables, project-structure examples, and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces production planning and editing guidance; it does not directly invoke video-generation tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
