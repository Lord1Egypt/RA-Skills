## Description: <br>
Automates 2haoHR meal-subsidy requests by reading attendance records, checking late-off-work eligibility, and filling and submitting reimbursement forms for a single date, week, or month. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamy-lei](https://clawhub.ai/user/jamy-lei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees who use 2haoHR can use this skill to check attendance-derived meal-subsidy eligibility and submit meal-subsidy requests for eligible dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in 2haoHR browser session and submits meal-subsidy forms automatically without a clear final confirmation step. <br>
Mitigation: Use a dedicated Chrome profile with no unrelated accounts or tabs, and review generated screenshots, CSV records, and logs after each run. <br>
Risk: Weekly or monthly batch mode can submit multiple requests based on parsed attendance data. <br>
Mitigation: Test single-date submissions first and use batch mode only after confirming the generated records match the intended reimbursement dates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jamy-lei/meal-subsidy) <br>
- [2haoHR desk home](https://i-wework.2haohr.com/desk/home) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [CLI execution with generated screenshots, CSV records, and log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes attendance screenshots, form screenshots, monthly late-record CSV files, and a local log file.] <br>

## Skill Version(s): <br>
1.3.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
