## Description: <br>
Generates text in a learned writing voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, developers, and external users can use this skill to draft prose that follows a saved voice profile, selected register, and user-provided source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads local voice profiles and optional project overrides, so output can be shaped by profile content the user did not intend to apply. <br>
Mitigation: Review the selected voice profile, register, and any .voice/override.md file before using generated text. <br>
Risk: Writing-voice generation can reproduce sensitive stylistic or source-material patterns. <br>
Mitigation: Use only profiles and source material the user is authorized to use, and manually review final drafts before sharing. <br>
Risk: Silent banned-phrase and punctuation cleanup may alter wording before the user sees the draft. <br>
Mitigation: Manually check final text against the intended meaning, style, and punctuation requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-voice-generate) <br>
- [Claude Night Market scribe plugin](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated prose and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May load local voice profiles and project overrides, generate prose in sections, silently clean banned phrases and punctuation, and optionally dispatch review agents.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
