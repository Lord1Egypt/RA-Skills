## Description: <br>
Answer OpenClaw-related questions by querying and analyzing the official documentation at docs.openclaw.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wx528](https://clawhub.ai/user/wx528) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to answer OpenClaw configuration, command, troubleshooting, architecture, and best-practice questions from the official OpenClaw documentation. It helps produce concise sourced guidance and user-run validation commands for OpenClaw configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest local OpenClaw configuration commands that affect a user's environment if copied and run without review. <br>
Mitigation: Present commands as user-run validation or inspection steps, explain expected output, and encourage reviewing configuration changes before applying them. <br>
Risk: Answers can become inaccurate if OpenClaw documentation is unavailable, unclear, or has changed. <br>
Mitigation: Fetch the relevant docs.openclaw.ai pages for each OpenClaw-specific answer, cite the source, and state when documentation does not clearly answer the question. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw FAQ](https://docs.openclaw.ai/faq) <br>
- [OpenClaw Troubleshooting](https://docs.openclaw.ai/troubleshooting) <br>
- [OpenClaw Configuration](https://docs.openclaw.ai/config) <br>
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with sourced prose and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is instruction-only; users run any suggested commands themselves.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
