## Description: <br>
Automates job search on Indeed, analyzes fit, tailors resumes, and applies through supported ATS platforms while logging results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbedMir31](https://clawhub.ai/user/AbedMir31) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers or authorized agents use this skill to search for matching roles, tailor a resume from existing source data, submit applications through job platforms, and track application outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit job applications using a named person's personal data and job-site accounts. <br>
Mitigation: Install or run it only for Abed Mir or with explicit permission, and require approval before every submission or disable auto-apply. <br>
Risk: Scheduled runs can continue submitting applications without active oversight. <br>
Mitigation: Make scheduled execution opt-in, provide a clear stop path, and review the run summary and application log after each run. <br>
Risk: Credential or one-time-code requests over Discord could expose account access. <br>
Mitigation: Never send passwords or one-time codes through Discord; complete authentication through secure account flows. <br>
Risk: Sharing the artifact as-is can expose hard-coded personal data. <br>
Mitigation: Remove or replace personal data before sharing, publishing, or adapting the skill for another person. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbedMir31/job-applications) <br>
- [Publisher profile](https://clawhub.ai/user/AbedMir31) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, JSON logs, LaTeX source, and generated resume files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create tailored resume artifacts and application tracking records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
