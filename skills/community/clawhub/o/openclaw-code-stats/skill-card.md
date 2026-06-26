## Description: <br>
Analyzes a code repository to report file counts, line counts, and language distribution so users can understand project size and complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[douduandou](https://clawhub.ai/user/douduandou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a workspace and understand repository scale, code volume, and language mix. It is useful for quick project sizing, complexity review, and tracking codebase composition over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads files under a hardcoded local OpenClaw workspace path. <br>
Mitigation: Review the configured workspace path before running the skill and edit the script if a different repository should be analyzed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/douduandou/openclaw-code-stats) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, shell commands, guidance] <br>
**Output Format:** [Console text summary with totals and per-language breakdowns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local workspace files to compute aggregate counts; does not modify files or transmit data according to security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
