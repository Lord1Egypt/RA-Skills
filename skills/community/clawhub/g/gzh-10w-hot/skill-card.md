## Description: <br>
Finds and analyzes WeChat Official Account articles that reached 100k+ reads, supports category-based hot article queries and subscriptions, and can generate visual HTML ranking reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat operators, content creators, editors, and marketing teams use this skill to find recent 100k+ read articles, compare vertical categories, analyze viral content patterns, and create shareable ranking reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and contacts redfox.hk. <br>
Mitigation: Configure REDFOX_API_KEY through environment variables or a platform secret mechanism, and do not expose the key in shell startup files, prompts, logs, or generated output. <br>
Risk: Generated HTML reports store article metadata locally and load a PDF-export library from cdnjs when opened. <br>
Mitigation: Review report contents before sharing and open reports only in an environment where the external CDN dependency is acceptable. <br>
Risk: Daily subscription behavior may trigger scheduled pushes in the host platform. <br>
Mitigation: Review subscription settings before enabling daily pushes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/gzh-10w-hot) <br>
- [API specification](references/api-spec.md) <br>
- [Category mapping](references/category-mapping.md) <br>
- [RedFox API endpoint](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, HTML files, guidance] <br>
**Output Format:** [Markdown analysis and tables, shell command examples, configuration guidance, and generated HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may be exported to PDF by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
