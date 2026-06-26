## Description: <br>
上传单词到 K241 班单词自学网站 (k241.wooomooo.com)，支持自动获取翻译和拼音。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veelove](https://clawhub.ai/user/veelove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External site administrators use this skill to add or update K241 vocabulary records, including translations and pinyin, on the class self-study website. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a shared login and could allow unauthorized access if credentials are reused. <br>
Mitigation: Use only with authorization, rotate the exposed password, and prefer a version that requests credentials securely at runtime. <br>
Risk: The skill gives agents direct ability to upload or update live website records. <br>
Mitigation: Require confirmation before changing records and review uploaded or updated entries after execution. <br>


## Reference(s): <br>
- [K241 word site](https://k241.wooomooo.com) <br>
- [K241 单词拼音参考表](references/pinyin.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with HTTP request examples and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in changes to live vocabulary records when an authorized agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
