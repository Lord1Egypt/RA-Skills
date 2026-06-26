## Description: <br>
A lottery analysis assistant for SSQ and DLT that analyzes historical draw data, tracks statistical patterns, and generates number recommendations for reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixiaohe](https://clawhub.ai/user/xixiaohe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze bundled or custom SSQ and DLT lottery history, inspect hot and cold numbers, review trends, and generate statistical recommendation outputs. The skill is for entertainment and reference workflows and does not guarantee winning outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify bundled lottery CSV data and save prediction, report, and result JSON files locally. <br>
Mitigation: Install only when local file updates are acceptable, review generated files, and use no-save behavior when prediction history should not be retained. <br>
Risk: Optional message-hook integration may process lottery-looking messages and trigger updates automatically. <br>
Mitigation: Do not enable hook integration unless that behavior is intentional, and keep message patterns scoped to expected lottery data formats. <br>
Risk: Lottery recommendations may be overinterpreted as reliable predictions. <br>
Mitigation: Present outputs as statistical reference and entertainment only, and preserve the skill's warning that results do not guarantee winning outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixiaohe/lottery-analyzer-backup-20260418-083724) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xixiaohe) <br>
- [README](README.md) <br>
- [Quick Start](QUICK_START.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files, Guidance] <br>
**Output Format:** [Markdown instructions, Python and shell snippets, console text, and JSON analysis or prediction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save prediction history, reports, results, and updated lottery CSV data locally unless run with no-save behavior where supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
