## Description:

Happy Notes lets agents manage iflow knowledge bases, import files, URLs, and text, search web or academic sources, and generate reports, presentations, podcasts, mind maps, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflow-ai-skill](https://clawhub.ai/user/iflow-ai-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize iflow knowledge bases, save notes or source material, retrieve knowledge-base content, and create downstream content such as reports, presentations, podcasts, mind maps, and videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents, pasted notes, URLs, searches, and generated outputs may be sent to iflow.

Mitigation: Install only when this data transfer is acceptable, and avoid submitting sensitive content unless the iflow account and workspace are approved for it.

Risk: Broad triggers and full-knowledge-base defaults could expose or alter more user data than intended.

Mitigation: Verify the target knowledge base and selected files before import, delete, share, search, or generation actions.

Risk: Credential or endpoint misconfiguration could send requests to an untrusted service.

Mitigation: Use IFLOW_API_KEY or a chmod 600 config file for the API key, and avoid IFLOW_BASE_URL unless the endpoint is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iflow-ai-skill/skills/happy-notes)
- [Publisher profile](https://clawhub.ai/user/iflow-ai-skill)
- [iflow](https://iflow.cn)
- [API reference](references/api.md)
- [Pipeline reference](references/pipelines.md)
- [Knowledge-base matching reference](references/kb-matching.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status summaries; generated iflow artifacts may include PDF, DOCX, Markdown, PPT, XMIND, podcast audio, or video.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous generation flows for longer report, presentation, mind-map, podcast, and video outputs.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
