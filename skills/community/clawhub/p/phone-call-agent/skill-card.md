## Description:

AI voice call agent that can make outbound calls, generate browser call links, accept inbound calls, and return call transcripts and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlesheepxy](https://clawhub.ai/user/littlesheepxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to a self-hosted voice call service for outbound calls, browser call links, inbound call handling, and post-call transcript and summary retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running unpinned remote Docker code or images could introduce unexpected behavior before credentials are added.

Mitigation: Use a pinned commit or release and inspect the Docker Compose file and container images before deployment.

Risk: The skill uses sensitive calling, LLM, speech, and LiveKit credentials.

Mitigation: Use narrowly scoped, revocable API keys, keep them out of prompts and shared logs, and rotate keys if exposure is suspected.

Risk: Call transcripts, summaries, and optional webhooks can expose personal or business-sensitive conversation data.

Mitigation: Require consent or notice where calls are recorded or transcribed, avoid unnecessary webhooks, and define retention and deletion rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/littlesheepxy/skills/phone-call-agent)
- [Source repository from skill metadata](https://github.com/Littlesheepxy/phone-call-agent)
- [Publisher profile](https://clawhub.ai/user/littlesheepxy)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, environment variable, JSON, and plain-text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser call links and call result fields such as transcript and summary when connected to the service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
