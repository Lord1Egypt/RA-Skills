## Description: <br>
Browse AI (browse.ai). Use this skill for ANY Browse AI request - reading, creating, and updating data. Whenever a task involves Browse AI, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Browse AI robot schemas, list robots and tasks, retrieve captured task data, start robot tasks, and update robot cookies through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates Browse AI through an OOMOL-connected account and depends on server-side credential injection. <br>
Mitigation: Install only when the agent should use the connected Browse AI account, and review account connection status before use. <br>
Risk: Write actions can update robot cookies or start tasks that may consume Browse AI or OOMOL account resources. <br>
Mitigation: Confirm the exact payload and intended effect with the user before write actions, especially cookie updates and task starts. <br>


## Reference(s): <br>
- [ClawHub Browse AI Skill](https://clawhub.ai/oomol/oo-browse-ai) <br>
- [Browse AI Homepage](https://www.browse.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions return JSON data from the Browse AI connector when executed with the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
