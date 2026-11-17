## Description:

Turn smart glasses photos into social media posts by monitoring a Google Drive folder for new images, analyzing them with vision AI, drafting posts in the user's voice, and publishing only after approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junebugg1214](https://clawhub.ai/user/junebugg1214)

### License/Terms of Use:


## Use Case:

External users and creators use this skill to turn smart-glasses photos into reviewed social media drafts and optional approved posts. It supports hands-free content workflows that depend on a dedicated photo folder, vision analysis, caption drafting, and processed-file tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart-glasses photos may include bystanders, sensitive locations, private documents, or other content that should not be analyzed or posted.

Mitigation: Use a private, dedicated Google Drive folder containing only photos intentionally submitted for social posting, and review each image and draft before approval.

Risk: Public link sharing for the Google Drive folder can expose photos beyond the intended workflow.

Mitigation: Avoid public link sharing where possible and restrict access to the minimum accounts or tools needed for processing.

Risk: Posting credentials or automated publishing settings could allow unintended publication.

Mitigation: Keep social posting credentials separate and require explicit approval for every post.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/junebugg1214/skills/glasses-to-social)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, image-analysis summaries, and social post drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafted posts require explicit user approval before publishing; scripts can emit new-photo paths and update processed-photo tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
