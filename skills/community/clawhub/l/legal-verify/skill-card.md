## Description: <br>
校验法律文本中的法规、法条、案例和案号引用，调用权威来源比对语义一致性和时效性，并输出判定与依据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doudoudou12138-design](https://clawhub.ai/user/doudoudou12138-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
法律从业者、合规人员和使用代理撰写法律文本的用户可用该技能复核正式文本中的中国法律引用，识别过期法规、语义不一致和未命中的案例或案号。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal text submitted for checking is sent to the ChineseLaw API through the configured API key. <br>
Mitigation: Use only when authorized to share the material, and avoid privileged, confidential, or personal content unless appropriate approvals are in place. <br>
Risk: Local body.json, response.json, and .env files can contain sensitive legal text, API responses, or credentials. <br>
Mitigation: Protect environment files, avoid committing credentials, and remove generated request and response files when they contain sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/doudoudou12138-design/legal-verify) <br>
- [ChineseLaw hall_detect API endpoint](https://open.chineselaw.com/open/hall_detect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown table with request IDs, source excerpts, links, and optional shell commands plus JSON request and response files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YUANDIAN_API_KEY; API calls may create body.json and response.json containing submitted legal text and returned source material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
