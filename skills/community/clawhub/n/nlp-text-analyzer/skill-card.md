## Description:

Analyzes Chinese and English text with tokenization, sentiment analysis, keyword extraction, summarization, word-frequency statistics, basic named-entity recognition, text classification, and similarity scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze Chinese and English text for tokenization, sentiment, keywords, summaries, word frequencies, basic classification, and similarity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python NLP dependencies are version-ranged and resolved from current package indexes.

Mitigation: Pin or lock jieba, snownlp, and textblob before reproducible or production use.

Risk: The included basic_usage.py example has a syntax error.

Mitigation: Correct the unterminated triple-quoted string before running examples; the core analyzer module compiles separately.

## Reference(s):

- [NLP Text Analyzer repository](https://github.com/kaiyuelv/nlp-text-analyzer)
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/nlp-text-analyzer)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Markdown guidance and Python data structures containing analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python NLP processing; results depend on jieba, SnowNLP, and TextBlob behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
