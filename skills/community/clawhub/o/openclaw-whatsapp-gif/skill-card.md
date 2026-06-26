## Description: <br>
Source and send relevant reaction GIFs in WhatsApp chats using safe filters and deterministic ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[witty-quotes25](https://clawhub.ai/user/witty-quotes25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find one safe, context-matching reaction GIF and send it in a WhatsApp chat when a short visual response fits the conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GIF search queries are sent to external provider services and could include sensitive personal context. <br>
Mitigation: Use concise, non-sensitive search terms and avoid sending private or sensitive personal text as GIF queries. <br>
Risk: Optional web-scraping fallback, remote URL fallback, or telemetry logging can broaden network and logging behavior if enabled. <br>
Mitigation: Keep these policy options disabled unless needed, and review references/policy.json before deployment. <br>
Risk: Downloaded media is written to an OS temp cache for local WhatsApp delivery. <br>
Mitigation: Use the built-in host allowlist and media size/type validation, and clear temp cache files according to local retention policy. <br>


## Reference(s): <br>
- [Provider notes](references/providers.md) <br>
- [Runtime policy](references/policy.json) <br>
- [ClawHub skill page](https://clawhub.ai/witty-quotes25/openclaw-whatsapp-gif) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text, JSON payloads, and local GIF/MP4/WebM media files for WhatsApp message handoff] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return ranked candidate lists, ready-to-send WhatsApp message payloads, or a payload-only handoff; local delivery writes validated media to an OS temp cache.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
