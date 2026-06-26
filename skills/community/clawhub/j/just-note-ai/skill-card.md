## Description: <br>
记一下 helps users capture ideas, knowledge, expenses, diary entries, tasks, and quotes like messages, with AI classification, tags, links, and local note views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yankj](https://clawhub.ai/user/yankj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture WeChat, Feishu, or CLI notes into a local Markdown knowledge base, then query, summarize, and export those records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive personal, financial, work, or message content as local notes. <br>
Mitigation: Route only content intended for capture, avoid secrets or sensitive records unless local protections are in place, and review retention or deletion controls before enabling WeChat or Feishu capture. <br>
Risk: The release relies on a just-note command-line executable that evidence says is unreviewed or missing. <br>
Mitigation: Confirm which just-note executable will run and inspect it before installing or routing messages to it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yankj/just-note-ai) <br>
- [README](README.md) <br>
- [AI message handling guide](AI-HANDLER.md) <br>
- [Examples](EXAMPLES.md) <br>
- [Test report](TEST-REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, CLI command guidance, summaries, and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores captured notes under memory/just-note and may export JSONL, Markdown, or CSV formats.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release evidence and CHANGELOG; package.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
