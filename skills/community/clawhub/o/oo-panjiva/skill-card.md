## Description:

Panjiva (panjiva.com). Use this skill for ANY Panjiva request — reading, creating, and updating data. Whenever a task involves Panjiva, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can use the connected Panjiva account to search companies and shipments, inspect trade data, parse HS codes, and submit supported bulk jobs. The skill guides users to inspect action schemas first and confirm the payload and effect before running actions marked as writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified installation code and introduce persistent agent skills without explaining those effects.

Mitigation: Review the CLI installation separately and disable unwanted startup skill synchronization before use.

Risk: Panjiva requests pass through the connected OOMOL account, and write actions can change state.

Mitigation: Connect only the intended account and review the exact write payloads and effects before running them.

## Reference(s):

- [Panjiva](https://panjiva.com/)
- [Panjiva API documentation](https://panjiva.com/api-guide/spec)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, CSV, JSONL, Shell commands, Guidance]

**Output Format:** [JSON responses and downloadable JSONL or CSV data, with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Panjiva action, request schema, and connected account.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
