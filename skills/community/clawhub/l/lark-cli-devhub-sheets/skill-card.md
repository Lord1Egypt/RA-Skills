## Description: <br>
Use when using Feishu/Lark Sheets through lark-cli or feishu-cli for office reports, QA matrices, release checklists, KPI trackers, imports/exports, tabular analysis, and Dev Hub artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Feishu/Lark Sheets via lark-cli or feishu-cli for office reports, QA matrices, release checklists, KPI trackers, imports, exports, tabular analysis, and Dev Hub artifact workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sheet write commands can modify shared business spreadsheets if the target URL, range, or JSON payload is wrong. <br>
Mitigation: Review Sheet URLs, ranges, and JSON files before running write commands, and confirm the Lark/Feishu account and CLI configuration are trusted. <br>
Risk: The skill depends on an existing lark-cli or feishu-cli installation and its authenticated account permissions. <br>
Mitigation: Install and use the CLI only in an environment where its authentication, permissions, and account context are understood. <br>


## Reference(s): <br>
- [Lark CLI Dev Hub Sheets on ClawHub](https://clawhub.ai/afengzi/lark-cli-devhub-sheets) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Sheet routing guidance, CLI command examples, and Dev Hub workflow suggestions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
