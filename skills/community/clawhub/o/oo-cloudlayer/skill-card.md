## Description: <br>
cloudlayer.io lets an agent operate a user's OOMOL-connected cloudlayer.io account to create PDF jobs and read account, asset, and job data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate cloudlayer.io through an OOMOL-connected account, including asynchronous PDF generation from HTML, templates, or public URLs and retrieval of account, job, and asset data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates an OOMOL-connected cloudlayer.io account and may require sensitive account credentials. <br>
Mitigation: Install only when the user intends to operate that cloudlayer.io account, and rely on OOMOL-managed credentials rather than handling raw tokens. <br>
Risk: PDF job creation actions can change cloudlayer.io account state or affect account usage and cost. <br>
Mitigation: Confirm the exact payload and expected cost or effect with the user before running write actions. <br>
Risk: First-time setup may require installing the oo CLI with a shell installer command. <br>
Mitigation: Review the installer command before execution and run setup only after an actual CLI, authentication, connection, or billing error. <br>


## Reference(s): <br>
- [cloudlayer.io homepage](https://cloudlayer.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-cloudlayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
