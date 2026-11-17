## Description:

Minimal Flask-based multi-user chat interface enabling OpenClaw HTTP integration with persistent UI state and optional Google Maps support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeanne0r](https://clawhub.ai/user/jeanne0r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a lightweight browser chat gateway that forwards messages to an OpenClaw HTTP endpoint while maintaining local participant state and memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent household memory can retain sensitive personal or location information.

Mitigation: Use in a trusted local environment, disclose memory behavior to users, make memory opt-in where possible, and provide a way to review or clear stored memory.

Risk: Weak multi-user boundaries may allow users to select or affect another participant's identity or memory.

Mitigation: Add authentication and session isolation before shared use, and prevent users from selecting identities they are not authorized to use.

Risk: Network exposure without authentication can expose the chat gateway and local state to unintended users.

Mitigation: Bind to 127.0.0.1 by default and add access control before exposing the service beyond a trusted host.

Risk: Client-supplied system messages can change assistant behavior.

Mitigation: Reject system-role messages from clients and construct trusted system context only on the server side.

Risk: Google Maps route support can send stored home or work locations to an external service.

Mitigation: Confirm with the user before using stored locations, and restrict any Google Maps browser key to the intended origins and APIs.

Risk: Unpinned dependency versions can change runtime behavior or security properties over time.

Mitigation: Pin reviewed dependency versions and update them through a controlled review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeanne0r/skills/openclaw-web-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration]

**Output Format:** [Browser chat replies and JSON API responses, with local JSON state and memory files when those features are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return route action metadata for Google Maps and may persist participant-specific memory locally.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
