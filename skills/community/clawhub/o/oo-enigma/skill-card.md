## Description:

Operate Enigma through a connected OOMOL account to read, create, update, and delete data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business teams use this skill to query Enigma business data and manage lists or suggestions through a connected account. The skill requires confirmation before write actions and explicit approval before deleting a list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes downloaded CLI installation code without a separate approval step.

Mitigation: Review and approve CLI installation separately, and use a verified release.

Risk: The connected Enigma account may have broader access than a task requires.

Mitigation: Restrict the connected account to the permissions needed for the task.

Risk: Write and deletion actions can change or remove Enigma data.

Mitigation: Keep the skill's confirmation requirement for writes and explicit approval requirement for deletions.

## Reference(s):

- [Enigma API documentation](https://developers.enigma.com/docs/getting-started)
- [Enigma](https://www.enigma.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action; enriched business data may include raw provider payloads.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
