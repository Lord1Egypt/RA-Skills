## Description:

Automated academic writing assistant based on a three-layer architecture: Framework Layer, Summary Layer, and Body Layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrchenkuan](https://clawhub.ai/user/mrchenkuan)

### License/Terms of Use:


## Use Case:

Students, researchers, and academic writers use this skill to structure long-form papers, process references, generate framework and summary layers, draft Markdown body sections, and synchronize changes across those layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write or overwrite academic project files while drafting body sections or synchronizing layers.

Mitigation: Set an explicit project directory, keep backups of thesis drafts, and ask for a preview before operations that may overwrite body files.

Risk: The skill may use networking for literature search and attempted downloads.

Mitigation: Review requested searches and downloaded source material before incorporating it into the paper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrchenkuan/skills/paper-engineering-assistant)
- [Publisher profile](https://clawhub.ai/user/mrchenkuan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON project files, project directories, and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update academic project files, including structs.json, summaries.json, document_body Markdown files, processed reference notes, and literature review reports.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
