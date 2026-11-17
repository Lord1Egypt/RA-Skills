## Description:

使用 Playwright 对本地网页、静态 HTML 或在线页面执行自动化测试、元素发现、控制台日志采集与截图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[carpedx](https://clawhub.ai/user/carpedx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate browser checks on local, static, or online pages, including screenshots, UI element discovery, and browser console log capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw user text may be passed through shell evaluation by the agent entrypoint.

Mitigation: Review or change the entrypoint so user input is passed as an argument without shell evaluation before deployment.

Risk: The helper script can start arbitrary local server commands.

Mitigation: Restrict with_server.py usage to approved commands, expected ports, and trusted users.

Risk: file:// targets and console capture can expose sensitive local content or page data.

Mitigation: Use only trusted targets and avoid sensitive local files or confidential browser console output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carpedx/skills/playwright-web-test)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown or plain text with command suggestions, Python code snippets, console logs, and MEDIA file references for screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create screenshot PNG files and console log files under the configured output directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
