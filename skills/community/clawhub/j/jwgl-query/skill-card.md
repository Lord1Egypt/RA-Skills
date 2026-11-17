## Description:

Query a university JWGL/education administration system for teacher-facing schedules and exam-related arrangements, and help manage saved school URLs and teacher credentials through natural-language interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jovial-liu](https://clawhub.ai/user/jovial-liu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query teacher weekly course schedules, invigilation duties, course exam arrangements, and exam information from legacy JWGL sites. The agent gathers missing school, teacher, term, and credential details in natural language, then runs the underlying local scripts and summarizes results in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores teacher JWGL usernames and passwords locally in plaintext.

Mitigation: Use dedicated, least-privileged accounts where possible, keep config.json out of shared folders and source control, and avoid passing passwords on the command line.

Risk: The skill automates authenticated logins to user-configured school URLs and trusts those configured URLs broadly.

Mitigation: Verify each school URL is the real HTTPS institutional domain before saving it, and configure only trusted JWGL sites.

Risk: Debug and probe modes may create local output files from authenticated JWGL pages.

Mitigation: Use debug or probe modes only when needed, protect their output directories, and delete generated artifacts after troubleshooting.

## Reference(s):

- [Config format](artifact/references/config-format.md)
- [Query types](artifact/references/query-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Chinese natural-language summaries, Markdown guidance, shell command examples, and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query JSON includes fields such as query_type, teacher, term, count, rows, and details for aggregate exam queries.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
