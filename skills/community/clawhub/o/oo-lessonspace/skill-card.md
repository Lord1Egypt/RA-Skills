## Description: <br>
Lessonspace lets agents read, create, and update Lessonspace data through the OOMOL oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Lessonspace through their connected OOMOL account, including creating or retrieving rooms, listing and fetching organisation sessions, and retrieving recording playback URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires server-side credentials for Lessonspace through OOMOL. <br>
Mitigation: Use it only with an expected OOMOL-connected Lessonspace account and avoid exposing raw credentials in prompts or command payloads. <br>
Risk: The create_unified_space action can change Lessonspace state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Authentication, connection, or billing failures can block actions. <br>
Mitigation: Run first-time setup or billing remediation steps only after a command returns the matching error. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-lessonspace) <br>
- [Lessonspace Homepage](https://www.thelessonspace.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the oo CLI and may return JSON responses with data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
