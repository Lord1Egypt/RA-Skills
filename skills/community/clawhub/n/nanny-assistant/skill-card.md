## Description: <br>
A maternal and newborn care assistant that generates an interactive HTML dashboard for 28-day postpartum workflows, including care logs, health monitoring, meal planning, medication tracking, reports, and handoff summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, maternity centers, and maternal-newborn care teams use this skill to create a browser-based dashboard for recording postpartum and newborn care activities, tracking daily health data, and preparing family reports or handoff summaries. Users should treat stored and exported records as sensitive health information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive family and health records in browser storage and exported JSON files. <br>
Mitigation: Use only on a trusted device and browser profile, avoid shared computers, and treat exported JSON backups as sensitive medical records. <br>
Risk: The release evidence reports overbroad agent permissions and an undisclosed third-party script load. <br>
Mitigation: Review the skill before installing, prefer removing unnecessary Bash permission, and bundle Chart.js locally or use integrity protections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/nanny-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus a single-page HTML dashboard with browser localStorage and JSON import/export support] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated dashboard stores maternal and newborn care data locally in the browser, can export JSON backups, and loads Chart.js from a third-party CDN.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
