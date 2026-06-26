## Description: <br>
Nex Onboarding helps agency operators manage client onboarding workflows from contract through go-live with local checklists, progress tracking, task status updates, statistics, and JSON/CSV exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agency operators and service providers use this skill to start and manage client onboarding workflows, track blocked or completed steps, assign work, report statistics, and export local onboarding records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores client onboarding records locally and can export them as JSON or CSV, so those files may contain sensitive client information. <br>
Mitigation: Treat the database and exports as sensitive records, avoid storing passwords or service credentials in notes, and review CSV exports before opening them in spreadsheet tools. <br>
Risk: The setup script creates files under ~/.nex-onboarding and installs a command wrapper in ~/.local/bin. <br>
Mitigation: Review the setup behavior before installation and remove the local data directory and wrapper if the skill should no longer retain data on the machine. <br>


## Reference(s): <br>
- [Nex AI](https://nex-ai.be) <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; CLI output as terminal text; exports as JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores onboarding data locally in ~/.nex-onboarding and uses a nex-onboarding command wrapper created in ~/.local/bin during setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
