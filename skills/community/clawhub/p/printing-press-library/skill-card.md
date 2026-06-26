## Description: <br>
Use when looking for a CLI, API wrapper, scraper, data-source tool, automation tool, or focused agent skill for a task; searches the Printing Press Library and installs matching tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find purpose-built Printing Press CLIs or focused skills, choose an appropriate match for a task, and install or refresh only the selected tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to install third-party Printing Press CLIs or skills. <br>
Mitigation: Install only when the selected tool is useful for the user's task, review each proposed tool before installation, and verify with a harmless command before claiming success. <br>
Risk: Some discovered tools may require credentials, scrape websites, mutate accounts, or perform paid or public-facing actions. <br>
Mitigation: Check requirements before installation or use, avoid printing secrets, and require explicit user approval before any external side effect. <br>
Risk: Recurring update jobs are durable side effects. <br>
Mitigation: Offer consolidated low-frequency updates only after a successful install or refresh, and create scheduled jobs only with explicit user approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tmchow/skills/printing-press-library) <br>
- [Project Homepage](https://github.com/mvanhorn/printing-press-library) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install, update, reload, verification, and credential-check guidance; external side effects require user approval.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
