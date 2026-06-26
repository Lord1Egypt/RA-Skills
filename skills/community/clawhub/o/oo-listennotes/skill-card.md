## Description: <br>
Listen Notes (listennotes.com). Use this skill for ANY Listen Notes request - searching and reading data. Whenever a task involves Listen Notes, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search Listen Notes, retrieve podcast and episode details, and list discovery metadata through an OOMOL-connected Listen Notes account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Listen Notes account and credential-backed connector access. <br>
Mitigation: Review the first-time CLI install and account connection steps before use, and run account setup only when an auth or connection error requires it. <br>
Risk: Connector payloads can become invalid if the live Listen Notes action schema changes. <br>
Mitigation: Inspect the current action schema with oo connector schema before constructing or running each payload. <br>


## Reference(s): <br>
- [ClawHub Listen Notes Skill Page](https://clawhub.ai/oomol/oo-listennotes) <br>
- [Listen Notes Homepage](https://www.listennotes.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill inspects the live action schema before running read-only Listen Notes connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
