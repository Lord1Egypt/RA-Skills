## Description: <br>
Transforms an Obsidian vault into a dual-layer knowledge base with raw input, structured wiki cards, daily summaries, and retrieval guidance for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warren2008-2020-spec](https://clawhub.ai/user/warren2008-2020-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and teams use this skill to organize Obsidian notes into raw INBOX material and structured WIKI cards, then expose concise summaries and search paths to an AI agent for report writing, analysis, and recurring knowledge work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may expose private Obsidian notes or sensitive vault content to an AI agent. <br>
Mitigation: Use the skill only with vaults and folders approved for AI access, and define tags or folder allowlists before enabling ingestion or search. <br>
Risk: Automatic startup injection could place private, stale, or overbroad summaries into future sessions. <br>
Mitigation: Disable or gate startup injection until summary size limits, approved folders, review steps, and refresh rules are configured. <br>
Risk: Summary pushing may send derived knowledge-base content to unintended recipients. <br>
Mitigation: Do not enable summary pushing until recipients, approval steps, logging, and privacy rules are explicitly configured. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/warren2008-2020-spec/obsidian-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with directory layouts, card templates, retrieval flow, scheduling notes, and example Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes suggested Obsidian folder conventions, daily summary structure, context-size limits, and startup/retrieval workflow guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
