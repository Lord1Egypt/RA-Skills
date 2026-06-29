## Description: <br>
Ingest Document saves a single document, uploaded file, meeting note, experiment record, link, or chat-provided material into a personal or team knowledge base with summaries, source archiving, duplicate checks, and aggregation updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to ingest one item of source material into a Gitea-backed personal or team knowledge base. It is intended for workflows that need a generated summary, preserved source context, duplicate handling, and project or people page updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write summaries and archived source files into Gitea knowledge-base repositories using broad repository credentials. <br>
Mitigation: Use a dedicated low-privilege Gitea token scoped only to the intended repositories, avoid site-admin tokens, and verify the target personal or team repository before saving. <br>
Risk: Full source files and user-provided material may be archived into repositories where other users could have access. <br>
Mitigation: Tell users when source files will be archived, avoid ingesting sensitive material unless the repository access model is appropriate, and review repository permissions regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/ingest-document) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-oriented command output with shell commands and Gitea page links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated summaries, save status, duplicate-resolution prompts, interactive card payloads, and links returned from Gitea.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
