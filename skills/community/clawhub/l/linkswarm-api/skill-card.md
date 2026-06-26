## Description: <br>
LinkSwarm API helps agents manage LinkSwarm backlink exchanges by registering domains, requesting backlinks, contributing link slots, checking credits and status, and configuring placement notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Heyw00d](https://clawhub.ai/user/Heyw00d) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators can use this skill to let an agent interact with the LinkSwarm API for approved domains: registering sites, managing backlink credits, requesting or contributing placements, and monitoring results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent spend LinkSwarm credits and request public backlinks. <br>
Mitigation: Require explicit approval before backlink requests and limit use to owned domains and approved pages. <br>
Risk: Site registration and link-slot contributions can affect SEO and reputation for public pages. <br>
Mitigation: Approve domains, pages, categories, and link-slot contributions before the agent submits them. <br>
Risk: Webhook setup and API key use introduce credential and endpoint security concerns. <br>
Mitigation: Store the API key in a trusted credential store and approve webhook destinations before configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Heyw00d/linkswarm-api) <br>
- [LinkSwarm Documentation](https://linkswarm.ai/docs/) <br>
- [LinkSwarm Registration](https://linkswarm.ai/register/) <br>
- [LinkSwarm API Status](https://api.linkswarm.ai/health) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with curl and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkSwarm API key and approval before making site, backlink, credit, or webhook changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
