## Description: <br>
ManyChat CLI is an agent-friendly command-line wrapper for automating ManyChat API tasks with stable JSON output and playbook support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent inspect ManyChat account data, manage subscribers, apply tags and custom fields, send flows or content, and run sequential JSON playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live access to ManyChat customer records and messaging. <br>
Mitigation: Install only for trusted publishers and use the narrowest available ManyChat API key. <br>
Risk: Raw endpoint calls and playbook execution can change subscriber data or send flows without enough built-in safeguards. <br>
Mitigation: Review raw and playbook actions before use and require explicit approval before changing subscriber data or sending flows. <br>
Risk: Subscriber output and logs may contain sensitive personal data. <br>
Mitigation: Treat subscriber responses and logs as sensitive data and limit retention and sharing. <br>


## Reference(s): <br>
- [ManyChat CLI release page](https://clawhub.ai/danielfoch/manychat-cli) <br>
- [danielfoch publisher profile](https://clawhub.ai/user/danielfoch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash examples and JSON command output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI responses use JSON objects with ok/result or ok/error fields and exit codes for orchestration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
