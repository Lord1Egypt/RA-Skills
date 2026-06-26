## Description: <br>
Guides an agent to respond in group chats only when directly named, clearly addressed by role, or relevant to an open capability request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebly](https://clawhub.ai/user/ebly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents used in shared or multi-agent chats use this skill to decide when to answer and when to stay silent, reducing duplicate or misdirected responses. It is intended for assistants that have a known name, role, and capability profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An inaccurate or outdated agent identity can cause the agent to miss relevant requests or respond when it was not the intended recipient. <br>
Mitigation: Keep the agent's name, role, aliases, and capability descriptions accurate in identity files and related configuration. <br>
Risk: Ambiguous group-chat messages can still be interpreted incorrectly. <br>
Mitigation: Prefer silence when the intended recipient is unclear, or ask a brief clarifying question before helping. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ebly/group-chat-response) <br>
- [Source skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only behavior guidance; no files, code, installs, credentials, or external calls are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-03-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
