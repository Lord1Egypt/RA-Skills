## Description: <br>
Installs the full Job Autopilot pipeline for searching jobs, tailoring resumes, and submitting applications by installing jobautopilot-search, jobautopilot-tailor, and jobautopilot-submitter together. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerronl](https://clawhub.ai/user/jerronl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers use this bundle to install and configure a Job Autopilot workflow that finds job leads, tailors resumes and cover letters, and prepares application submissions. The bundle also creates local configuration, workspace, tracker, and browser-profile setup guidance used by the related skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup stores privacy-sensitive job-application information, including contact details, resume paths, and EEOC answers, in a local shell config file. <br>
Mitigation: Review the generated config, keep owner-only permissions, and avoid storing unnecessary personal information. <br>
Risk: Application submission workflows can enter information on external job sites when the user gives submission commands. <br>
Mitigation: Run submission commands only when ready for the information to be entered externally, and review browser activity before final submission. <br>
Risk: Browser profiles used for applications may retain job-site sessions or saved credentials. <br>
Mitigation: Use isolated browser profiles, avoid saving unnecessary credentials in the apply profile, and inspect or delete profiles when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jerronl/jobautopilot-bundle) <br>
- [Publisher Profile](https://clawhub.ai/user/jerronl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local user configuration, job tracker, handoff files, and setup instructions for related Job Autopilot skills.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
