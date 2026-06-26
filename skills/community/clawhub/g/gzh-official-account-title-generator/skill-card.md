## Description: <br>
Generates WeChat Official Account title candidates and scores existing titles using RedFox trend data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, account operators, MCNs, and brands use this skill to generate data-aligned WeChat Official Account titles or evaluate existing titles with scoring and optimization suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Title topics and scoring inputs are sent to RedFox. <br>
Mitigation: Use the skill only when sharing those inputs with RedFox is acceptable, and avoid submitting confidential or sensitive draft content. <br>
Risk: Debug logging may expose the X-API-Key credential. <br>
Mitigation: Avoid using --debug unless the script redacts credentials, and review logs before sharing them. <br>
Risk: Broad activation could apply the skill to generic writing requests. <br>
Mitigation: Use it only for explicit WeChat title-generation or title-scoring tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/gzh-official-account-title-generator) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox WeChat trend data API](https://redfox.hk/story/api/cozeSkill/getWxCozeSkillData) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated title lists, scoring breakdowns, recommendation text, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; recommendations and scores should be checked against returned trend data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
