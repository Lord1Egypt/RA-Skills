## Description: <br>
Advanced NLP with perplexity scoring, burstiness analysis, and entropy calculation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to analyze input text for AI-content indicators using perplexity, sentence-length burstiness, entropy, and token distribution metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-content detection can be misleading because the skill uses simplified statistical heuristics rather than a full language model. <br>
Mitigation: Treat the result as a rough signal, require human review before making authorship decisions, and avoid using confidence scores as definitive proof. <br>
Risk: Very short text may not provide enough signal for meaningful analysis. <br>
Mitigation: Use the minimum text length setting and request more input when the skill returns a short-text error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/nlp-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [Structured JavaScript object with detection flag, confidence score, metric values, token statistics, thresholds, and explanatory text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts configurable perplexity threshold, burstiness threshold, and minimum text length.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
