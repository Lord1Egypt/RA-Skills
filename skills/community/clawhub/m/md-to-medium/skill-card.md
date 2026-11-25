## Description:

Convert a Markdown article into an HTML fragment Medium's story editor accepts on paste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers can convert Markdown drafts into HTML that can be pasted into Medium while preserving supported formatting, code blocks, and hosted images. The converter also reports the article title separately because a paste does not fill Medium's title field.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the skill suspicious, citing unsafe table rendering and image checks that may let images pass despite the stated hosting requirements.

Mitigation: Review the generated HTML and table images, and confirm each image URL is public and points to pushed content before pasting into Medium.

Risk: The security scan is partial because some local references were missing, so its review evidence is incomplete.

Mitigation: Review the complete release files and scan results before installing or using the skill.

## Reference(s):

- [md-to-medium on ClawHub](https://clawhub.ai/j3ffyang/skills/md-to-medium)
- [Publisher profile: j3ffyang](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [HTML, Text, Image URLs]

**Output Format:** [HTML fragment with a plain-text title and image hosting status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tables are represented as hosted PNG images by default or as bullet lists; images use public URLs and are checked for pushed availability.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
