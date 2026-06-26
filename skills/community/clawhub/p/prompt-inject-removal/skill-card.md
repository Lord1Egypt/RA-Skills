## Description: <br>
A secure sanitization system to strip instructions from external content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Quarantiine](https://clawhub.ai/user/Quarantiine) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to summarize untrusted external content while stripping or marking prompt-injection instructions before the content is used in a conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-injection examples in the artifact may appear risky when viewed in isolation. <br>
Mitigation: Treat those examples as defensive negative constraints, consistent with the server security verdict that the release is clean and the flagged phrases support the skill's stated safety purpose. <br>
Risk: Prompt-based sanitization does not guarantee removal of all adversarial instructions. <br>
Mitigation: Review sanitized summaries before state-changing actions and use isolated sub-agents or sandboxes for high-risk workflows, as recommended by the artifact security documentation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Quarantiine/prompt-inject-removal) <br>
- [Prompt Inject Removal Security Documentation](references/security.md) <br>
- [Hardened Sanitization Prompt](PROMPT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise sanitized summary text, with an optional [INJECTION_ATTEMPT_REMOVED] marker when blatant prompt injection is detected.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [If no usable content is present, the prompt specifies the exact fallback string: [Prompt Inject Removal: No content to process].] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
