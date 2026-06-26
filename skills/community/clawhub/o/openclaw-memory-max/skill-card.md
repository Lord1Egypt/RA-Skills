## Description: <br>
OpenClaw memory suite with auto-recall, cross-encoder reranking, multi-hop search, causal graph memory, episodic memory, and scheduled consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanistolberg](https://clawhub.ai/user/stanistolberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent local memory, proactive recall, memory search, experience-graph lookup, and consolidation to agent sessions. It is intended for agents that should reuse prior preferences, decisions, corrections, and task outcomes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived data and later re-inject remembered content into agent context. <br>
Mitigation: Install only when persistent local memory is desired, review retained sidecar files periodically, and delete stale or sensitive memory artifacts when they are no longer needed. <br>
Risk: Auto-capture and rule pinning can increase disclosure and prompt-influence risk if enabled without controlling write access to the memory directory. <br>
Mitigation: Keep auto-capture and rule pinning disabled unless explicitly needed, and restrict write access to the OpenClaw memory directory and MEMORY.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stanistolberg/openclaw-memory-max) <br>
- [Project homepage](https://github.com/stanistolberg/openclaw-memory-max) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, configuration] <br>
**Output Format:** [Injected memory context blocks, structured JSON tool results, and Markdown consolidation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw memory sidecar files; auto-capture and rule pinning are configurable.] <br>

## Skill Version(s): <br>
3.0.4 (source: ClawHub release evidence; artifact package and README list 3.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
