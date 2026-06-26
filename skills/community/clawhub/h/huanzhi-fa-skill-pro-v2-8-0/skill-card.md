## Description: <br>
A Chinese-language fundraising advisor for founders that helps assess fundraising readiness, analyze term-sheet risks, simulate investor negotiation, and provide Capital EQ support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-innopower](https://clawhub.ai/user/ai-innopower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders and startup operators use this skill to structure fundraising preparation, review term-sheet clauses, improve pitch materials, and manage follow-up or emotional pressure during a financing process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive fundraising profiles, BP materials, term-sheet content, and progress notes that may contain confidential business information. <br>
Mitigation: Use redacted inputs where possible, keep local storage access controlled, and confirm what will be saved before recording profile or financing progress data. <br>
Risk: Broad emotional triggers and follow-up behavior could lead to unwanted memory updates or scheduled reminders. <br>
Mitigation: Require explicit user confirmation before saving data or scheduling follow-ups, and provide a clear way to skip or delete stored context. <br>
Risk: The artifact claims a ClawHub audit pass, while the server security evidence says the claim is unsupported. <br>
Mitigation: Do not rely on the audit claim in the skill text; review the current server security verdict and remove or correct unsupported safety claims before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-innopower/huanzhi-fa-skill-pro-v2-8-0) <br>
- [System prompt](references/system-prompt.md) <br>
- [Knowledge base](references/knowledge-base.md) <br>
- [Response templates](references/response-templates.md) <br>
- [Configuration guide](references/config-guide.md) <br>
- [Output schemas](references/outputs-schema.md) <br>
- [Failure handling](references/failure-handling.md) <br>
- [Known limitations](references/known-limitations.md) <br>
- [Determinism details](references/determinism-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance, configuration] <br>
**Output Format:** [Markdown guidance with structured Chinese sections and JSON outputs for diagnosis or term-sheet analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deterministic local scoring for fundraising readiness and recommends output validation with retry and fallback paths.] <br>

## Skill Version(s): <br>
2.8.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
