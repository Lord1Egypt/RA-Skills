## Description: <br>
Helps agents search, summarize, and monitor GIS and surveying campus recruiting information, prioritizing state-owned enterprises, public institutions, and major technology companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5758703](https://clawhub.ai/user/5758703) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, career advisors, and agents use this skill to find GIS and surveying campus recruitment leads, compare newly found postings with prior outputs, and prepare concise job reports for follow-up. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate live monitoring because bundled scripts include sample or fixed report data. <br>
Mitigation: Treat included job outputs as examples unless the agent performs a fresh live search and verifies links before sharing results. <br>
Risk: Scheduled push behavior can continue sending updates after setup. <br>
Mitigation: Enable scheduled pushes only when the operator knows how to inspect and remove the cron job. <br>
Risk: Search and report scripts may write local files, including fixed report paths. <br>
Mitigation: Review output paths before execution and run scripts in an appropriate workspace or temporary directory. <br>
Risk: Network search may require a Brave Search API key. <br>
Mitigation: Use a limited-scope API key and avoid embedding secrets in skill files or generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/5758703/gis-job-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/5758703) <br>
- [GIS employer list](references/company-list.md) <br>
- [GIS recruiting sites](references/job-sites.md) <br>
- [Latest GIS job records](references/latest-jobs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with job listings, shell command examples, Python scripts, and optional generated report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include job title, employer, degree, major, location, deadline, publish date, and source link fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
