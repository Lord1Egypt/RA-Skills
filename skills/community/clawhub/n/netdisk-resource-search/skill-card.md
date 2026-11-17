## Description:

Guides Chinese-language searches across public Baidu, Quark, and Aliyun Drive share-link indexes and helps filter and organize results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to locate and compare publicly indexed netdisk share links for authorized resources, including books, courses, media, and software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party share links may point to unauthorized copies of paid content.

Mitigation: Limit searches and shared results to resources the user is authorized to access; suggest licensed or free alternatives when appropriate.

Risk: The skill recommends an unpinned Docker image for an optional local search service.

Mitigation: Review the Docker command and image before running it, and pin a vetted image digest.

Risk: The skill proposes bypassing system proxies for upstream requests.

Mitigation: Do not bypass organizational or managed-device proxy policies without permission.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oracis/skills/netdisk-resource-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Chinese-language text or Markdown with share links, extraction codes, and optional Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on third-party indexes and may include duplicates or irrelevant links.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
