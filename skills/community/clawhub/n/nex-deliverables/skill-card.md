## Description: <br>
Nex Deliverables helps agency operators and freelancers track client deliverables, deadlines, workload, status updates, and exports through a local Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agency operators, design studios, marketing firms, and freelancers use this skill through an agent to manage client deliverables, track deadlines and statuses, generate client status email drafts, and export records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores client names, contact details, retainer details, deadlines, notes, and deliverable history locally. <br>
Mitigation: Use it only on machines where local storage under ~/.nex-deliverables is acceptable, and protect or back up that directory according to the user's data-handling requirements. <br>
Risk: Setup adds a nex-deliverables command under ~/.local/bin. <br>
Mitigation: Review the setup step before installation and ensure ~/.local/bin PATH behavior is acceptable for the agent environment. <br>
Risk: Some natural-language invocation phrases are broad and could match multiple status or export actions. <br>
Mitigation: Use explicit client names, deliverable titles, IDs, statuses, and export formats before changing records or creating exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-deliverables) <br>
- [Publisher profile](https://clawhub.ai/user/nexaiguy) <br>
- [Nex AI website](https://nex-ai.be) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text CLI output, generated status email text, and optional CSV or JSON export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite storage under ~/.nex-deliverables; command output includes a footer that agents should omit when presenting results.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
