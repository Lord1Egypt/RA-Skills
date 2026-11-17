## Description:

Builds structured LLM prompts from a chapter outline, optional voice profile, and character files to help generate novel chapter prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and developers use this skill to prepare chapter-generation prompts for local novel projects. It combines a Markdown chapter outline with optional style and character YAML files, then outputs a Markdown prompt package for review before use with an LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path handling can read files outside the intended book project when untrusted users control input paths.

Mitigation: Use the skill only with trusted local book projects, fix the project directory in automation, and do not let untrusted users choose --outline or --output values.

Risk: Project text can be carried into generated prompts and treated as instructions by a downstream LLM.

Mitigation: Review generated prompt files before sending them to an LLM and remove or neutralize unexpected instructions from outline, style, or character content.

Risk: Unpinned dependencies can change behavior over time in automated use.

Mitigation: Pin rich and PyYAML versions in deployment environments and install from trusted package sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/novel-writer-v2)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown prompt file with system and user prompt sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Markdown and YAML inputs; no network call or credentials are required by the artifact.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
