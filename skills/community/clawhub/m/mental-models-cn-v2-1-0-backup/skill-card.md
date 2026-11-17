## Description:

Chinese-language reference skill that helps an agent choose and apply mental models for business analysis, investment decisions, psychology, and systems thinking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmilton09](https://clawhub.ai/user/gmilton09)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill as a Chinese-language reference library for selecting mental models and generating structured analysis templates for strategy, investing, risk review, career choices, and communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation documentation can point users to a different package name than the canonical skill slug.

Mitigation: Verify the intended ClawHub package before installation and follow the server-resolved skill identity rather than the mismatched INSTALL.md command.

Risk: Investment-oriented frameworks and examples could be mistaken for financial advice.

Mitigation: Treat outputs as educational decision scaffolds and require qualified review before making financial decisions.

Risk: Broad triggers cover decision making, investing, psychology, and communication, which can activate the skill across sensitive contexts.

Mitigation: Invoke deliberately for analysis support and check generated conclusions against current domain evidence and professional requirements.

Risk: Some documentation still describes a recommendation script that the release changelog says was removed.

Mitigation: Expect static reference behavior and ignore script-based instructions unless the referenced script is present in the installed release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmilton09/skills/mental-models-cn-v2-1-0-backup)
- [README](artifact/README.md)
- [Model Cards](artifact/MODEL-CARDS.md)
- [Model Combos](artifact/MODEL-COMBOS.md)
- [Flowchart](artifact/FLOWCHART.md)
- [Templates](artifact/TEMPLATES.md)
- [Case Studies](artifact/CASE-STUDIES.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown guidance, checklists, and analysis templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static reference content; no MCP, API key, or tool references were detected.]

## Skill Version(s):

2.6.2 (source: server release metadata; artifact frontmatter lists 2.6.0 and changelog top entry lists 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
