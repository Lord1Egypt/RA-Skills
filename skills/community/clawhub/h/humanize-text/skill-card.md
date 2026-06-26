## Description: <br>
Humanize AI-generated text by removing telltale AI writing patterns such as em dashes, filler phrases, structural tells, and sycophantic openings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rustyorb](https://clawhub.ai/user/rustyorb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Writers, editors, developers, and other external users use this skill to clean AI-sounding prose while preserving meaning, technical accuracy, and the author's existing voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit files that users ask it to process. <br>
Mitigation: Use copies or version-controlled documents for important content and review diffs before keeping changes. <br>
Risk: Automated wording changes can alter meaning, technical terms, or records if applied too broadly. <br>
Mitigation: Avoid applying it to code, configuration, sensitive records, or domain-specific content unless intended, and preserve technical accuracy during review. <br>


## Reference(s): <br>
- [Extended AI Pattern Reference](references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional diff summaries and file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rewrite requested text or edit requested files; users should review changes before keeping them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
