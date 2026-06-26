## Description: <br>
Historical Guide helps an agent present museum objects through the voice and style of Chinese historical figures such as Li Bai, Su Shi, and Confucius. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangmingchen1994-dotcom](https://clawhub.ai/user/yangmingchen1994-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to create conversational museum-guide responses, switch between historical-persona narrators, and explain artifacts with persona-specific style and reference profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Museum queries and conversation text are sent to the configured model provider. <br>
Mitigation: Use a trusted API_BASE and avoid entering sensitive personal data. <br>
Risk: A configured API key is required for model calls. <br>
Mitigation: Use a least-privilege API key and keep it in environment variables or a protected local configuration file. <br>
Risk: Generated out-of-library persona files are synthetic and may be inaccurate or malformed. <br>
Mitigation: Review or delete generated files in references/ before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangmingchen1994-dotcom/historical-guide) <br>
- [kongzi.json](references/kongzi.json) <br>
- [libai.json](references/libai.json) <br>
- [liqingzhao.json](references/liqingzhao.json) <br>
- [sushi.json](references/sushi.json) <br>
- [wangxizhi.json](references/wangxizhi.json) <br>
- [zhangqian.json](references/zhangqian.json) <br>
- [zhugeliang.json](references/zhugeliang.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style conversational text with optional shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured model API and may save generated persona profiles under references/.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
