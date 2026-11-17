## Description:

Use an OOMOL-connected account to read, create, update, or delete TemplateDocs data and generate documents from templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users automating document workflows use this skill to list and inspect TemplateDocs templates, generate documents, and manage template settings or deletion through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions direct the user to run downloaded CLI installers without requiring prior approval.

Mitigation: Review and approve setup separately; prefer a reviewed, pinned installation and check whether it installs additional agent skills.

Risk: Template generation changes data, and template updates or deletion can alter or permanently remove user content.

Mitigation: Keep the skill's explicit confirmations for changes and deletions; review the exact target and payload before approving the action.

## Reference(s):

- [TemplateDocs](https://templatedocs.io)
- [TemplateDocs API overview](https://templatedocs.io/docs/api/overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands, Guidance]

**Output Format:** [TemplateDocs data and generated DOCX or PDF files, with actions issued through oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The returned content depends on the selected TemplateDocs action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
