## Description: <br>
TokenSaver is a bilingual Korean and English context memory and search skill that compresses stored agent context to reduce token usage and AI costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorongss](https://clawhub.ai/user/dorongss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use TokenSaver to save, compress, search, export, and reload local context memories while limiting the amount of text returned to an agent. It is aimed at Korean and English workflows that need cheaper recurring context recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and persist sensitive workspace, profile, business, health, and personal context in local memory stores. <br>
Mitigation: Install first in a dedicated test workspace, restrict stored categories, review the data paths before use, and clear ~/.openviking and ~/.openclaw/workspace/.openviking caches when the data is no longer needed. <br>
Risk: Auto-sync and initialization scripts may read or retain OpenClaw workspace memory, profile files, query history, and summaries without clear retention controls. <br>
Mitigation: Review auto-sync and initialization behavior before running those scripts, avoid enabling them for sensitive workspaces, and document retention expectations for users. <br>


## Reference(s): <br>
- [TokenSaver ClawHub page](https://clawhub.ai/dorongss/openviking-korean) <br>
- [API Reference](docs/API_REFERENCE.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compressed context summaries, search results, local memory files, backup data, and setup guidance.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata, clawhub.json, API reference; pyproject.toml lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
