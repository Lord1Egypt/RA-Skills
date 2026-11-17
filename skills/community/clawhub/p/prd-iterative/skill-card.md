## Description:

PRD Iterative guides an agent through a multi-round Chinese-language PRD drafting workflow with writer and reviewer iterations from a product topic, background material, and target platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galaxy-operations-guide](https://clawhub.ai/user/galaxy-operations-guide)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, and developers use this skill to draft and review Chinese-language PRDs over configurable writer/reviewer rounds, producing versioned PRD and review outputs in a user-confirmed location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background material or linked sources may contain private or sensitive product information.

Mitigation: Confirm the source material with the user and avoid processing sensitive inputs unless the user accepts that handling.

Risk: The workflow may fetch linked material and write PRD files to a user-specified location.

Mitigation: Confirm models, links, output folder, and round count before starting the workflow.

## Reference(s):

- [PRD standard structure reference](references/prd-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files with concise progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces versioned PRD and review Markdown files in a user-confirmed output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
