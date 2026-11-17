## Description:

Searches a curated Nano Banana Pro image-generation prompt library and recommends matching prompts with sample images, with optional customization for user-provided content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find, compare, and adapt image-generation prompts for portraits, product visuals, social posts, posters, thumbnails, illustrations, and other creative use cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-update prompt references from mutable remote GitHub data, and the security summary notes that a compromised remote manifest could cause writes outside the intended references folder.

Mitigation: Review before installing, keep updates explicit or host-controlled where possible, validate remote manifest filenames, and constrain writes to the references directory.

Risk: The security guidance notes that installer commands should be pinned and preview media fetching should be consent-aware.

Mitigation: Review installer commands before execution and ask before fetching or sending preview media in environments where media handling has privacy or policy impact.

Risk: Development documentation mentions CMS credentials for maintaining the prompt dataset.

Mitigation: Do not use or expose developer CMS credentials unless maintaining the prompt dataset and following secret-handling controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dophinl/skills/nano-banana-pro-prompts)
- [YouMind Nano Banana Pro Prompt Gallery](https://youmind.com/nano-banana-pro-prompts?utm_source=nano-banana-pro-prompts-recommend)
- [Remote Prompt References](https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill/tree/main/references)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with prompt previews, links, optional sample image references, and occasional inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends at most three prompts per request and may generate a customized English prompt after the user selects a template.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
