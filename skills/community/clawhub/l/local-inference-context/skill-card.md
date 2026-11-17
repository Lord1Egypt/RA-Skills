## Description:

Context management for self-hosted LLM backends (llama.cpp, Ollama) that helps prevent mid-task 503 errors and context overflows caused by VRAM-limited KV caches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joekravelli](https://clawhub.ai/user/joekravelli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running agents against local llama.cpp or Ollama backends use this skill to manage context pressure, calibrate VRAM-aware thresholds, and choose when to checkpoint, compact, retry, or start a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational checkpoints and local backend status may be stored in memory.

Mitigation: Avoid writing secrets, tokens, or sensitive prompt contents into checkpoints; keep memory entries limited to task state, paths, ports, fill levels, and error signals.

Risk: Troubleshooting guidance may query localhost inference endpoints.

Mitigation: Confirm that localhost endpoints point to the intended local backend and avoid sharing sensitive service responses in logs or transcripts.

Risk: The guidance is tailored for local llama.cpp and Ollama context pressure, so it may be over-conservative or incomplete for other providers.

Mitigation: Use this skill when local inference behavior matches the evidence, and prefer a provider-specific context skill for cloud or unrelated backends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joekravelli/skills/local-inference-context)
- [Publisher profile](https://clawhub.ai/user/joekravelli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, status checklists, and checkpoint templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are operational recommendations for local inference context management; no files or network calls are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
