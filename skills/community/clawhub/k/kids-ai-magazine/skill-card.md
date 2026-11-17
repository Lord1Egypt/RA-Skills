## Description:

Generate a kid-friendly AI news magazine with text, audio narration, parent-child dialogue, activities, and quizzes for ages 3-6.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaofengshi](https://clawhub.ai/user/xiaofengshi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, parents, educators, and content creators use this skill to turn current AI news into preschool-friendly magazine stories with narration, parent notes, and simple activities. Agents can use it to prepare story JSON, generate TTS audio, build an interactive HTML issue, and provide preview or sharing commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may be unsafe to serve or share publicly.

Mitigation: Review generated files before serving or sharing them, and avoid using public tunnels for sensitive content.

Risk: Story inputs may include private child or family information.

Mitigation: Do not include private child or family details in story JSON, narration text, source fields, or generated pages.

Risk: Story JSON and source fields are untrusted inputs.

Mitigation: Escape story text and validate links before building or distributing the HTML output.

Risk: Generated output may contain misleading hardcoded publisher attribution.

Mitigation: Verify or remove hardcoded publisher attribution before distributing the magazine.

## Reference(s):

- [Example Stories JSON](references/example-stories.json)
- [ClawHub skill page](https://clawhub.ai/xiaofengshi/skills/kids-ai-magazine)
- [The Paper sample news source](https://www.thepaper.cn/newsDetail_forward_32689787)
- [Everyone Is a Product Manager sample news source](https://www.woshipm.com/share/6355994.html)
- [36Kr sample news source](https://36kr.com/p/3602173033792516)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands; generated artifacts are HTML magazine files and MP3 narration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses story JSON as input, builds a local HTML issue from a template, and can generate audio through edge-tts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
