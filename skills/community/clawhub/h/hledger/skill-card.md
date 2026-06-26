## Description: <br>
Execute hledger CLI commands to query balances, registers, reports, and journals, returning structured output from local ledger files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bisbeebucky](https://clawhub.ai/user/bisbeebucky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Personal finance users and automation developers use this skill inside OpenClaw to run hledger balance, register, report, and journal queries against local ledger files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted input can cause unintended local shell commands to run through the hledger wrapper. <br>
Mitigation: Use only in a trusted local environment and prefer a fixed version that invokes hledger with validated arguments through spawn or execFile. <br>
Risk: Command output may expose sensitive personal finance data from local ledger files. <br>
Mitigation: Limit file access to intended ledgers and review outputs before sharing them outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bisbeebucky/hledger) <br>
- [Publisher profile](https://clawhub.ai/user/bisbeebucky) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text command output from hledger stdout or stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hledger on PATH and read access to the user's local ledger files.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata, artifact package.json, artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
