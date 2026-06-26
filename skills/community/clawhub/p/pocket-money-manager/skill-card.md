## Description: <br>
理财小助手，收支记录、消费分析、预算提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[786793119](https://clawhub.ai/user/786793119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to ask an agent for personal finance tracking commands, including income and expense entries, balance checks, weekly spending reports, monthly budgets, and overspending alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records personal finance data in local JSON files. <br>
Mitigation: Install and use it only on devices where storing income, expense, and budget details locally is acceptable. <br>
Risk: The artifact references a separate pocket-money-manager.py script that is not included in the reviewed artifact. <br>
Mitigation: Review any separate script before running the commands described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/786793119/pocket-money-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact describes local JSON storage for finance records and budget settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
