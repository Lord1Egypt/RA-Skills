## Description:

Convert Markdown articles into LinkedIn-ready rich text, with options for table flattening or images and an HTML file for browser-based copying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to prepare Markdown drafts for LinkedIn's article editor. It converts common Markdown formatting into rich text, provides table handling choices, and gives a browser-copy fallback when clipboard use is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional table-image rendering uses Chromium with its sandbox disabled, which the security review identifies as a concern; the scan was partial and the tool scope was not fully resolved.

Mitigation: Use the default table-flattening mode for untrusted Markdown. Review the required local tools and use image rendering only in an environment where running Chromium without its sandbox is acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/j3ffyang/skills/md-to-linkedin)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [Relative-link base used by the converter](https://github.com/j3ffyang/ai-thoughts/blob/main/docs/)

## Skill Output:

**Output Type(s):** [HTML, Files, Text]

**Output Format:** [LinkedIn-ready HTML fragment; optional HTML, PNG, and DOCX files, with textual notes and image-upload checklist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves headings, links, lists, quotes, and code by default. Tables flatten to bullets unless image or keep mode is selected; source images become placeholders and require manual upload.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
