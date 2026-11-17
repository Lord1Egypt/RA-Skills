## Description:

博物馆讲解器升级版：召唤李白、苏轼、孔子等历史人物讲解文物。支持「让李白讲这个」「换成苏轼」等自然对话，沉浸式了解文物本身。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmingchen1994-dotcom](https://clawhub.ai/user/yangmingchen1994-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Museum visitors, educators, and agents use this skill to guide Chinese-language artifact conversations through historical-persona narration, including switching among known figures and answering follow-up questions in character.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that automatic persona generation can persist model-generated files with insufficient validation.

Mitigation: Disable or gate dynamic persona generation in sensitive environments, validate generated persona IDs and schemas, and prevent path traversal or unintended overwrites before saving persona files.

Risk: The security guidance calls for trusted API endpoints and protected credentials.

Mitigation: Use only trusted HTTPS API endpoints and keep API keys in environment variables or a secret manager rather than in scripts/config.json.

Risk: The security guidance notes that Chinese-language behavior should be expected.

Mitigation: Deploy where Chinese-language museum-guide responses are intended and review outputs for the target audience and setting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangmingchen1994-dotcom/skills/historical-guide)
- [OpenClaw configuration metadata](artifact/SKILL.md)
- [Required API configuration file](artifact/scripts/config.json)
- [Kongzi persona reference](artifact/references/kongzi.json)
- [Li Bai persona reference](artifact/references/libai.json)
- [Li Qingzhao persona reference](artifact/references/liqingzhao.json)
- [Su Shi persona reference](artifact/references/sushi.json)
- [Wang Xizhi persona reference](artifact/references/wangxizhi.json)
- [Zhang Qian persona reference](artifact/references/zhangqian.json)
- [Zhuge Liang persona reference](artifact/references/zhugeliang.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language text and Markdown with optional shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a configured chat-completions API and may persist generated persona JSON files under references/.]

## Skill Version(s):

1.1.8 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
