## Description:

Generates AI images and videos through the AI Artist API from text prompts and optional reference media, then polls asynchronous jobs until completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create images or videos from prompts, upload local reference media for generation workflows, and return generated media as URLs, Markdown, JSON, or downloaded files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images or videos are sent to AI Artist for generation and upload workflows.

Mitigation: Use only media and prompts that are appropriate to share with the provider, and confirm retention and sharing terms before using private or sensitive content.

Risk: Optional Feishu webhook notifications can post prompts and generated result links to a configured workspace.

Mitigation: Set FEISHU_WEBHOOK_URL only in environments where that disclosure is intended, and avoid shared shells or shared configuration files for private work.

Risk: The AI_ARTIST_TOKEN grants API access and may need rotation if exposed in logs or shared environments.

Mitigation: Store the token in a private environment variable or protected .env file, avoid printing it, and rotate it after any suspected exposure.

Risk: The download option retrieves provider-returned media URLs without validating URL destination or download size.

Mitigation: Use --download only for trusted generation results, review output locations, and avoid running downloads in sensitive network environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/image-video-gen)
- [AI Artist API reference](references/api.md)
- [Chat integration reference](references/chat-integration.md)
- [Feishu integration reference](references/feishu-integration.md)
- [AI Artist login](https://ai.deepsop.com/login?source=2)
- [AI Artist registration](https://ai.deepsop.com/register?source=2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated media URLs, one-line JSON, Markdown image links, or local file paths from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external AI Artist endpoints, upload reference media, poll job status, optionally download returned media, and optionally send Feishu webhook notifications.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
