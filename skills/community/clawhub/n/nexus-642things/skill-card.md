## Description:

生成「642件可写的小事」H5 创意写作应用，当用户请求 642、创意写作、写作灵感或生成写作 H5 时，代理会生成一个完整的单文件 HTML 应用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwter](https://clawhub.ai/user/lwter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a mobile-first creative-writing H5 app with writing prompts, local work storage, progress tracking, and a small portfolio view. It is intended for low-friction creative writing and writing-inspiration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite a local HTML app file when invoked from broad trigger phrases.

Mitigation: Use an explicit prompt and output path, and review the target path before allowing the file write.

Risk: Generated writing content is stored in the browser through localStorage on the user's device.

Mitigation: Avoid entering sensitive personal information into the generated app unless the local browser storage behavior is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwter/skills/nexus-642things)
- [ClawHub publisher profile](https://clawhub.ai/user/lwter)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration instructions, Guidance]

**Output Format:** [Single-file HTML with inline CSS and JavaScript, plus concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated app is designed to run locally in a browser with no external dependencies and uses browser localStorage for saved writing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
