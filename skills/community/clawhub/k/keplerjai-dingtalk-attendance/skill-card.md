## Description: <br>
Fetches employee attendance data from the DingTalk Open Platform and saves it locally or sends it to a configured channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renjicode](https://clawhub.ai/user/renjicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR, operations, or IT administrators use this skill to collect DingTalk department, employee, and attendance records for daily, weekly, or date-range reporting. It can generate local JSON and Excel attendance reports after the DingTalk app is configured and authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive employee attendance and directory data. <br>
Mitigation: Install and run it only for authorized DingTalk administrators; keep credentials out of version control, restrict output directory access, and define retention and deletion rules. <br>
Risk: Normal use can install a Python dependency automatically if openpyxl is missing. <br>
Mitigation: Install npm and Python dependencies in a controlled environment before running, and remove or avoid the automatic pip-install fallback where policy requires fixed dependencies. <br>
Risk: Scheduled collection can repeatedly export employee data without direct user review. <br>
Mitigation: Enable cron or other automated execution only with clear approval, monitoring, and access controls for generated reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/renjicode/keplerjai-dingtalk-attendance) <br>
- [Publisher profile](https://clawhub.ai/user/renjicode) <br>
- [DingTalk Open Platform](https://open.dingtalk.com) <br>
- [README.md](README.md) <br>
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) <br>
- [WEEKLY_GUIDE.md](WEEKLY_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated JSON and Excel files from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local attendance reports and summary statistics; credentials are read from local configuration and should not be echoed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
