## Description: <br>
Pure file-based interaction with a local Logseq graph. Read, write, search, and manage Logseq journals and pages via direct `.md` file operations. No plugins or HTTP APIs needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ham-5on](https://clawhub.ai/user/ham-5on) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, note-taking power users, and external agents use this skill to read, write, search, and manage local Logseq journals and pages through direct Markdown file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to read and modify local Logseq graph files, which can expose or alter personal notes if pointed at the wrong directory. <br>
Mitigation: Install only when comfortable with that file access, double-check the graph path, and use a backup or test graph before write operations. <br>
Risk: Examples that inspect Logseq transit files may reveal local index contents beyond ordinary page and journal Markdown. <br>
Mitigation: Avoid the transit-file examples unless intentionally inspecting local Logseq index files. <br>


## Reference(s): <br>
- [Logseq](https://logseq.com) <br>
- [Logseq Documentation](https://docs.logseq.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/ham-5on/logseq-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file-operation guidance for a user-provided local Logseq graph path.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
