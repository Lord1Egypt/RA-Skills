## Description: <br>
Capture meeting transcripts from Fireflies.ai via polling or webhooks and write structured markdown summaries, action items, decisions, and full transcripts to memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessewunderlich](https://clawhub.ai/user/jessewunderlich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to capture Fireflies.ai meeting transcripts on demand, on a polling schedule, or through webhooks, then review saved meeting summaries, action items, topics, and speaker-labeled transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists sensitive meeting content, including participants, summaries, action items, and speaker-labeled transcripts. <br>
Mitigation: Review stored meeting files regularly, restrict access to the memory directory, and delete captured records that are no longer needed. <br>
Risk: The optional webhook server can be exposed publicly, and signature verification is disabled when no webhook secret is configured. <br>
Mitigation: Prefer polling unless real-time capture is required, and configure a strong webhook secret before exposing the server through a tunnel or public URL. <br>
Risk: The Fireflies API key enables transcript access for the configured account. <br>
Mitigation: Store the key only in the documented secrets path, rotate or remove it when capture is no longer needed, and remove scheduled polling jobs or webhook tunnels that are no longer in use. <br>


## Reference(s): <br>
- [Meeting Transcripts on ClawHub](https://clawhub.ai/jessewunderlich/meeting-transcripts) <br>
- [Fireflies GraphQL API](https://api.fireflies.ai/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with JSON status messages and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes transcript files under memory/meetings and may print JSON status for polling results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
