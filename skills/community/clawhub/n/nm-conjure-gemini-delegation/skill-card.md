## Description: <br>
Delegates tasks to Gemini CLI implementing delegation-core for Google's models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route large-context analysis, summarization, batch processing, and pattern extraction tasks to Gemini CLI when delegation-core selects Gemini or Google's models are appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad delegation triggers can activate the skill more often than intended and send selected files to Gemini. <br>
Mitigation: Use explicit Gemini delegation requests, review included @path or recursive glob inputs before execution, and avoid broad terms such as cli or google for unrelated tasks. <br>
Risk: Large recursive context patterns can include more source files or sensitive content than needed. <br>
Mitigation: Prefer narrow file paths and selective globs, and review the selected files before sending them through Gemini CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conjure-gemini-delegation) <br>
- [Claude Night Market conjure plugin](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [Gemini-specific configuration](artifact/modules/gemini-specifics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Gemini CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Gemini CLI command construction, authentication guidance, model selection, JSON-output options, and saved delegation output paths.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
