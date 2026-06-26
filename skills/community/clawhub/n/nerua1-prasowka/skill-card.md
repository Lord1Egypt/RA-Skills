## Description: <br>
Generate a daily news portal as a single HTML file with fetched public news, summaries, category sections, theme controls, and a responsive layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to assemble a daily Polish-language news portal covering AI, technology, science, markets, world news, and Poland. It is intended to fetch public news items, summarize article content, and write a local HTML page for browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party news sites and public APIs during normal operation. <br>
Mitigation: Review the configured sources before use and run it only in environments where those outbound requests are allowed. <br>
Risk: Fetched article text may be sent to an LLM for summarization. <br>
Mitigation: Use the skill only with public article URLs and review generated summaries before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nerua1/nerua1-prasowka) <br>
- [Topics](references/topics.md) <br>
- [Sources](references/sources.md) <br>
- [Format](references/format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, HTML, Shell commands, Configuration] <br>
**Output Format:** [Single HTML file with inline CSS and JavaScript, plus command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated HTML portal to the local canvas directory and may update local seen-url state.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
