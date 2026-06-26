## Description: <br>
Todoist (todoist.com). Use this skill for ANY Todoist request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read, create, update, organize, and complete Todoist tasks, projects, sections, labels, and comments through an OOMOL-connected Todoist account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, complete, and organize Todoist records, so an ambiguous request could change the user's task data unexpectedly. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running write actions. <br>
Risk: The skill requires access to a connected Todoist account through OOMOL. <br>
Mitigation: Install it only when the agent is expected to use that Todoist account, and review requests before allowing account-backed actions. <br>
Risk: The security summary notes that the trigger wording is broader than ideal. <br>
Mitigation: Treat incidental Todoist mentions cautiously and ask for clarification before taking write actions. <br>


## Reference(s): <br>
- [Todoist homepage](https://www.todoist.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-todoist) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a signed-in OOMOL account with a connected Todoist provider before live actions can run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
