## Description:

Generates responsive single-page HTML introduction and analysis pages for literary and media works, with theme color guidance, interactive sections, and structured content blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to generate polished, self-contained HTML pages that introduce, summarize, and analyze novels, films, anime, games, and similar works.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default trigger wording and page guidance are Chinese-oriented, which may route or shape output differently than expected in multilingual deployments.

Mitigation: Review and adjust trigger phrases, default language expectations, and font defaults before deployment in non-Chinese or tightly routed environments.

Risk: Generated pages may include external font loading through the documented Google Fonts mirror.

Mitigation: Review external asset loading requirements and replace the font source with an approved internal or regional source when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouchang1988/skills/page-gen)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Google Fonts mirror](https://fonts.loli.net)

## Skill Output:

**Output Type(s):** [code, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for a single self-contained responsive HTML page.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
