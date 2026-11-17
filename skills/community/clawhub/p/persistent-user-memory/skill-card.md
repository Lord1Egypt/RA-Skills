## Description:

Manages long-term local user memory across sessions for personalization, learning preferences, contacts, and patterns to tailor assistance continually.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyadhrif](https://clawhub.ai/user/eyadhrif)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to give agents local, structured long-term memory for preferences, contacts, recurring tasks, and prior interaction summaries so future assistance can be personalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically builds and changes a persistent plaintext profile about the user and contacts.

Mitigation: Install only when long-term local profiling is intentional; review the memory file regularly and avoid storing sensitive personal or business details.

Risk: The local memory file can expose personal or contact data to anyone with filesystem access.

Mitigation: Use restrictive file permissions or encryption before broad use, and define a clear disable and delete workflow.

Risk: Silent memory writes may preserve incorrect, stale, or overly broad preferences.

Mitigation: Use explicit opt-in or write review for sensitive updates, enforce retention limits, and honor correction and deletion requests promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eyadhrif/skills/persistent-user-memory)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [Example user profile](artifact/user_profile.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text, JSON]

**Output Format:** [Markdown instructions with JSON profile schema and shell installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local plaintext JSON profile at ~/.openclaw/memory/user_profile.json when enabled.]

## Skill Version(s):

1.0.0 (source: release evidence, changelog, and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
