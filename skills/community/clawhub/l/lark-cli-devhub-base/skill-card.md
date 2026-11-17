## Description:

Helps agents design, provision, search, and write Feishu/Lark Base records through lark-cli or feishu-cli for a Dev Hub knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to maintain searchable Dev Hub records in Feishu/Lark Base, including projects, tasks, decisions, releases, artifacts, and AI run summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide provisioning or writes to a configured Lark/Feishu Base, so records may go to the wrong base or schema if the environment is misconfigured.

Mitigation: Confirm the target base token and current schema before provisioning or writing records.

Risk: Development records may accidentally include secrets or raw credentials.

Mitigation: Redact sensitive values before writing and follow the skill's rule not to store secrets or raw credentials.

Risk: The skill assumes external lark-cli, feishu-cli, and Dev Hub tooling already exist and are appropriate for the workspace.

Mitigation: Review and install the external tooling separately before relying on this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes lark-cli or feishu-cli and python3 are available in the agent environment.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
