## Description: <br>
运行 GitHub 热榜脚本，获取每日前十项目名称和简介，并协助翻译成中文。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongym1234](https://clawhub.ai/user/kongym1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitHub watchers use this skill to fetch the current daily top 10 GitHub trending projects and present translated Chinese names and descriptions for quick review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes a live request to GitHub, so results may be unavailable, rate-limited, or affected by upstream page changes. <br>
Mitigation: Run it only when live public GitHub data is acceptable, and review the generated list before relying on it. <br>
Risk: The script depends on Python packages such as requests and beautifulsoup4 being available. <br>
Mitigation: Verify dependencies in the execution environment before invoking the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongym1234/github-daily-trending) <br>
- [GitHub Trending daily page](https://github.com/trending?since=daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted Chinese list with project names and descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live public GitHub data at invocation time; output is limited to 10 projects when the upstream page can be fetched.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
