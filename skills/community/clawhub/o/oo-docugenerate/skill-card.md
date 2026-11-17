## Description:

DocuGenerate (docugenerate.com). Use this skill for ANY DocuGenerate request — reading, creating, updating, and deleting data. Whenever a task involves DocuGenerate, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage DocuGenerate templates and generated documents through their connected OOMOL account, including listing, retrieving, generating, renaming, and deleting documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to download and run software whose installer was unavailable for inspection.

Mitigation: Use a verified oo CLI release and review and approve local installation; set OO_SKILLS_SYNC_DISABLED=1 to prevent automatic skill synchronization.

Risk: Actions use the connected DocuGenerate account and can change or delete documents.

Mitigation: Use the intended connected account, review the exact effect and payload before writes, and explicitly approve the target before deletion.

## Reference(s):

- [DocuGenerate](https://www.docugenerate.com)
- [DocuGenerate Developer Quickstart](https://www.docugenerate.com/developers/quickstart/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API responses, Guidance]

**Output Format:** [JSON responses and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, rename, or delete DocuGenerate documents.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
