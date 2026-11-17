## Description:

生成美甲制作过程短视频。猫眼、流沙、星空、奶油胶、微缩立体美甲——小尺寸极高细节，近景治愈感强，支持节日主题，一句话出片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to prepare short vertical nail-art process videos with macro ASMR styling, including character-based nail designs and material-focused close-ups. The skill helps collect prompts, confirm generation parameters, and run the WeryAI video generation CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can send WERYAI_API_KEY and generation prompts to configured network endpoints.

Mitigation: Run the skill only in a controlled environment, keep WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL unset unless they point to trusted endpoints, and treat WERYAI_API_KEY as a sensitive secret.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill and its network behavior before installing or using it in a shared environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/nail-art-video)
- [Publisher profile](https://clawhub.ai/user/zoucdr)
- [WeryAI video API endpoint](https://api.weryai.com)
- [WeryAI model registry endpoint](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and WERYAI_API_KEY; video generation results are returned as task status and video URL JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
