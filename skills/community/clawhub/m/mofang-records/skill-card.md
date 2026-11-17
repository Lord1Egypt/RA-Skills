## Description:

Query and manage Magicflu/Mofang web-table records and BPM workflow tasks through the bundled CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicscape](https://clawhub.ai/user/magicscape)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Magicflu/Mofang spaces and forms, manage table records, and perform BPM workflow actions through a Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses business credentials for powerful record and BPM workflow actions.

Mitigation: Use it only with a trusted Magicflu/Mofang server and a narrowly scoped non-admin account, and require explicit human confirmation before deletes or BPM workflow changes.

Risk: Insecure HTTP endpoints could expose credentials.

Mitigation: Configure an HTTPS BASE_URL whenever possible.

Risk: Recent space and form aliases may be stored locally under ~/.mofang-skills.

Mitigation: Use the skill on trusted hosts and clear the local cache when the environment is shared or decommissioned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicscape/skills/mofang-records)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown text with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands return JSON payloads from the configured Magicflu/Mofang service.]

## Skill Version(s):

3.1.3 (source: server release metadata; artifact manifests report 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
