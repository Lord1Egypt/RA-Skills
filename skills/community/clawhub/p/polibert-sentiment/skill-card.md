## Description:

Provides political sentiment analysis with PoliBERTweet for support, opposition, and neutral stance detection over direct text, local files, stdin, and Reddit political discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and researchers use this skill to classify political sentiment around candidates, figures, issues, and events from text, files, stdin, or Reddit discussions. It is best used as one signal in a broader analysis or forecasting workflow, not as a standalone decision source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Political sentiment outputs may be mistaken for dependable forecasts or representative public opinion.

Mitigation: Treat outputs as experimental and combine them with other evidence such as polling, market data, and source review.

Risk: Local files or political research inputs may contain sensitive information.

Mitigation: Avoid private or sensitive inputs unless the runtime environment and downstream handling are approved.

Risk: The Hugging Face model and Python dependencies affect reliability and supply-chain exposure.

Mitigation: Pin and verify the model and update vulnerable dependencies before installing in controlled environments.

Risk: The bundled Polymarket script is under-documented relative to the sentiment-analysis workflow.

Mitigation: Remove it or clearly document its role before relying on the package.

## Reference(s):

- [PoliBERTweet Repository](https://github.com/GU-DataLab/PoliBERTweet)
- [PoliBERTweet LREC 2022 Paper](https://aclanthology.org/2022.lrec-1.801)
- [ClawHub Skill Page](https://clawhub.ai/erongcao/skills/polibert-sentiment)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; sentiment tool output can be human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes direct text, stdin, local files, or Reddit search results; first model use may download an approximately 500 MB Hugging Face model.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
