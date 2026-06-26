## Description: <br>
Find installed GOG games not played in 30+ days, email a summary report, and add each game to Apple Reminders as a cleanup nudge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan a local GOG library JSON for installed games inactive past a cutoff, then review a cleanup report and optionally create personal email and reminder nudges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send an email report or create Apple Reminders from broad cleanup triggers. <br>
Mitigation: Ask the agent to scan first, review the generated report and recipient, and approve email or reminder creation explicitly before running those actions. <br>
Risk: The workflow reads a local GOG library JSON that may contain game names, play history, and install paths. <br>
Mitigation: Run it only against the intended library file and avoid sharing the generated report outside the user's chosen email or reminder workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/gog-dormant-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated plain-text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a temporary report file and can send email or create reminders when approved and supporting tools are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
