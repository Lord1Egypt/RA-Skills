## Description:

查询京东账号（京东pin）绑定手机号及关联员工公司信息流程；入参为：pin（京东账号（京东pin））

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuoxiangpang](https://clawhub.ai/user/zhuoxiangpang)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized internal support, security, or account operations staff use this skill to trace a JD account pin to historical bound phone data and related employee, company, and supplier context. It should be used only for approved cases where the executing agent already has access to the named datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose sensitive phone, employee, company, and supplier relationships for a JD account pin.

Mitigation: Limit installation to authorized internal environments, require a documented business justification, and ensure the agent already has approved access to each named dataset.

Risk: Lookup results could be used for broad account searches or third-party profiling.

Mitigation: Log each lookup, restrict use to approved cases, and mask or suppress phone and employee fields by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuoxiangpang/skills/pin)
- [ClawHub publisher profile](https://clawhub.ai/user/zhuoxiangpang)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance with structured lookup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a JD account pin as the lookup key; returned phone, employee, company, and supplier fields should be minimized, masked, and logged according to authorization requirements.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
