## Description: <br>
Access Hedy meeting data: sessions, transcripts, highlights, todos, topics, contexts, and webhooks via the Hedy REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JulianPscheid](https://clawhub.ai/user/JulianPscheid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to query Hedy meeting sessions, transcripts, highlights, todos, topics, contexts, and webhooks from the Hedy REST API. It also guides cautious management of topics, contexts, and webhook configuration. <br>

### Deployment Geography for Use: <br>
Global, with US and EU Hedy API regions selected by user configuration. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive meeting content, including transcripts, notes, highlights, and todos. <br>
Mitigation: Use it only for intended Hedy data access, protect HEDY_API_KEY, avoid broad transcript retrieval unless needed, and keep meeting-derived output within approved tools and audiences. <br>
Risk: Webhook creation can send future meeting-derived data outside Hedy to an external URL. <br>
Mitigation: Before creating a webhook, confirm the destination host, selected events, and user intent; delete unused webhooks and avoid untrusted destinations. <br>
Risk: POST, PATCH, and DELETE endpoints can create, update, or remove topics, contexts, and webhooks. <br>
Mitigation: Show the exact proposed change before execution, require explicit confirmation, and use double confirmation for deletions. <br>


## Reference(s): <br>
- [Hedy ClawHub skill page](https://clawhub.ai/JulianPscheid/hedy) <br>
- [Hedy API US base URL](https://api.hedy.bot) <br>
- [Hedy API EU base URL](https://eu-api.hedy.bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JSON examples, and formatted meeting data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HEDY_API_KEY and typically uses curl and jq; API responses may contain sensitive meeting transcripts, notes, todos, and webhook metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
