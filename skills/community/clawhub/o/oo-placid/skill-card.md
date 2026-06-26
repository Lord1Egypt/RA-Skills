## Description: <br>
Placid enables agents to read, create, update, and delete Placid data through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Placid through an OOMOL-connected account, inspect connector schemas, manage templates, generate images, poll image status, and delete image requests with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may execute remote installer scripts directly from the network without verification. <br>
Mitigation: Install the oo CLI from a trusted, versioned source or verify the installer before execution. <br>
Risk: Write and delete actions can modify or remove Placid resources. <br>
Mitigation: Approve these actions only after checking the exact payload, effect, and target. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-placid) <br>
- [Placid homepage](https://placid.app) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
