## Description: <br>
Analyzes memes, screenshots, and Telegram media by decomposing visual and text elements, researching cultural references in their original language, and explaining the humor and context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antibagr](https://clawhub.ai/user/antibagr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to explain image memes, screenshots, and jokes, especially Russian-language and Telegram-distributed memes that require cultural research. It can also support scheduled Telegram meme ingestion and maintain reusable memory about meme templates, references, and channel profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ingest Telegram media and channel content automatically. <br>
Mitigation: Limit ingestion to approved public or authorized channels and keep human review around any channel configuration or downloaded media processing. <br>
Risk: The skill can persist user explanations and channel profiles without explicit retention boundaries. <br>
Mitigation: Configure the agent to ask before saving user-provided explanations or long-term channel profiles, and periodically review stored memory for retention and consent concerns. <br>
Risk: Private screenshots or meme text may be searched externally during analysis. <br>
Mitigation: Avoid using the skill on private or sensitive screenshots unless external search is acceptable for that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antibagr/meme-analyst) <br>
- [Publisher profile](https://clawhub.ai/user/antibagr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or conversational text with structured meme analysis and optional memory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce reference, twist, humor, irony, and context explanations; in ingestion mode it may also propose or update memory files for templates, references, channel profiles, and summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
