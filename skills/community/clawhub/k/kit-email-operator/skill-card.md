## Description: <br>
AI-powered tool to create, personalize, schedule, send, and track professional email campaigns using Kit (ConvertKit) API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kevjade](https://clawhub.ai/user/Kevjade) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and business operators use this skill to generate email campaign copy, select audiences, create Kit broadcasts, schedule or send approved campaigns, and review campaign performance. It is intended for agent-assisted email marketing workflows where the user reviews content, links, targeting, and timing before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful Kit email credentials that can create, schedule, or send campaigns. <br>
Mitigation: Install only when the workspace is trusted, keep Kit credentials protected, and verify the exact email body, links, audience, timing, and draft/scheduled/immediate status before approving any send. <br>
Risk: Voice-training samples and business context may contain customer data or sensitive marketing information. <br>
Mitigation: Redact customer data from past emails before training, review local files written by the skill, and avoid using sensitive samples in shared workspaces. <br>
Risk: Stored credentials and local campaign context can remain available to anyone with workspace access. <br>
Mitigation: Restrict workspace access, review stored credential and profile files, and rotate Kit credentials if the workspace may be shared or compromised. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Kevjade/kit-email-operator) <br>
- [Kit](https://kit.com) <br>
- [OpenClaw Documentation](https://openclaw.com/docs) <br>
- [Email Marketing Best Practices](artifact/references/email-best-practices.md) <br>
- [Kit Personalization Tags Reference](artifact/references/kit-personalization.md) <br>
- [Email Sequence Templates](artifact/references/sequence-templates.md) <br>
- [Subject Line Formulas](artifact/references/subject-line-formulas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, configuration prompts, shell commands, and Kit campaign actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create drafts, update broadcasts, schedule sends, send approved campaigns, retrieve campaign statistics, and write local credential or voice-profile files during setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
