## Description: <br>
Pinecone Memory syncs selected local Markdown memory files into Pinecone, supports semantic search, and provides health check, statistics, cleanup, backup, and restore commands through a Node.js CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenni666](https://clawhub.ai/user/chenni666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to persist selected local memory or Markdown content in Pinecone, retrieve it semantically, and run operational maintenance such as stats, heartbeat checks, cleanup, backup, and restore. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local memory or Markdown files may be uploaded to a Pinecone account, including private notes or secrets. <br>
Mitigation: Review paths before sync or restore, avoid uploading secrets or private notes, and use a scoped Pinecone API key. <br>
Risk: Scheduled heartbeat or sync commands can create ongoing remote writes and API usage. <br>
Mitigation: Use separate test and production namespaces, confirm schedule frequency before enabling cron or Task Scheduler, and monitor write verification output. <br>
Risk: Cleanup can delete data from a Pinecone namespace. <br>
Mitigation: Confirm the target index and namespace, keep backups, and run cleanup only when deletion is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenni666/pinecone-memory) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Creating Skills documentation](https://docs.openclaw.ai/tools/creating-skills) <br>
- [OpenClaw ClawHub documentation](https://docs.openclaw.ai/tools/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and CLI JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, PINECONE_API_KEY, and a Pinecone Integrated Embedding index configured with chunk_text.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact package.json reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
