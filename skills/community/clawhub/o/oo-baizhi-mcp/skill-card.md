## Description:

Search and read Baizhi Cloud Agent Toolkit data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search Baizhi Cloud Agent Toolkit and read or extract webpage content through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloads and create persistent changes in agent skill directories.

Mitigation: Review the CLI setup, prefer an independently verified pinned release, and limit which agent skill directories it can change.

Risk: Search inputs pass through OOMOL to Baizhi and may consume service credits.

Mitigation: Keep search inputs free of sensitive information and use focused queries to control credit use.

## Reference(s):

- [Baizhi Cloud Agent Toolkit](https://baizhi.cloud/landing/agent-toolkit)
- [Baizhi Agent Toolkit documentation](https://github.com/chaitin/baizhi-agent-toolkit)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Retrieved webpage content]

**Output Format:** [Structured JSON responses and retrieved text content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search, page reading, and extraction results; response fields vary by the selected tool.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
