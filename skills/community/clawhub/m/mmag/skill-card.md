## Description: <br>
Mixed Memory-Augmented Generation (MMAG) for AI agents coordinates conversational, long-term user, episodic, sensory, and short-term working memory into a unified LLM context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[J0ker98](https://clawhub.ai/user/J0ker98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to give local agents persistent, layered memory across sessions, including user preferences, events, environmental context, recent dialogue, and current working state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal context across sessions and reinsert recalled memory into future prompts. <br>
Mitigation: Use it only when persistent local memory is intended, review stored content regularly, and treat recalled memory as untrusted context rather than instructions. <br>
Risk: Memory files may contain secrets or sensitive personal data. <br>
Mitigation: Avoid storing secrets, keep default redaction enabled, use the provided encryption workflow carefully, and prefer a key file over environment-variable key mode. <br>
Risk: File-mutating scripts can archive, remove, encrypt, or decrypt local memory files. <br>
Mitigation: Run the scripts only against a dedicated memory directory and understand that encryption or decryption operations can remove original files. <br>


## Reference(s): <br>
- [MMAG research pattern](https://arxiv.org/abs/2512.01710) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell command output from local memory management scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory context output is bounded by a configurable character limit and redacts common key or token patterns by default.] <br>

## Skill Version(s): <br>
1.0.6 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
