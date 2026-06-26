## Description: <br>
Uses OOMOL's oo CLI connector to search and read Worksnaps profiles, projects, tasks, assignments, and time-tracking data through a connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to inspect Worksnaps account, project, task, assignment, and time-entry information through an already connected Worksnaps account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Worksnaps business and time-tracking data through a connected account. <br>
Mitigation: Install it only when the user trusts OOMOL and intends the agent to access Worksnaps data through that account. <br>
Risk: First-time CLI installation, sign-in, or Worksnaps connection steps could expose sensitive account setup flows to an agent. <br>
Mitigation: Have the user perform first-time install, login, and Worksnaps API-key connection steps directly. <br>
Risk: Future connector actions labeled write or destructive could change or remove Worksnaps data. <br>
Mitigation: Require explicit user approval of the exact payload and effect before running any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/oomol/oo-worksnaps) <br>
- [Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Worksnaps Homepage](https://www.worksnaps.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Worksnaps connector actions unless a future action is explicitly labeled write or destructive.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
