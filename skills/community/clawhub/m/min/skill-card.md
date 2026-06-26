## Description: <br>
Captures learnings, errors, feature requests, and corrections so agents can record reusable project knowledge and improve future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragon-wlf](https://clawhub.ai/user/dragon-wlf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and maintain project-local learning logs, error records, feature-request notes, and reusable agent guidance. It supports OpenClaw and general agent workflows that need persistent, reviewed learning artifacts across tasks or sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can retain sensitive notes or command output if users log too much detail. <br>
Mitigation: Prefer project-local .learnings folders and avoid storing secrets, tokens, raw transcripts, environment variables, private keys, or sensitive command output. <br>
Risk: Optional prompt and tool hooks can add reminders broadly across sessions and may inspect command output for error patterns. <br>
Mitigation: Enable hooks only after review, avoid global all-prompt hooks unless that behavior is intended, and keep hook output sanitized and minimal. <br>


## Reference(s): <br>
- [Entry Examples](references/examples.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append project-local .learnings markdown files and may provide optional hook reminders when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
