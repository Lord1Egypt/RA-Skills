## Description: <br>
Generates interactive HTML magazines that adapt AI news into parent-child stories for ages 3-6 with text, audio narration, dialogues, activities, rhymes, and quizzes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaofengShi](https://clawhub.ai/user/xiaofengShi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, educators, and agents preparing child-friendly content use this skill to turn selected AI news items into preschool parent-child magazine stories with narration and an interactive HTML page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story JSON fields are inserted into generated HTML, so untrusted story content could create misleading or unsafe output. <br>
Mitigation: Use trusted story JSON, review the generated HTML before opening or sharing it, and avoid private or sensitive text in narration. <br>
Risk: The audio and sharing workflow can install local Python dependencies and may expose the generated output directory when cloudflared is used. <br>
Mitigation: Review the local scripts before execution, install edge-tts intentionally, and use cloudflared only when the output is meant to be publicly reachable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaofengShi/kids-ai-magazine) <br>
- [Example stories JSON](artifact/references/example-stories.json) <br>
- [The Paper source article](https://www.thepaper.cn/newsDetail_forward_32689787) <br>
- [人人都是产品经理 source article](https://www.woshipm.com/share/6355994.html) <br>
- [36Kr source article](https://36kr.com/p/3602173033792516) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON story data, shell commands, generated HTML, and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts; audio generation depends on edge-tts and optional public sharing uses cloudflared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
