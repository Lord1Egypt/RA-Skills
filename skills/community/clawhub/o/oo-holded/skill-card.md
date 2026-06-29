## Description: <br>
Holded (holded.com). Use this skill for ANY Holded request - reading, creating, and updating data. Whenever a task involves Holded, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Holded through an OOMOL-connected account, including contact creation, contact lookup, product lookup, and paginated list workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read business contact and product data from an OOMOL-connected Holded account. <br>
Mitigation: Install and use it only when the agent is intended to access that Holded account and its business data. <br>
Risk: The create_contact action can change data in the connected Holded account. <br>
Mitigation: Review the exact write payload and expected effect with the user before approving execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-holded) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Holded Homepage](https://www.holded.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before actions; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
