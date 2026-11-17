## Description:

Personal Wiki helps an agent ingest IMA notes, Evernote notes, and local files into a local ~/wiki knowledge base, query and lint wiki pages, visualize the knowledge graph, and generate customized demo scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to maintain a local personal wiki from note services and local documents, then search, clean up, visualize, and reuse that knowledge for demo scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to IMA, Evernote, and local ~/wiki content.

Mitigation: Install only when that credential and content access is acceptable, and keep tokens out of chat transcripts and shared logs.

Risk: The artifact documents persistent Evernote token storage in a shell startup file.

Mitigation: Prefer an environment-specific secret store or short-lived terminal export, and rotate the token if it has been pasted or logged.

Risk: The documented dependency setup uses global Python package installation and a local package patch.

Mitigation: Use an isolated virtual environment and review dependencies before running ingestion or visualization commands.

Risk: The generated wiki graph HTML may expose sensitive imported content and uses browser-rendered markdown with remote scripts.

Mitigation: Avoid opening generated graph files for sensitive wiki content unless the viewer sanitizes markdown and avoids untrusted remote scripts.

## Reference(s):

- [ClawHub Personal Wiki skill page](https://clawhub.ai/heavenchenggong/skills/personal-wiki)
- [IMA list_note_by_folder_id endpoint](https://ima.qq.com/openapi/note/v1/list_note_by_folder_id)
- [IMA get_doc_content endpoint](https://ima.qq.com/openapi/note/v1/get_doc_content)
- [Yinxiang Developer Token page](https://app.yinxiang.com/api/DeveloperToken.action)
- [Cytoscape.js distribution](https://cdn.jsdelivr.net/npm/cytoscape@3.28.1/dist/cytoscape.min.js)
- [Marked distribution](https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets; may create markdown wiki pages, log entries, demo scripts, and a single-file HTML graph.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local ~/wiki files plus IMA and Evernote credentials when the user requests ingestion or synchronization.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
