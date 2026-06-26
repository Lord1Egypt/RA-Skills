## Description: <br>
Operate BunnyCDN through an OOMOL-connected account by inspecting connector schemas and running supported pull zone list, get, and cache purge actions with the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to manage BunnyCDN pull zones through OOMOL's connector workflow, including listing pull zones, retrieving one pull zone, and explicitly approved cache purges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup instructions include remote installer commands for the oo CLI. <br>
Mitigation: Do not let an agent run the remote installer automatically; install the oo CLI only through a trusted, verified method. <br>
Risk: The purge_pull_zone_cache action is destructive and can remove cached BunnyCDN content for a pull zone or cache tag. <br>
Mitigation: Confirm the exact pull zone ID, optional cache tag, and expected effect with the user before running the purge. <br>
Risk: The skill requires connected BunnyCDN credentials through OOMOL. <br>
Mitigation: Use the OOMOL-connected account flow and avoid requesting, displaying, or storing raw BunnyCDN tokens in the agent conversation. <br>


## Reference(s): <br>
- [ClawHub BunnyCDN Skill](https://clawhub.ai/oomol/oo-bunnycdn) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [BunnyCDN Homepage](https://bunny.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before building action payloads; destructive cache purges require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
