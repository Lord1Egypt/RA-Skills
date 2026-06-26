## Description: <br>
Provides clear, concise, best-effort general assistant behavior for Ouwibo Agent, including uncertainty disclosure and practical next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouwibo](https://clawhub.ai/user/ouwibo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ouwibo Agent users use this skill to guide general assistant responses toward concise best-effort answers, explicit assumptions when information is uncertain, and action-oriented next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search for current or latest information may send user query terms to external services. <br>
Mitigation: Avoid including secrets or sensitive personal data in search queries, and clearly state uncertainty when sourced information is incomplete. <br>
Risk: Best-effort answers can still be incomplete or incorrect when evidence is uncertain. <br>
Mitigation: Explain assumptions, cite or summarize grounding when available, and suggest a concrete next step for verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ouwibo/ouwibo-general) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ouwibo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with bullets and fenced code blocks when commands or snippets are useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only behavior guide; no executable code, persistence, or sensitive permissions are added.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
