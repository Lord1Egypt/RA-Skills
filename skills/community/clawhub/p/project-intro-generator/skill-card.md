## Description:

一键生成项目介绍页，支持本地编辑和长图导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunyashaw](https://clawhub.ai/user/kunyashaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scan a local project or existing HTML file and generate a project introduction page plus an exported long PNG screenshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe handling of remote repositories and untrusted HTML may let attacker-controlled input run code or make network requests.

Mitigation: Use the skill only with trusted project directories and HTML files, and run it in an isolated workspace without secrets or private network access.

Risk: The hidden --git option is not suitable for untrusted repository URLs.

Mitigation: Avoid --git for untrusted repositories until shell-safe git invocation is added.

Risk: Rendering untrusted README or HTML content can expose the browser renderer to attacker-controlled content.

Mitigation: Avoid rendering untrusted content until HTML sanitization and restricted Playwright rendering are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kunyashaw/skills/project-intro-generator)
- [Project repository link from skill documentation](https://github.com/kunyashaw/createRepoIntro)
- [Demo video](https://www.youtube.com/watch?v=6ZRcgbdZSXw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance plus generated HTML and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated HTML is editable and the PNG is exported from the rendered page when Playwright is available.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
