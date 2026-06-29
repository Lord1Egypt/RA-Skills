## Description: <br>
Extracts writing style patterns from exemplar text into a reusable profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developer agents use this skill to analyze exemplar text, extract measurable style features, select representative passages, and build a reusable profile for consistent future writing or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad style-related triggers may activate the skill during general writing discussions. <br>
Mitigation: Review when the skill is active and use it only when style learning or style application is intended. <br>
Risk: Exemplar text can contain sensitive or proprietary writing samples. <br>
Mitigation: Provide only exemplar content that is appropriate for analysis and reuse in a style profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-scribe-style-learner) <br>
- [Scribe Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Feature Extraction Module](artifact/modules/feature-extraction.md) <br>
- [Exemplar Reference Module](artifact/modules/exemplar-reference.md) <br>
- [Style Application Module](artifact/modules/style-application.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown and YAML-style profile guidance with optional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces style metrics, exemplar selections, anti-patterns, validation checks, and reusable style-profile structure.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
