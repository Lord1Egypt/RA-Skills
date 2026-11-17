## Description:

OSM AI Bridge connects an agent workflow to browser-based AI assistants through Chrome DevTools Protocol, supporting browser launch, anti-detection script injection, storage access, and Ask/Discuss/Verify collaboration modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanara-osm](https://clawhub.ai/user/yanara-osm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route prompts to logged-in Doubao or Gemini browser sessions for direct questions, multi-angle discussion, and answer checking from an OpenClaw workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-browser and storage access can expose cookies, localStorage, and active sessions.

Mitigation: Use an isolated browser profile with no sensitive accounts or data, and avoid connecting it to a normal logged-in browser.

Risk: Anti-detection behavior changes browser automation fingerprints and may conflict with service rules or user expectations.

Mitigation: Review applicable service terms and disable or remove anti-detection behavior where it is not explicitly allowed.

Risk: Prompts and response fragments may be sent to third-party AI services and retained in local logs.

Mitigation: Use non-sensitive prompts, get approval before sending confidential content, and rotate or clear logs under ~/.openclaw/ai_bridge when needed.

Risk: The security verdict is suspicious because the design combines broad browser access, storage access, anti-detection, and persistent logging without strong safeguards.

Mitigation: Perform manual review before installation or execution, and restrict use to controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanara-osm/skills/osm-ai-bridge)
- [Doubao](https://www.doubao.com)
- [Gemini](https://gemini.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single response stream; may include assistant replies, discussion summaries, errors, and the local log file path.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact changelog lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
