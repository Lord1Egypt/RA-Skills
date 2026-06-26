## Description: <br>
AI note-taking assistant that captures, cleans, organizes, tags, indexes, searches, and exports text, voice, paste, URL, and photo-based notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this agent skill to turn raw notes, voice transcripts, pasted content, URLs, and photos into structured, searchable local notes with tags, categories, summaries, action items, templates, and export options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local notes may contain sensitive personal, confidential, regulated, or private URL content. <br>
Mitigation: Avoid saving secrets or regulated data unless local storage, URL fetching, long-term memory, and any dashboard sync behavior have been reviewed and explicitly approved. <br>
Risk: The skill includes file-write and export behavior for notes and indexes. <br>
Mitigation: Run setup only from a clean, known skill directory, keep exports inside the intended workspace, and back up existing note indexes before initialization or export. <br>
Risk: Security evidence flags under-bounded setup, export, network, memory, and dashboard-sync behavior for user review. <br>
Mitigation: Review the security guidance before installation and disable or require explicit approval for URL fetching, long-term memory, and dashboard or Supabase sync when not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/nollio/notetaker-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security Audit](artifact/CODEX-SECURITY-AUDIT.md) <br>
- [Configuration](artifact/config/notes-config.json) <br>
- [Dashboard Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chat responses, Markdown notes and exports, JSON note records and indexes, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores persistent local note data and can export selected notes as Markdown, JSON, or a single compiled Markdown document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and config/notes-config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
