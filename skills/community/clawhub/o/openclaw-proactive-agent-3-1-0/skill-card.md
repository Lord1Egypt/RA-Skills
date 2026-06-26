## Description: <br>
Openclaw Proactive Agent 3.1.0 helps agents maintain persistent memory, perform proactive check-ins, recover from context loss, and improve safely through documented guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q262045312-ui](https://clawhub.ai/user/q262045312-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a proactive agent that records durable memory, performs periodic self-checks, handles onboarding, and proposes useful work while requiring approval for external or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages durable memory, which can retain sensitive user or workspace context. <br>
Mitigation: Restrict which files and accounts the agent may access, periodically inspect or purge created memory files, and avoid storing secrets in memory documents. <br>
Risk: The skill supports proactive and autonomous local-environment work. <br>
Mitigation: Require confirmation before deletion, cleanup, external sends or posts, and operating-rule changes; limit crons and sub-agent permissions to approved scopes. <br>
Risk: A proactive agent may process untrusted external content while also using private memory. <br>
Mitigation: Treat external content as data, not instructions; use prompt-injection checks and require approval before actions that leave the machine. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/q262045312-ui/openclaw-proactive-agent-3-1-0) <br>
- [Publisher profile](https://clawhub.ai/user/q262045312-ui) <br>
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md) <br>
- [Security Patterns Reference](artifact/references/security-patterns.md) <br>
- [Security Audit Script](artifact/scripts/security-audit.sh) <br>
- [Author profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with workspace template files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional local security-audit script and reusable reference documents.] <br>

## Skill Version(s): <br>
3.1.0 (source: artifact/SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
