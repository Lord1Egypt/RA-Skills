## Description:

Convert Chinese text to Pinyin with optional tone marks, tone stripping, or uppercase initials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, language learners, and Chinese-language tooling authors use this skill to convert Chinese text snippets to Pinyin for learning, input-method prototyping, and text processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted output may be incomplete or inaccurate because the bundled converter covers only a small embedded character set and can silently omit unsupported characters or whitespace.

Mitigation: Use it for lightweight learning or prototyping, and review or validate results before relying on them in user-facing language workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Code]

**Output Format:** [Markdown guidance with inline shell commands; the bundled script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The converter uses a small embedded character set and may omit unsupported Chinese characters or whitespace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
