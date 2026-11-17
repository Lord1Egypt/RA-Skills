## Description:

An apparel-focused keyword mining and semantic tagging skill that builds product context from apparel attributes, mines Amazon suggestion keywords, classifies complete attribute phrases, and separates positive, negative, and review keyword libraries for Listing and PPC workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and marketing operators use this skill to mine apparel-specific long-tail keywords, identify complete attribute phrases, and prepare structured keyword libraries for Listing optimization and PPC. It is intended for apparel categories such as dresses, tops, bottoms, and outerwear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive LinkFox credentials and user data may be sent through environment-configurable service endpoints.

Mitigation: Install only in trusted environments, pin dependencies, and keep LINKFOX_TOOL_GATEWAY and related endpoint variables pointed only at trusted LinkFox hosts.

Risk: Uploaded files can become publicly accessible.

Mitigation: Upload only files that are safe to publish and review generated workbooks, reports, and media before sharing.

Risk: Generated HTML reports may contain active content.

Mitigation: Open and distribute generated HTML reports cautiously, and review report content before external use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-apparel-keyword-mining)
- [LinkFox AIGC TextGen API](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [LinkFox Keyword Library API](artifact/skills/linkfox-keyword-library/references/api.md)
- [LinkFox File Upload API](artifact/skills/linkfox-file-upload/references/api.md)
- [LinkFox Report Layout Reference](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated Excel or JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The main workflow produces a seven-sheet Excel workbook covering summary, tagged details, positive keywords, negative keywords, review keywords, complete attribute phrases, and raw mined suggestions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
