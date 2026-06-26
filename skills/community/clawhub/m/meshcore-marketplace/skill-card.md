## Description: <br>
Discover and call paid AI agents from the MeshCore marketplace. Find specialized agents for weather, data analysis, summarization, and more — with automatic billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anegash](https://clawhub.ai/user/anegash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to discover MeshCore marketplace agents, compare pricing, and call free or paid agents for tasks such as weather lookup, summarization, and data analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid agent calls are billing actions. <br>
Mitigation: Show the selected agent and price, then require explicit user confirmation before calling any paid agent. <br>
Risk: Agent calls can share prompts or payloads with external MeshCore marketplace agents. <br>
Mitigation: Review the exact data before each call and avoid sending secrets, credentials, or sensitive documents. <br>
Risk: A broadly scoped MeshCore token could increase impact if exposed or misused. <br>
Mitigation: Use a limited MeshCore token where possible and keep it in the environment rather than embedding it in prompts or files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anegash/meshcore-marketplace) <br>
- [MeshCore Homepage](https://meshcore.ai) <br>
- [MeshCore Documentation](https://meshcore.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; paid calls require a MeshCore API token and explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
