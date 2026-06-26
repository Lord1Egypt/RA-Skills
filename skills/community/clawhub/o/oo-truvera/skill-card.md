## Description: <br>
Truvera helps agents read, create, and delete Truvera account resources through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Truvera account profile data, DIDs, credential schemas, and background job status from an agent workflow. It is intended for OOMOL-connected Truvera accounts where credentials are supplied through the configured connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change Truvera DIDs or credential schemas. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running actions tagged as write. <br>
Risk: Destructive actions can delete Truvera DIDs or credential schemas. <br>
Mitigation: Confirm the specific target and obtain explicit approval before running actions tagged as destructive. <br>
Risk: The skill requires access to a Truvera account through OOMOL-connected credentials. <br>
Mitigation: Use the configured connector for credential handling, do not ask for raw API tokens, and run setup steps only after an authentication or connection error. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-truvera) <br>
- [Truvera Homepage](https://truvera.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require an installed oo CLI, a signed-in OOMOL account, and a connected Truvera API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
