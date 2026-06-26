## Description: <br>
个性化信息简报生成技能。支持按需生成一次性简报或定期推送，涵盖信息搜索、筛选、整理与输出全流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winsaney](https://clawhub.ai/user/winsaney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users use this skill to configure topics, source preferences, cadence, and templates for one-off or recurring personalized newsletters. Agents use it to search, filter, summarize, organize, and deliver newsletter content with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated newsletters may include inaccurate, outdated, or weakly sourced information. <br>
Mitigation: Review generated issues before relying on them, prefer high-quality sources, and keep source links with each item for verification. <br>
Risk: Recurring newsletters or push delivery can access unintended sources or integrations if configured too broadly. <br>
Mitigation: Confirm allowed sources before enabling recurring use and only provide credentials to specific trusted integrations intentionally configured by the user. <br>


## Reference(s): <br>
- [Basic newsletter template](assets/template-basic.md) <br>
- [Advanced newsletter template](assets/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text newsletter content, source lists, reusable templates, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports one-off newsletters and recurring newsletter setup with customizable topics, sources, depth, item count, format, and section structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
