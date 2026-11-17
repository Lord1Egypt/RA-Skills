## Description:

Ingest a single document, uploaded file, meeting note, experiment record, or chat-provided material into a personal or team knowledge base, including summaries, source archiving, duplicate checks, and project/person aggregation updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to ingest a single uploaded file, link, meeting note, experiment record, or chat-provided item into a personal or team knowledge base. It guides target selection, duplicate handling, summary generation, source archiving, and related project or people page updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Gitea admin token and default Gitea endpoint settings, which could expose credentials or documents if deployed broadly.

Mitigation: Deploy only in a controlled environment, replace the default endpoint with an administered HTTPS Gitea URL, and use a narrowly scoped service token.

Risk: The skill can ingest and archive uploaded source files into a knowledge-base repository.

Mitigation: Constrain file inputs and archived outputs to a per-request attachment directory and review repository visibility before enabling source archiving.

Risk: Dependencies are listed without pinned versions.

Mitigation: Pin and review Python dependencies before installation.

## Reference(s):

- [Ingest Document ClawHub skill page](https://clawhub.ai/myd2002/skills/ingest-document)
- [myd2002 publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown summaries, JSON command responses, interactive card payloads, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May archive original source files and return generated Gitea page URLs when configured.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
