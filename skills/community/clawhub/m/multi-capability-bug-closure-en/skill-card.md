## Description: <br>
Unified bug investigation and closure by combining source code, database, server logs, and software platform query capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate bugs with a complete evidence chain from logs, database queries, source-code localization, and platform validation before drawing root-cause conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide agents toward sensitive maintainer workflows or high-impact operational commands. <br>
Mitigation: Review proposed commands before execution and use reduced-access review modes when full access is not required. <br>
Risk: Bug-closure conclusions can be misleading if any required evidence source is missing. <br>
Mitigation: Require source-code, database, server-log, and platform-query checks before issuing final root-cause conclusions. <br>
Risk: Investigation outputs could expose sensitive credentials or operational data. <br>
Mitigation: Use environment variables or secret managers for credentials and avoid printing plaintext secrets in outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/multi-capability-bug-closure-en) <br>
- [server-log-analysis companion skill](https://clawhub.ai/hgvgfgvh/server-log-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown investigation summary with evidence, root-cause assessment, recommendations, and verification criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires source-code, database, server-log, and platform-query evidence before final conclusions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
