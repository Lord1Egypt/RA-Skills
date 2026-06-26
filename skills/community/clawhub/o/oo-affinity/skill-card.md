## Description: <br>
Affinity (affinity.co) supports searching and reading Affinity data through the OOMOL `oo` CLI connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Affinity connector schemas and retrieve Affinity companies, people, opportunities, lists, saved views, and field metadata from an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Affinity account. <br>
Mitigation: Use the existing OOMOL connection flow and avoid exposing raw credentials in prompts, shell history, or generated files. <br>
Risk: Connector schemas may change over time, causing stale payload assumptions. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing or running connector payloads. <br>


## Reference(s): <br>
- [ClawHub Affinity Skill](https://clawhub.ai/oomol/oo-affinity) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Affinity Homepage](https://www.affinity.co) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, OOMOL sign-in, and an active Affinity connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
