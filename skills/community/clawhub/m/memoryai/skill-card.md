## Description:

Long-term memory for AI agents. Your AI remembers everything - preferences, decisions, context - across sessions, forever.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ch270035](https://clawhub.ai/user/ch270035)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use MemoryAI to give an AI agent persistent memory across sessions, including preferences, decisions, identity, goals, procedures, and session summaries. The skill supports explicit store, recall, bootstrap, track, save, profile, and health commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation text, summaries, and inferred profile information may be sent to and persisted by a third-party memory service.

Mitigation: Do not use the skill for secrets, credentials, regulated personal data, private business content, or sensitive chats unless there is explicit consent and trusted retention and deletion controls.

Risk: A configurable remote endpoint receives memory and profile requests.

Mitigation: Verify that the endpoint is HTTPS and trusted before adding an API key or sending conversation content.

Risk: The HM_API_KEY credential grants access to the configured memory service.

Mitigation: Treat the API key as sensitive, store it outside shared artifacts when possible, and rotate it regularly.

## Reference(s):

- [MemoryAI service](https://memoryai.dev)
- [MemoryAI ClawHub skill page](https://clawhub.ai/ch270035/skills/memoryai)
- [Publisher profile](https://clawhub.ai/user/ch270035)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and HM_API_KEY; commands make explicit HTTPS requests to the configured MemoryAI endpoint.]

## Skill Version(s):

2.4.0 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
