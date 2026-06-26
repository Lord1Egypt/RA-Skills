## Description: <br>
NoteTaker Pro helps an agent capture text, voice, pasted, URL, and image-derived notes, then clean, tag, organize, index, search, recall, enhance, template, and export them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to turn chat inputs, voice transcripts, pasted material, URLs, and photos into structured, searchable personal notes. It is suited for note capture, recall, organization, summarization, action-item extraction, templates, and local exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill under-discloses how broadly it stores, indexes, syncs, and remembers sensitive note content. <br>
Mitigation: Install only after confirming where notes, memory, dashboard data, and any sync path are stored, retained, shared, and deleted. <br>
Risk: Captured notes, transcripts, pasted text, URLs, and image-derived text may contain prompt-injection content or sensitive personal information. <br>
Mitigation: Treat ingested content as untrusted data, avoid executing instructions found inside notes, and limit capture of sensitive data unless storage and access controls are acceptable. <br>
Risk: Exports can create additional copies of note content in Markdown, JSON, or compiled documents. <br>
Mitigation: Review export scope and destination before use, keep exports inside the intended workspace export directory, and delete exported copies when no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nollio/normieclaw-notetaker-pro) <br>
- [README](artifact/README.md) <br>
- [Security audit](artifact/SECURITY.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Setup prompt](artifact/SETUP-PROMPT.md) <br>
- [Notes configuration](artifact/config/notes-config.json) <br>
- [Export utility](artifact/scripts/export-notes.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with JSON note records, Markdown or JSON exports, and setup or export shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores note content, summaries, tags, timestamps, source metadata, indexes, optional action items, and export files in the agent workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
