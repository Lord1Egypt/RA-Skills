## Description: <br>
LMS data aggregation and reporting tool for course information management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Acogkr](https://clawhub.ai/user/Acogkr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to collect Hoseo LMS course data, summarize deadlines and attendance status, and run limited lecture playback only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated LMS login and lecture playback may violate institutional rules or exceed the user's intended LMS activity. <br>
Mitigation: Use the skill only when LMS automation is allowed, require an explicit user request, and run auto_attend with concrete course and lecture limits. <br>
Risk: Credentials may be exposed if passed on the command line or stored without appropriate file protections. <br>
Mitigation: Prefer a protected local credentials file, avoid command-line passwords, and remove or secure the file when it is not needed. <br>
Risk: The implementation can perform lecture playback, which is broader than a reporting-only workflow. <br>
Mitigation: Treat playback as a separate high-impact action that requires user confirmation before execution. <br>


## Reference(s): <br>
- [Hoseo LMS](https://learn.hoseo.ac.kr) <br>
- [ClawHub skill page](https://clawhub.ai/Acogkr/hoseo-lms) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown guidance with shell commands, terminal reports, and local JSON data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Playwright-supported browser automation for lecture playback.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
