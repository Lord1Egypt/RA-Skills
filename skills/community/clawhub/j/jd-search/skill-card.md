## Description: <br>
Execute keyword-based product searches on JD Gongcai Cloud with category, price, pagination, and output-format controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangr19](https://clawhub.ai/user/zhangr19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized JD internal users use this skill to run product searches against JD Gongcai Cloud search services and inspect product data in table, JSON, or CSV output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented CLI executable is not included in the artifact. <br>
Mitigation: Inspect and obtain the executable from a trusted source before running chmod, creating a /usr/local/bin symlink, or invoking jd-search. <br>
Risk: The search service is described as an internal JD service. <br>
Mitigation: Use the skill only when authorized to access JD internal search services and from an appropriate network environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangr19/jd-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and structured option descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may be requested as table, JSON, or CSV when the documented CLI is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
