## Description: <br>
基于 liepin-v4.mjs 的猎聘岗位检索与抓取技能，支持关键词搜索、结构化结果输出与调试截图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiaoxinxin](https://clawhub.ai/user/qiaoxinxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting and HR users use this skill to search Liepin for candidates, score matches against an Excel profile, capture resume evidence, and prepare structured candidate data for follow-up. It is intended only for lawful, authorized recruiting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate candidate contact and process candidate resume or contact data. <br>
Mitigation: Use only with an authorized Liepin recruiting account and a lawful basis for candidate processing; confirm outreach, retention, deletion, and data-protection rules before running. <br>
Risk: Resume text, screenshots, phone numbers, and progress data may be stored locally in plaintext. <br>
Mitigation: Run on a managed device or test account, restrict access to the output directory, and encrypt, archive, or delete outputs according to organizational policy. <br>
Risk: Authenticated site automation may trigger platform controls or produce incomplete results when pages, selectors, login state, or network conditions change. <br>
Mitigation: Start with small test runs, control request frequency, monitor CAPTCHA and failure states, and review generated records before using them in recruiting decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiaoxinxin/liepin-v4-skill) <br>
- [Project homepage](https://github.com/qiaoxinxin/liepin-v4-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, text, configuration] <br>
**Output Format:** [Local CSV, PNG screenshots, TXT resume extracts, JSON progress data, and console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written locally under a Desktop candidates directory and may include candidate contact details and resume content.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
