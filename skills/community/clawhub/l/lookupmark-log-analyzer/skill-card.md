## Description: <br>
Securely analyze system and application logs with automatic sensitive data redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect whitelisted local service logs, summarize error patterns, and search recent log output with automatic redaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local logs can contain sensitive or operational details even when automatic redaction is enabled. <br>
Mitigation: Install only when the agent should inspect the listed logs, use specific source or search prompts, and review output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lookupmark/lookupmark-log-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text summaries or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local log inspection with configurable error and redaction patterns.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
