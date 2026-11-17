## Description:

A secure sanitization system to strip instructions from external content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quarantiine](https://clawhub.ai/user/quarantiine)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to sanitize summaries of untrusted external content before the main agent uses that information in a conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-based sanitization is a defense-in-depth aid, not a complete security boundary.

Mitigation: Use read-only browsing or fetch tools where possible, review summaries before state-changing actions, and prefer sandboxed or subagent execution for high-risk untrusted content.

Risk: A sanitized summary can still carry misleading or malicious content into the main agent's reasoning.

Mitigation: Treat sanitized summaries as untrusted until reviewed and avoid automatic writes, deletes, sends, or other state-changing actions based only on the summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quarantiine/skills/prompt-inject-removal)
- [ClawHub metadata homepage](https://clawhub.ai/Quarantiine/prompt-inject-removal)
- [Prompt Inject Removal Security Documentation](artifact/references/security.md)
- [Hardened System Prompt](artifact/PROMPT.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise sanitized Markdown summary with optional injection marker.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit [INJECTION_ATTEMPT_REMOVED] when blatant injection text is detected, or a no-content sentinel when input is empty or unintelligible.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
