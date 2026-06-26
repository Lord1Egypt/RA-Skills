## Description: <br>
FFHub helps agents operate FFHub FFmpeg transcoding tasks through the OOMOL oo CLI connector, including creating tasks and checking task status or outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media workflow operators use this skill to create FFmpeg transcoding tasks in FFHub and inspect task status, timing, errors, and generated outputs through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected FFHub account and can act through credentials managed by that connection. <br>
Mitigation: Install or use it only when the user intends to grant that account access, and run authentication or connection recovery steps only after matching command failures. <br>
Risk: Creating an FFmpeg task changes FFHub state and may consume account resources or credits. <br>
Mitigation: Confirm the exact payload and expected effect with the user before write actions, and inspect the live connector schema before building the payload. <br>
Risk: Connector schemas, authentication state, and billing state can change at runtime. <br>
Mitigation: Use the live schema as authoritative for each action and treat authentication, connection, or billing failures as explicit recovery paths. <br>


## Reference(s): <br>
- [FFHub homepage](https://ffhub.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub release page](https://clawhub.ai/oomol/oo-ffhub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
