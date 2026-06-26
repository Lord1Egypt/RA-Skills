## Description: <br>
AI agent tool for compressing/executing shell commands with domain-aware output truncation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ether-btc](https://clawhub.ai/user/ether-btc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to shorten verbose shell command output before an agent reasons over it, especially for git diffs, git logs, grep or rg results, directory listings, and build logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell output is shortened before the agent reasons over it, so omitted lines may contain context that matters for audits, incident response, destructive operations, or secret review. <br>
Mitigation: Review raw unfiltered output before acting in high-impact workflows or when commands may emit sensitive data. <br>
Risk: A plugin package installed outside this artifact may include manifest or hook behavior that differs from the documented truncation utility. <br>
Mitigation: Confirm the installed manifest and hook files match the documented behavior before deployment. <br>
Risk: Domain-specific filters can remove details from git, grep, directory, or build output that an agent might otherwise inspect. <br>
Mitigation: Use the documented bypass or raw-output review path when complete command output is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ether-btc/openclaw-exec-truncate) <br>
- [Publisher Profile](https://clawhub.ai/user/ether-btc) <br>
- [OpenClaw Plugin SDK](https://docs.openclaw.ai/plugins/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown guidance with TypeScript code snippets, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces shortened command-output text with truncation markers; small outputs and failed filters return the original output unchanged.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
