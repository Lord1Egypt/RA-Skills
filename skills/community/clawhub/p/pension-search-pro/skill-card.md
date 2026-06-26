## Description: <br>
企业年金智能查询技能。搜索并确认企业年金信息，输出带来源链接和错误检查的标准化调查报告。只查询企业年金，不查询职业年金。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanwenzhe](https://clawhub.ai/user/yanwenzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents use this skill to investigate whether a named organization has public enterprise-pension information and to produce a sourced Markdown report with confidence labels and review checks. <br>

### Deployment Geography for Use: <br>
Global; intended for public enterprise-pension research about organizations covered by China enterprise-pension context. <br>

## Known Risks and Mitigations: <br>
Risk: Investigation queries may send target organization names and pension-related terms to external search providers. <br>
Mitigation: Review queries before execution, avoid confidential targets or sensitive internal context, and use only approved search providers and credentials. <br>
Risk: Security review found the scripts may do more than the advertised enterprise-pension-only purpose. <br>
Mitigation: Treat script output as a draft, review generated reports before use, and confirm that conclusions address enterprise pensions rather than occupational pensions. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review and scan the skill before installing or running it in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanwenzhe/pension-search-pro) <br>
- [Publisher profile](https://clawhub.ai/user/yanwenzhe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown investigation report with source links, confidence labels, and checklist items; shell scripts may also print search URLs and write Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an organization name as the primary input. Script execution may require curl, jq, and TAVILY_API_KEY.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
