## Description: <br>
Evenium (corp.evenium.com). Use this skill for Evenium requests that read, create, or update event and guest data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Evenium action schemas, list or retrieve events and guests, and perform confirmed status-changing guest actions through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a connected Evenium account and therefore depends on sensitive account credentials managed by OOMOL. <br>
Mitigation: Install and use it only for accounts the agent is allowed to access, and verify the OOMOL connection flow from trusted sources before first-time setup. <br>
Risk: Some Evenium actions can change guest status or other event data. <br>
Mitigation: Inspect the live action schema and confirm the exact payload and expected effect with the user before running any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub Evenium Skill](https://clawhub.ai/oomol/oo-evenium) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Evenium Homepage](https://corp.evenium.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses server-side OOMOL credential injection and requires confirmation before write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
