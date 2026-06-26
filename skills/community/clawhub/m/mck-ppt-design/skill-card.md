## Description: <br>
Creates consultant-grade PowerPoint presentations from scratch using python-pptx and a McKinsey-style design system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likaku](https://clawhub.ai/user/likaku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, consultants, and agents use this skill to generate professional PPTX decks, slide layouts, charts, dashboards, and design-consistent business presentations programmatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks may be posted back to the active chat or workspace when OpenClaw channel delivery is available. <br>
Mitigation: For confidential board, finance, strategy, or personnel decks, disable or remove the delivery helper and verify the destination before sharing. <br>
Risk: The skill creates local PPTX files that may contain sensitive presentation content. <br>
Mitigation: Run it in a controlled workspace, review generated files before distribution, and pin dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/likaku/mck-ppt-design) <br>
- [Layout catalog](references/layout-catalog.md) <br>
- [Color palette](references/color-palette.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with Python code patterns and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks are local PPTX files; when OpenClaw channel delivery is available, the skill may post the generated deck back to the active chat or workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and changelog, released 2026-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
