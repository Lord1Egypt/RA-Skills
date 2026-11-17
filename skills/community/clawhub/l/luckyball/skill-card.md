## Description:

Luckyball generates Chinese Double Color Ball lottery number predictions using BaZi-style calendar features and random-forest/AR(1) models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landyun](https://clawhub.ai/user/landyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to produce entertainment-only lottery prediction reports for a requested draw date, including BaZi analysis, ranked red and blue ball candidates, five candidate number sets, and backtest summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent prediction history reads and writes, memory-index updates, and web searches may occur without clear per-action user control.

Mitigation: Review before installing; require explicit user approval for each read, write, memory update, and web lookup, or change persistence to a skill-owned local data file.

Risk: Lottery predictions may be mistaken for reliable betting advice even though the artifact describes them as entertainment-only and notes that lottery draws are random.

Mitigation: Keep the entertainment-only disclaimer visible in generated reports and avoid presenting recommendations as financially reliable predictions.

## Reference(s):

- [Luckyball ClawHub Skill Page](https://clawhub.ai/landyun/skills/luckyball)
- [landyun ClawHub Publisher Profile](https://clawhub.ai/user/landyun)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with analysis tables, ranked lottery-number candidates, and brief guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prior prediction comparison when stored history is available.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
