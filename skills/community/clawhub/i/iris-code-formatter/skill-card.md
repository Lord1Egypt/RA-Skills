## Description: <br>
Reviews, formats, and corrects InterSystems IRIS/Cache ObjectScript code against naming, formatting, lock, transaction, trap, blank-line, and comment conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaoxin521123](https://clawhub.ai/user/yaoxin521123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review IRIS/ObjectScript snippets, identify style and correctness issues, and receive a complete corrected version of the submitted code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted IRIS/ObjectScript code may contain secrets or sensitive proprietary logic, and the skill is designed to return full corrected code. <br>
Mitigation: Avoid submitting secrets or sensitive proprietary code unless sharing that code with the agent environment is acceptable. <br>
Risk: Broad activation wording may trigger review automatically when pasted IRIS/ObjectScript code is present. <br>
Mitigation: Use the skill in contexts where automatic style review is expected, and review the returned corrections before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yaoxin521123/iris-code-formatter) <br>
- [Code Standard Reference Index](references/README.md) <br>
- [Variable Naming Standards](references/代码规范 - 变量.md) <br>
- [Method Naming Standards](references/代码规范 - 方法.md) <br>
- [Formatting Standards](references/代码规范 - 格式.md) <br>
- [Transaction Standards](references/代码规范 - 事务.md) <br>
- [Lock Standards](references/代码规范 - 锁.md) <br>
- [Trap Standards](references/代码规范 - 陷阱.md) <br>
- [Blank Line Standards](references/代码规范 - 空行.md) <br>
- [Comment Standards](references/代码规范 - 注释.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, guidance] <br>
**Output Format:** [Markdown code review report with corrected ObjectScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns issue summaries, detailed explanations, rule references, and the full corrected code when applicable.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence; changelog released 2026-04-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
