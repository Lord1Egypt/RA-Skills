## Description: <br>
Political sentiment analysis using PoliBERTweet, a RoBERTa model pre-trained on political tweets, to analyze support, opposition, and stance toward political figures and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to classify political text from direct input, local files, standard input, or Reddit searches into support, oppose, or neutral sentiment. It is best used as one signal alongside polling, market, and domain evidence rather than as a standalone forecasting source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Political text or research terms may be sensitive, especially when using Reddit search or processing private local files. <br>
Mitigation: Avoid using confidential political text or private research terms; review inputs before running Reddit-backed collection. <br>
Risk: Sentiment and market-helper outputs may be stale, biased, or misleading if treated as a complete forecast. <br>
Mitigation: Use the skill as one analytical signal and validate findings against current polling, market data, and other domain evidence. <br>
Risk: The first model run can download a large HuggingFace model and may fail in restricted network environments. <br>
Mitigation: Confirm model download permissions, storage, and network access before deployment. <br>


## Reference(s): <br>
- [PoliBERTweet GitHub repository](https://github.com/GU-DataLab/PoliBERTweet) <br>
- [PoliBERTweet LREC 2022 paper](https://aclanthology.org/2022.lrec-1.801) <br>
- [ClawHub skill page](https://clawhub.ai/erongcao/polibert-sentiment) <br>
- [Publisher profile](https://clawhub.ai/user/erongcao) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable sentiment summaries or structured JSON results from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download a HuggingFace model on first run and may query Reddit when the Reddit option is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
