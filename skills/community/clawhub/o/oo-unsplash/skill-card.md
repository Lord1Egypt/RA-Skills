## Description: <br>
Guides agents to search and fetch Unsplash photos and topics through an OOMOL-connected oo CLI Unsplash connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to discover, search, list, or retrieve Unsplash photos and topics through a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires use of OOMOL's oo CLI and an Unsplash connection with credentials injected server-side. <br>
Mitigation: Install only when OOMOL-mediated Unsplash access is intended, keep account connections scoped to the expected use, and avoid handling raw Unsplash tokens directly. <br>
Risk: First-time setup may ask the agent to run a remote CLI installer if the oo command is missing. <br>
Mitigation: Review the OOMOL CLI install step before execution and run setup commands only after an actual missing-CLI, authentication, connection, or billing error. <br>
Risk: Connector requests route through OOMOL rather than direct Unsplash API calls. <br>
Mitigation: Review OOMOL account, billing, and connector trust requirements before using the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub Unsplash skill page](https://clawhub.ai/oomol/oo-unsplash) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Unsplash homepage](https://unsplash.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are expected as JSON with data and meta.executionId fields when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
