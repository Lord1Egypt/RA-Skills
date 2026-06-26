## Description: <br>
Runs Gemini Deep Research through the Gemini CLI deep-research MCP extension, then polls for completion and saves the resulting research report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to launch long-running Gemini Deep Research tasks for market, industry, geopolitical, investment, or other multi-source research. It is intended for environments where the user has installed Gemini CLI, the external deep-research extension, and a paid Google AI API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run background automation that messages Discord and triggers a downstream NotebookLM workflow without clear upfront consent. <br>
Mitigation: Require explicit user confirmation before enabling downstream agent chaining, or remove the NotebookLM trigger for sensitive or regulated work. <br>
Risk: Research content may be saved locally and passed through Discord, OpenClaw, or NotebookLM. <br>
Mitigation: Avoid sensitive inputs unless those destinations are approved, choose an appropriate output path, avoid full-response logging where possible, and clean up task folders after use. <br>
Risk: The workflow depends on an external Gemini Deep Research extension and paid Gemini API usage. <br>
Mitigation: Install only from a trusted source, pin or review the extension version before use, and confirm paid API quota and billing expectations. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Gemini CLI Deep Research Extension](https://github.com/allenhutchison/gemini-cli-deep-research) <br>
- [Google AI Studio API Keys](https://aistudio.google.com/apikey) <br>
- [NotebookLM](https://notebooklm.google.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/skywalker-lili/jclaw-gemini-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown reports, JSON status objects, and concise status messages with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates task metadata, poll logs, and saved report files; default polling is every 5 minutes for up to 40 minutes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
