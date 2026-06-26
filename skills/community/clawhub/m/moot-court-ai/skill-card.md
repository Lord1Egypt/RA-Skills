## Description: <br>
Simulate a full Chinese civil court hearing with 4 role-based agents (clerk, plaintiff, defendant, judge) orchestrated by deterministic Lobster workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal educators, moot-court teams, and developers can use this skill to simulate a structured Chinese civil hearing with role-based agents and staged deliberation. It supports preparation of case materials and review of exported judgments and hearing logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Case files and hearing logs may contain confidential or personal legal information. <br>
Mitigation: Redact confidential or personal details before loading real case files, and keep exported hearing logs private. <br>
Risk: Model-provider API keys can expose accounts to unintended usage or spend. <br>
Mitigation: Use dedicated DeepSeek and DashScope API keys with spending limits. <br>
Risk: A separately downloaded Lobster workflow or related script may change what runs locally. <br>
Mitigation: Review any separately downloaded workflow or script before execution. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/baobaodawang-creater/moot-court-ai) <br>
- [ClawHub skill page](https://clawhub.ai/baobaodawang-creater/moot-court-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and text guidance for running a Lobster workflow and reviewing exported hearing artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DeepSeek and DashScope API keys plus OpenClaw and Lobster binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
