## Description:

将 Markdown 文档转换为精美 PNG 图片。仅操作当前工作目录下的 Markdown 文件，不修改系统文件。当用户要求将 markdown 文件、markdown 文本转成图片、截图、png 时触发。支持多种主题（note/dark/sakura/ocean/tech 等）和尺寸（mobile/tablet/laptop/desktop）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiulanzhu](https://clawhub.ai/user/qiulanzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and documentation maintainers use this skill to convert Markdown files or Markdown text into themed PNG images for sharing, previews, and visual documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled filenames and temporary Markdown files can create command-injection or file-overwrite risk during Bash-based conversion.

Mitigation: Use only trusted working directories, keep Markdown paths relative to the current directory, avoid unusual filenames, and prefer an implementation that passes arguments through a safely quoted command or argument-array API.

Risk: The skill depends on a globally installed npm converter, which may vary across environments.

Mitigation: Verify the installed md2png-cli version before conversion and use npx --no-install so execution does not fetch packages at runtime.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash command snippets and generated PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports theme and size options; requires a locally available md2png-cli installation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
